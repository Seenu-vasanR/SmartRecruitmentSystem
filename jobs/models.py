from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings

# 1. Job Posting Table
class Job(models.Model):
    # settings.AUTH_USER_MODEL use panni accounts.User kooda link panrom
    recruiter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    description = models.TextField()
    requirements = models.TextField(help_text="Skills needed (e.g. Python, SQL, Django)")
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} - {self.company_name}"

# 2. Application Tracking Table
class Application(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('screening', 'Screening'),
        ('interview', 'Interview Scheduled'),
        ('accepted', 'Offered'),
        ('rejected', 'Rejected'),
    ]
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    candidate = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    resume_text = models.TextField(blank=True, help_text="Extracted text from resume for smart matching")
    resume = models.FileField(
    upload_to='resumes/',
    blank=True,
    null=True
  )
    match_score = models.FloatField(default=0.0) # Smart Ranking Score Percentage
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.candidate.username} applied for {self.job.title}"
