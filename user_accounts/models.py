from django.contrib.auth.models import AbstractUser
from django.db import models

# 1. Main User Model (With Roles Switches)
class User(AbstractUser):
    is_recruiter = models.BooleanField(default=False)
    is_candidate = models.BooleanField(default=False)

    def __str__(self):
        return self.username

# 2. Recruiter Profile Table
class RecruiterProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    company_name = models.CharField(max_length=255, blank=True)
    website = models.URLField(blank=True)
    
    def __str__(self):
        return f"{self.user.username} - Recruiter"

# 3. Candidate Profile Table
class CandidateProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(max_length=15, blank=True)
    skills = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.user.username} - Candidate"
