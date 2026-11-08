from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Job, Application

# 1. Recruiter Dashboard (Lists jobs posted by HR & candidate responses)
@login_required
def recruiter_dashboard(request):
    # Security Check: Login pannirukavanga Recruiter-ah nu check panrom
    if not request.user.is_recruiter:
        messages.error(request, "Access Denied! You are not a Recruiter.")
        return redirect('candidate_dashboard')
        
    # 1. Intha login panni irukura HR post panna Jobs-ah mattum database-la irundhu edukkurom
    my_jobs = Job.objects.filter(recruiter=request.user).order_by('-created_at')
    
    # 2. Oru oru job-kum apply panna candidates-oda list-ah match_score padi Descending Order-la (High to Low) adukkuroam
    for job in my_jobs:
        # '-match_score' nu munnadi minus (-) potta, high percentage top-la varum
        job.ranked_applications = job.application_set.all().order_by('-match_score')
        
    # 3. Intha data-va azhaga HTML template page-ku render panrom
    return render(request, 'jobs/recruiter_dashboard.html', {'jobs': my_jobs})


# 2. Job Creation View (For HR to post a new job vacancy)
@login_required
def post_job(request):
    if not request.user.is_recruiter:
        return redirect('candidate_dashboard')
        
    if request.method == 'POST':
        title = request.POST.get('title')
        company = request.POST.get('company_name')
        desc = request.POST.get('description')
        reqs = request.POST.get('requirements')
        loc = request.POST.get('location')
        
        Job.objects.create(
            recruiter=request.user,
            title=title,
            company_name=company,
            description=desc,
            requirements=reqs,
            location=loc
        )
        messages.success(request, "Job Vacancy Posted Successfully!")
        return redirect('recruiter_dashboard')
        
    return render(request, 'jobs/post_job.html')


# 3. Candidate Dashboard
@login_required
def candidate_dashboard(request):

    if not request.user.is_candidate:
        messages.error(request, "Access Denied!")
        return redirect('recruiter_dashboard')

    all_jobs = Job.objects.filter(
        is_active=True
    ).order_by('-created_at')

    return render(
        request,
        'jobs/candidate_dashboard.html',
        {'jobs': all_jobs}
    )


# 4. Candidate Apply Job with Resume Upload
@login_required
def apply_job(request, job_id):

    # Step 1: Check Candidate
    if not request.user.is_candidate:
        messages.error(request, "Only candidates can apply.")
        return redirect('recruiter_dashboard')

    # Step 2: Get Job Details
    job = get_object_or_404(Job, id=job_id, is_active=True)

    # Step 3: Check Already Applied
    already_applied = Application.objects.filter(
        job=job,
        candidate=request.user
    ).exists()

    if already_applied:
        messages.warning(request, "You have already applied for this job.")
        return redirect('candidate_dashboard')

    # Step 4: Get Resume
    if request.method == 'POST':

        resume = request.FILES.get('resume')

        if not resume:
            messages.error(request, "Please upload your resume.")
            return redirect('apply_job', job_id=job.id)

        # Step 5: Check PDF Format
        if not resume.name.lower().endswith('.pdf'):
            messages.error(request, "Please upload PDF only.")
            return redirect('apply_job', job_id=job.id)

        # Step 6: Save Application
        Application.objects.create(
            job=job,
            candidate=request.user,
            resume=resume
        )

        messages.success(request, "Job Applied Successfully!")
        return redirect('candidate_dashboard')

    # Step 7: Open Apply Page
    return render(request, 'jobs/apply_job.html', {'job': job})
