from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.shortcuts import redirect
from .models import Profile
from django.contrib.auth.models import User


def home(request):
    return render(request, 'home.html')

def login(request):
    if request.user.is_authenticated:
        if request.user.profile.role == 'job_seeker':
            return redirect('job_seeker_dashboard')
        elif request.user.profile.role == 'employer':
            return redirect('employer_dashboard')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            auth_login(request, user)

            if user.profile.role == 'job_seeker':
                return redirect('job_seeker_dashboard')
            elif user.profile.role == 'employer':
                return redirect('employer_dashboard')

        messages.error(request, 'Invalid email or password.')
        return redirect('login')

    return render(request, 'login.html')

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