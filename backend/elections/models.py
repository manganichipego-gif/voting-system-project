from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone
import random

def generate_5_digit_code():
    return str(random.randint(10000, 99999))

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

class ElectionSettings(models.Model):
    start_time = models.DateTimeField(help_text="When voting opens")
    end_time = models.DateTimeField(help_text="When voting closes")
    results_released = models.BooleanField(default=False, help_text="Check this to reveal results to students")

    class Meta:
        verbose_name_plural = "Election Settings"

    def is_voting_open(self):
        now = timezone.now()
        return self.start_time <= now <= self.end_time

    def __str__(self):
        return "Global Election Control Panel"


class RegistrationRequest(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    is_approved = models.BooleanField(default=False)
    approval_code = models.CharField(max_length=5, default=generate_5_digit_code, editable=False) 
    
    admin_token = models.UUIDField(default=uuid.uuid4, editable=False) 
    
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.username} - {self.email}"

class ElectionSettings(models.Model):
    start_time = models.DateTimeField(help_text="When voting opens")
    end_time = models.DateTimeField(help_text="When voting closes")
    results_released = models.BooleanField(default=False, help_text="Check this to reveal results to students")

    class Meta:
        verbose_name_plural = "Election Settings"

    def is_voting_open(self):
        now = timezone.now()
        return self.start_time <= now <= self.end_time

    def __str__(self):
        return "Global Election Control Panel"