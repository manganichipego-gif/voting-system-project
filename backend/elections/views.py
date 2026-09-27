from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Candidate, Vote
from .serializers import CandidateSerializer

class CandidateList(generics.ListAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer

class VoteCreate(APIView):
    def post(self, request, *args, **kwargs):
        # Retrieve the dictionary of checked boxes from React
        votes_data = request.data.get('votes', {})
        
        # TEMPORARY: Grab your superuser to act as the voter so the database doesn't block the test
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
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response

class ElectionResults(APIView):
    def get(self, request, *args, **kwargs):
        # Groups candidate votes and returns counts
        results = Candidate.objects.annotate(vote_count=Count('vote')).values(
            'id', 'name', 'position', 'party', 'vote_count'
        )
        return Response(list(results))