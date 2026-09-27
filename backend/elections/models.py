from django.db import models
from django.contrib.auth.models import User

class Candidate(models.Model):
    portrait = models.ImageField(upload_to='portrait/', blank=True, null=True)
    name = models.CharField(max_length=100)
    party = models.CharField(max_length=100, blank=True, null=True)
    position = models.CharField(max_length=100)
    party_logo = models.ImageField(upload_to='logos/', blank=True, null=True)

    def __str__(self):
        return self.name


class Vote(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    position = models.CharField(max_length=100) 
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('voter', 'position')

    def __str__(self):
        return f"{self.voter.username} voted for {self.candidate.name}"


class Election(models.Model):
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=50, choices=[('upcoming', 'Upcoming'), ('active', 'Active'), ('closed', 'Closed')])
    
    def __str__(self):
        return self.title

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    studentRef = models.CharField(max_length=50, unique=True)
    faculty = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.user.username} - {self.studentRef}"

class Eligibility(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    hasVoted = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.student.studentRef} - {self.election.title} - Voted: {self.hasVoted}"