
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/recruiter/', views.recruiter_dashboard, name='recruiter_dashboard'),
    path('dashboard/candidate/', views.candidate_dashboard, name='candidate_dashboard'),
    path('post-job/', views.post_job, name='post_job'),

    # Candidate Apply Job
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
]
