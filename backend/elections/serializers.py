from rest_framework import serializers
from .models import Candidate, Vote

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        # Expose the new fields to the React frontend
        fields = ['id', 'name', 'position', 'party', 'portrait', 'party_logo'] 

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'