from django.urls import path
from . import views

urlpatterns = [
    path('candidates/', views.CandidateList.as_view(), name='candidate-list'),
    path('vote/', views.VoteCreate.as_view(), name='vote-create'),
    # Add this new line for the results:
    path('results/', views.ElectionResults.as_view(), name='election-results'), 
]