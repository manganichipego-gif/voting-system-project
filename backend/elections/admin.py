from django.contrib import admin
from .models import Candidate, Vote

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    # This controls the columns you see in the admin panel
    list_display = ('id', 'voter', 'candidate', 'position')
    # This adds a filter sidebar
    list_filter = ('position', 'candidate')
    
@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'party')