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
    first_name = request.data.get('first_name')
    middle_name = request.data.get('middle_name', '')
    last_name = request.data.get('last_name')
    student_id = request.data.get('student_id')
    email = request.data.get('email')

    if not first_name.replace(' ', '').isalpha():
        return Response({'error': 'First name can only contain letters.'}, status=400)
    if middle_name and not middle_name.replace(' ', '').isalpha():
        return Response({'error': 'Middle name can only contain letters.'}, status=400)
    if not last_name.replace(' ', '').isalpha():
        return Response({'error': 'Last name can only contain letters.'}, status=400)
    if not student_id.isdigit():
        return Response({'error': 'Student ID must be numbers only.'}, status=400)
    
    if RegistrationRequest.objects.filter(student_id=student_id).exists():
        return Response({'error': 'Student ID already registered.'}, status=400)
    
    if RegistrationRequest.objects.filter(email=email).exists():
        return Response({'error': 'Email already registered.'}, status=400)
        
    allowed_domain = [ 'students.cavendish.co.zm']
    if not any(email.endswith(domain) for domain in allowed_domain):
        return Response({'error': 'Only university email addresses are allowed.'}, status=400)

    req = RegistrationRequest.objects.create(
        first_name=first_name,
        middle_name=middle_name,
        last_name=last_name,
        student_id=student_id,
        email=email
    )

    accept_link = f"http://Chipego.pythonanywhere.com/api/admin-decide/{req.admin_token}/accept/"
    decline_link = f"http://Chipego.pythonanywhere.com/api/admin-decide/{req.admin_token}/decline/"
    
    send_mail(
        'Action Required: New Voter Registration',
        f'Student {first_name} {last_name} {student_id} ({email}) has requested access to the voting system.\n\n'
        f'Click here to ACCEPT:\n{accept_link}\n\n'
        f'Click here to DECLINE:\n{decline_link}',
        'systemvoting76@gmail.com',        
        ['manganichipego@gmail.com'],       
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
            f'Hello {req.first_name} {req.last_name},\n\nYour registration has been approved.\n'
            f'Your 5-digit approval code is: {req.approval_code}\n\n'
            f'Go to http://voting-system-project-seven.vercel.app/setup-password to create your account.',
            'systemvoting76@gmail.com', 
            [req.email],            
            fail_silently=False,
        )
        return HttpResponse(f"<h1>Accepted</h1><p>Student {req.first_name} {req.last_name} has been approved. The 5-digit code was sent to their email.</p>")

    elif action == 'decline':
        
        send_mail(
            'University Election - Registration Denied',
            f'Hello {req.first_name} {req.last_name},\n\nUnfortunately, your request to register for the election has been denied by the administrator.',
            'systemvoting76@gmail.com', 
            [req.email],            
            fail_silently=False,
        )
        req.delete()
        return HttpResponse(f"<h1>Declined</h1><p>Student {req.first_name} {req.last_name} was denied. A rejection email has been sent.</p>")


@api_view(['POST'])
def setup_password(request):
    student_id = request.data.get('student_id')
    code = request.data.get('code')
    password = request.data.get('password')

    try:

        req = RegistrationRequest.objects.get(student_id=student_id, approval_code=code, is_approved=True)
        
        if User.objects.filter(username=student_id).exists():
            return Response({'error': 'Account already exists. You can now log in.'}, status=400)

        User.objects.create(
            username=req.student_id,
            email=req.email,
            first_name=req.first_name,
            last_name=req.last_name,
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