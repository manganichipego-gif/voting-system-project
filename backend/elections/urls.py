from django.urls import path
from . import views

urlpatterns = [
    path('candidates/', views.CandidateList.as_view(), name='candidate-list'),
    path('vote/', views.VoteCreate.as_view(), name='vote-create'),
    path('results/', views.ElectionResults.as_view(), name='election-results'), 
    path('register/', views.request_registration, name='request_registration'),
    path('status/', views.election_status, name='election_status'),
    path('setup-password/', views.setup_password, name='setup_password'),
]