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
    

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import RegistrationRequest, ElectionSettings

# ... (Make sure your existing views for candidates and voting stay above this line) ...

@api_view(['POST'])
def request_registration(request):
    username = request.data.get('username')
    email = request.data.get('email')
    
    if RegistrationRequest.objects.filter(email=email).exists():
        return Response({'error': 'Email already registered.'}, status=400)
        
    RegistrationRequest.objects.create(username=username, email=email)
    return Response({'success': 'Registration requested successfully! Waiting for admin approval.'})

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