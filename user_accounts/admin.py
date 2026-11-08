
from django.contrib import admin
from .models import User, CandidateProfile, RecruiterProfile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_candidate', 'is_recruiter')
    search_fields = ('username', 'email')


@admin.register(CandidateProfile)
class CandidateProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'skills')
    search_fields = ('user__username', 'phone_number')


@admin.register(RecruiterProfile)
class RecruiterProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'website')
    search_fields = ('user__username', 'company_name')
