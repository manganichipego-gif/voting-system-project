from django.contrib import admin
from .models import Candidate, Vote
from .models import ElectionSettings
from django.contrib import admin
from django.core.mail import send_mail
from .models import Candidate, Vote, ElectionSettings, RegistrationRequest

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
                f'Please go to http://localhost:5173/setup-password to enter this code and create your secure password.',
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
    list_display = ('__str__', 'start_time', 'end_time', 'results_released', 'is_active_now')

    def is_active_now(self, obj):
        return obj.is_voting_open()
    is_active_now.boolean = True
    is_active_now.short_description = "Is Voting Open Now?"