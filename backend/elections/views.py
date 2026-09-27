from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import Candidate, Vote
from .serializers import CandidateSerializer
from rest_framework.decorators import api_view
from django.utils import timezone
from .models import RegistrationRequest, ElectionSettings
from django.db.models import Count
from django.http import HttpResponse
from django.core.mail import send_mail


class CandidateList(generics.ListAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer

class VoteCreate(APIView):
    def post(self, request, *args, **kwargs):
        votes_data = request.data.get('votes', {})
        
        voter = User.objects.first() 
        
        if not voter:
            return Response({"error": "No users exist in the database."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Loop through each page of the ballot and save the selected candidate
            for position, candidate_id in votes_data.items():
                candidate = Candidate.objects.get(id=candidate_id)
                Vote.objects.create(
                    voter=voter,
                    candidate=candidate,
                    position=position
                )
            return Response({"message": "Ballot recorded successfully!"}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ElectionResults(APIView):
    def get(self, request, *args, **kwargs):
        # Groups candidate votes and returns counts
        results = Candidate.objects.annotate(vote_count=Count('vote')).values(
            'id', 'name', 'position', 'party', 'vote_count'
        )
        return Response(list(results))
    


@api_view(['POST'])
def request_registration(request):
    username = request.data.get('username')
    email = request.data.get('email')

    if any(char.isdigit() for char in username):
        return Response({'error': 'Username cannot contain numbers.'}, status=400)
    
    if RegistrationRequest.objects.filter(email=email).exists():
        return Response({'error': 'Email already registered.'}, status=400)
        
    req = RegistrationRequest.objects.create(username=username, email=email)
    
    accept_link = f"http://127.0.0.1:8000/api/admin-decide/{req.admin_token}/accept/"
    decline_link = f"http://127.0.0.1:8000/api/admin-decide/{req.admin_token}/decline/"
    
    send_mail(
        'Action Required: New Voter Registration',
        f'Student {username} ({email}) has requested access to the voting system.\n\n'
        f'Click here to ACCEPT:\n{accept_link}\n\n'
        f'Click here to DECLINE:\n{decline_link}',
        'your.email@gmail.com',         # From email
        ['admin@university.edu'],       # TO YOU (Put your actual email here)
        fail_silently=False,
    )
    
    return Response({'success': 'Registration requested successfully! Waiting for admin approval.'})

def admin_decision(request, token, action):
    try:
        req = RegistrationRequest.objects.get(admin_token=token)
    except RegistrationRequest.DoesNotExist:
        return HttpResponse("<h1>Error</h1><p>This request has already been processed or does not exist.</p>")

    if action == 'accept':
        if req.is_approved:
            return HttpResponse("<h1>Already Approved</h1><p>This student was already approved.</p>")
            
        req.is_approved = True
        req.save()
        
        send_mail(
            'University Election - Registration Approved!',
            f'Hello {req.username},\n\nYour registration has been approved.\n'
            f'Your 5-digit approval code is: {req.approval_code}\n\n'
            f'Go to http://localhost:5173/setup-password to create your account.',
            'your.email@gmail.com', 
            [req.email],            
            fail_silently=False,
        )
        return HttpResponse(f"<h1>Accepted</h1><p>Student {req.username} has been approved. The 5-digit code was sent to their email.</p>")

    elif action == 'decline':
        
        send_mail(
            'University Election - Registration Denied',
            f'Hello {req.username},\n\nUnfortunately, your request to register for the election has been denied by the administrator.',
            'your.email@gmail.com', 
            [req.email],            
            fail_silently=False,
        )
        req.delete()
        return HttpResponse(f"<h1>Declined</h1><p>Student {req.username} was denied. A rejection email has been sent.</p>")


@api_view(['POST'])
def setup_password(request):
    username = request.data.get('username')
    code = request.data.get('code')
    password = request.data.get('password')

    try:

        req = RegistrationRequest.objects.get(username=username, approval_code=code, is_approved=True)
        
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Account already exists. You can now log in.'}, status=400)

        User.objects.create(
            username=req.username,
            email=req.email,
            password=make_password(password)
        )
        
        req.delete()
        
        return Response({'success': 'Password set successfully! You can now log in to the ballot.'})
        
    except RegistrationRequest.DoesNotExist:
        return Response({'error': 'Invalid username, or incorrect 5-digit code, or request not yet approved.'}, status=400)


@api_view(['GET'])
def election_status(request):
    settings = ElectionSettings.objects.first()
    
    if not settings:
        return Response({
            'is_open': False,
            'results_released': False,
            'message': 'Election settings not configured.'
        })
        
    now = timezone.now()
    is_open = settings.start_time <= now <= settings.end_time
    
    return Response({
        'is_open': is_open,
        'results_released': settings.results_released,
        'start_time': settings.start_time,
        'end_time': settings.end_time
    })

@api_view(['POST'])
def submit_ballot(request):
    if not request.user.is_authenticated:
        return Response({'error': 'You must be logged in to cast a vote.'}, status=401)

    votes = request.data.get('votes', {})
    device_footprint = request.data.get('device_id')
    
    if Vote.objects.filter(voter=request.user).exists():
        return Response({'error': 'You have already cast your ballot. Multiple votes are not allowed.'}, status=403)
        
    if device_footprint and Vote.objects.filter(device_id=device_footprint).exists():
        return Response({
            'error': 'SECURITY VIOLATION: A vote has already been cast from this physical device. Multiple votes per device are prohibited.'
        }, status=403)
        
    try:
        for position, candidate_id in votes.items():
            candidate = Candidate.objects.get(id=candidate_id)
            
            Vote.objects.create(
                voter=request.user,
                candidate=candidate,
                device_id=device_footprint
            )
            
        return Response({'success': 'Ballot submitted successfully!'})
        
    except Candidate.DoesNotExist:
        return Response({'error': 'Invalid candidate selected. Please try again.'}, status=400)
    except Exception as e:
        return Response({'error': f'An error occurred: {str(e)}'}, status=500)