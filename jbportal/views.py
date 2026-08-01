from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.shortcuts import redirect
from .models import *
from django.contrib.auth.models import User
from django.http import JsonResponse

#home page
def home(request):
    return render(request, 'home.html')

#login page
def login(request):
    if request.user.is_authenticated:
        if request.user.profile.role == 'job_seeker':
            return redirect('jobs')
        elif request.user.profile.role == 'employer':
            return redirect('employer_dashboard')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            auth_login(request, user)

            if user.profile.role == 'job_seeker':
                return redirect('jobs')
            elif user.profile.role == 'employer':
                return redirect('employer_dashboard')

        messages.error(request, 'Invalid email or password.')
        return redirect('login')

    return render(request, 'login.html')

#register page
def register(request):
    if request.user.is_authenticated:
        if request.user.profile.role == 'job_seeker':
            return render(request, 'job_seeker_dashboard.html')
        elif request.user.profile.role == 'employer':
            return render(request, 'employer_dashboard.html')
    if request.method == 'POST':
        name =request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        if User.objects.filter(username=email).exists():
            messages.error(request, 'Email is already registered.')
            return redirect('register')

        # Create the user and save it to the database

        user = User.objects.create_user(username=email, email=email, password=password, first_name=name)
        profile = Profile(user=user, role=request.POST.get('role'))
        profile.save()
        auth_login(request, user)  # Log in the user after registration
        return redirect('job_seeker_dashboard')  # Redirect to the job seeker dashboard after successful registration

    return render(request, 'register.html')

@login_required(login_url='login')
def post_job(request):

    if not request.user.is_authenticated or request.user.profile.role != 'employer':
        return redirect('/access-denied')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        location = request.POST.get('location')
        company = request.POST.get('company')
        apply_link = request.POST.get('apply_link')
        category = request.POST.get('category')
        job_type = request.POST.get('job_type')
        apply_type = request.POST.get('apply_type')
        added_by = request.user
        job = Job(title=title, description=description, location=location, company=company, apply_link=apply_link, category_id=category, job_type_id=job_type, apply_type=apply_type, added_by=added_by)
        job.save()
    categories = Category.objects.all()
    job_types = JobType.objects.all()
    return render(request, 'post-job.html', {'categories': categories, 'job_types': job_types})

#jobs page for job seeker
@login_required(login_url='login')
def jobs(request):

    if not request.user.is_authenticated or request.user.profile.role == 'employer':
        return redirect('/employer-dashboard')
    
    jobs = Job.objects.all()
    return render(request, 'jobs.html', {'jobs': jobs})

#job details page and apply page for job seeker
@login_required(login_url='login')
def job(request, id):

    if not request.user.is_authenticated or request.user.profile.role == 'employer':
        return redirect('/access-denied')
    
    job = Job.objects.get(id=id)

    if request.user not in job.views.all():
        job.views.add(request.user)
        job.save()

    if request.method == "POST":
        
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        resume = request.FILES.get("resume")

        JobApplication.objects.create(
            job=job,
            name=name,
            email=email,
            phone=phone,
            resume=resume
        )

        messages.success(request, "Application submitted successfully.")

        return redirect("jobs")

    return render(request, "job.html", {"job": job})

#dashboard for employer
@login_required(login_url='login')
def employer_dashboard(request):
    if not request.user.is_authenticated or request.user.profile.role != 'employer':
        return redirect('/access-denied')

    jobs = Job.objects.filter(added_by=request.user)
    return render(request, 'employer-dashboard.html', {'jobs': jobs})

#manage job post, employer can see here post analytics and (edit, delete)
@login_required(login_url='login')
def manage_job(request, id):
    if not request.user.is_authenticated or request.user.profile.role != 'employer':
        return redirect('access-denied')
    
    job = Job.objects.get(id=id, added_by=request.user)
    views_count = job.views.count()  # Count the number of views for the job
    applications_count = JobApplication.objects.filter(job=job).count()  # Count the number of applications for the job 


    return render(request, 'manage-job.html', {'job': job, 'views_count': views_count, 'applications_count': applications_count})

# job post edit page
@login_required(login_url='login')
def edit_job(request, id):

    if not request.user.is_authenticated or request.user.profile.role != 'employer':
        return redirect('/access-denied')
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        location = request.POST.get('location')
        company = request.POST.get('company')
        apply_link = request.POST.get('apply_link')
        category = request.POST.get('category')
        job_type = request.POST.get('job_type')
        apply_type = request.POST.get('apply_type')
        added_by = request.user
        job = Job(title=title, description=description, location=location, company=company, apply_link=apply_link, category_id=category, job_type_id=job_type, apply_type=apply_type, added_by=added_by)
        job.save()
    job = Job.objects.get(id=id, added_by=request.user)
    categories = Category.objects.all()
    job_types = JobType.objects.all()
    return render(request, 'edit-job.html', {'job':job, 'categories': categories, 'job_types': job_types})

def access_denied(request):
    return render(request, 'cant-access.html')