from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .models import User, CandidateProfile, RecruiterProfile
from django.contrib.auth import authenticate

# 1. Candidate Sign-Up View
def candidate_signup(request):
    if request.method == 'POST':
        # HTML design form-la irundhu user input data-va direct-ah backend edukkurom
        uname = request.POST.get('username')
        pword = request.POST.get('password')
        email = request.POST.get('email')
        phone = request.POST.get('phone_number')
        skills = request.POST.get('skills')

        # Check: Intha username-la already user irukangala?
        if User.objects.filter(username=uname).exists():
            messages.error(request, "Username already exists!")
            return render(request, 'user_accounts/candidate_signup.html')

        # Main account create aaguthu (Password automatic-ah encrypt aydum)
        user = User.objects.create_user(username=uname, password=pword, email=email)
        user.is_candidate = True # Roles-ah fix panrom
        user.save()

        # Automatic-ah linked candidate details table record update aaguthu
        CandidateProfile.objects.create(user=user, phone_number=phone, skills=skills)

        # Success! Direct login dynamic response login
        login(request, user)
        messages.success(request, "Candidate Registration Successful!")
        return redirect('candidate_dashboard') 

    return render(request, 'user_accounts/candidate_signup.html')


# 2. Recruiter Sign-Up View

# 3. User Login View
def user_login(request):

    if request.method == 'POST':
        uname = request.POST.get('username')
        pword = request.POST.get('password')

        user = authenticate(
            request,
            username=uname,
            password=pword
        )

        if user is not None:
            login(request, user)
            messages.success(request, "Login Successful!")

            if user.is_recruiter:
                return redirect('recruiter_dashboard')
            elif user.is_candidate:
                return redirect('candidate_dashboard')

        else:
            messages.error(request, "Invalid Username or Password!")

    return render(request, 'user_accounts/login.html')

def recruiter_signup(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        pword = request.POST.get('password')
        email = request.POST.get('email')
        c_name = request.POST.get('company_name')
        web = request.POST.get('website')

        if User.objects.filter(username=uname).exists():
            messages.error(request, "Username already exists!")
            return render(request, 'user_accounts/recruiter_signup.html')

        user = User.objects.create_user(username=uname, password=pword, email=email)
        user.is_recruiter = True # Roles-ah fix panrom
        user.save()

        # Linked recruiter company profile row insert update aaguthu
        RecruiterProfile.objects.create(user=user, company_name=c_name, website=web)

        login(request, user)
        messages.success(request, "Recruiter Registration Successful!")
        return redirect('recruiter_dashboard')

    return render(request, 'user_accounts/recruiter_signup.html')

# Home Page View
def home_page(request):
    return render(request, 'user_accounts/home.html')