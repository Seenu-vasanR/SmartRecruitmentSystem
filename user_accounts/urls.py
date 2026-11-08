from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('signup/candidate/', views.candidate_signup, name='candidate_signup'),
    path('signup/recruiter/', views.recruiter_signup, name='recruiter_signup'),

    path('login/', views.user_login, name='user_login'),

   path('logout/', LogoutView.as_view(next_page='user_login'), name='logout'),
]