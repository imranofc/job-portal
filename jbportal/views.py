from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.shortcuts import redirect
from .models import *
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages

#home page
def home(request):
    categories = Category.objects.all()
    return render(request, 'home.html', context={"categories": categories})

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
            return redirect("jobs")
        elif request.user.profile.role == 'employer':
            return redirect("employer_dashboard")
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

        data = {
            'title': request.POST.get('title'),
            'description': request.POST.get('description'),
            'location': request.POST.get('location'),
            'company': request.POST.get('company'),
            'category': request.POST.get('category'),
            'job_type': request.POST.get('job_type'),
            'apply_type': request.POST.get('apply_type'),
            'apply_link': request.POST.get('apply_link'),
        }

        required_fields = {
            'title': 'Job title',
            'description': 'Description',
            'location': 'Location',
            'company': 'Company',
            'category': 'Category',
            'job_type': 'Job type',
            'apply_type': 'Apply type',
        }

        for field, name in required_fields.items():
            if not data[field]:
                messages.error(request, f"{name} is required.")
                return redirect("post_job")

        if data['apply_type'] == 'link' and not data['apply_link']:
            messages.error(request, "Please provide an application link.")
            return redirect("post_job")

        if data['apply_type'] == 'resume' and data['apply_link']:
            messages.error(
                request,
                "Please do not provide an application link when using Resume."
            )
            return redirect("post_job")

        job = Job(
            title=data['title'],
            description=data['description'],
            location=data['location'],
            company=data['company'],
            category_id=data['category'],
            job_type_id=data['job_type'],
            apply_type=data['apply_type'],
            apply_link=data['apply_link'],
            added_by=request.user
        )

        job.save()
        messages.success(request, "Job posted successfully.")
        return redirect("post_job")
    categories = Category.objects.all()
    job_types = JobType.objects.all()
    return render(request, 'post-job.html', {'categories': categories, 'job_types': job_types})

#jobs page for job seeker
@login_required(login_url='login')
def jobs(request):

    if not request.user.is_authenticated or request.user.profile.role == 'employer':
        return redirect('/employer-dashboard')

    location = request.GET.get("location", "")
    job_type = request.GET.get("job_type", "")
    category = request.GET.get("category", "")

    filters = {}

    if location:
        filters["location__icontains"] = location

    if job_type:
        filters["job_type__name__iexact"] = job_type

    if category:
        filters["category__name__iexact"] = category

    jobs = Job.objects.filter(**filters).order_by('-posted_date')
    categories = Category.objects.all()
    job_types = JobType.objects.all()

    return render(request, "jobs.html", {"jobs": jobs, "job_types": job_types, "categories": categories})

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

    jobs = Job.objects.filter(added_by=request.user).order_by('-posted_date')
    return render(request, 'employer-dashboard.html', {'jobs': jobs})

#manage job post, employer can see here post analytics and (edit, delete)
@login_required(login_url='login')
def manage_job(request, id):

    if request.method == 'POST':
        job = Job.objects.get(id=id, added_by=request.user)
        job.status = 'inactive'
        job.save()
        return JsonResponse({"success": True})
    
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

@login_required(login_url='login')
def logout(request):
    auth_logout(request)
    return redirect('login')

@login_required(login_url='login')
def job_views(request, id):

    if request.user.profile.role != 'employer':
        return redirect('access-denied')

    job = Job.objects.get(id=id, added_by=request.user)

    viewers = job.views.all()

    return render(request, 'job-views.html', {
        'job': job,
        'viewers': viewers
    })


@login_required(login_url='login')
def job_applications(request, id):

    if request.user.profile.role != 'employer':
        return redirect('access-denied')

    job = Job.objects.get(id=id, added_by=request.user)

    applications = JobApplication.objects.filter(job=job).order_by('-applied_date')

    return render(request, 'job-applications.html', {
        'job': job,
        'applications': applications
    })