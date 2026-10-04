from django.contrib import admin
from .models import Candidate, Vote
from .models import ElectionSettings
from django.contrib import admin
from django.core.mail import send_mail
from .models import Candidate, Vote, ElectionSettings, RegistrationRequest
from django.core.mail import send_mail, send_mass_mail
from django.contrib.auth.models import User

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'voter', 'candidate', 'position')
    list_filter = ('position', 'candidate')
    
@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'party')


@admin.action(description='Approve selected students and send email')
def approve_requests(modeladmin, request, queryset):
    for req in queryset:
        if not req.is_approved:
            req.is_approved = True
            req.save()
            
            # Send the automated email with the 5-digit code
            send_mail(
                'University Election - Registration Approved!',
                f'Hello {req.username},\n\nYour registration to vote has been approved by the Admin.\n\n'
                f'Your 5-digit approval code is: {req.approval_code}\n\n'
                f'Please go to https://voting-system-project.onrender.com/api/setup-password/ to enter this code and create your secure password.',
                'votingsystem76@gmail.com', 
                [req.email],            
                fail_silently=False,
            )

@admin.register(RegistrationRequest)
class RegistrationRequestAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_approved', 'created_at')
    actions = [approve_requests] 

@admin.register(ElectionSettings)
class ElectionSettingsAdmin(admin.ModelAdmin):
    list_display = ['start_time', 'end_time', 'results_released']
    
    # Register all three actions
    actions = [
        'open_election_and_notify', 
        'close_election_and_notify', 
        'release_results_and_notify'
    ]

    @admin.action(description='1. Announce Election OPEN & Email Voters')
    def open_election_and_notify(self, request, queryset):
        voters = User.objects.filter(is_superuser=False).exclude(email='')
        messages = []
        for voter in voters:
            subject = 'University Election is Now OPEN!'
            message = (
                f'Hello {voter.username},\n\n'
                f'The voting portal is officially open! '
                f'Please log in to https://voting-system-project-1.onrender.com/api/setup-password/ to cast your vote.'
            )
            from_email = 'systemvoting76@gmail.com' 
            messages.append((subject, message, from_email, [voter.email]))
            
        if messages:
            send_mass_mail(messages, fail_silently=False)
        self.message_user(request, f"Opening announced! Emails sent to {len(messages)} students.")

    @admin.action(description='2. Announce Election CLOSED & Email Voters')
    def close_election_and_notify(self, request, queryset):
        voters = User.objects.filter(is_superuser=False).exclude(email='')
        messages = []
        for voter in voters:
            subject = 'University Election is Now CLOSED'
            message = (
                f'Hello {voter.username},\n\n'
                f'The voting period has officially ended. Thank you for participating. '
                f'The final results will be published soon by the administrator.'
            )
            from_email = 'systemvoting76@gmail.com' 
            messages.append((subject, message, from_email, [voter.email]))
            
        if messages:
            send_mass_mail(messages, fail_silently=False)
        self.message_user(request, f"Closing announced! Emails sent to {len(messages)} students.")

    @admin.action(description='3. Publish Results & Email Voters')
    def release_results_and_notify(self, request, queryset):
        queryset.update(results_released=True)
        voters = User.objects.filter(is_superuser=False).exclude(email='')
        messages = []
        for voter in voters:
            subject = 'University Election Results Published!'
            message = (
                f'Hello {voter.username},\n\n'
                f'The official election results are now live! '
                f'Log in to the voting portal to view the final counts.'
            )
            from_email = 'systemvoting76@gmail.com' 
            messages.append((subject, message, from_email, [voter.email]))
            
        if messages:
            send_mass_mail(messages, fail_silently=False)
        self.message_user(request, f"Results released! Emails sent to {len(messages)} students.")
