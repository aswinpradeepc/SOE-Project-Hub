from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .forms import *
from django.contrib.auth.models import Group

def ask_login(request):
    return render(request, 'auth_login/ask_login.html')


def register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        print(form)
        if form.is_valid():
            user = form.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend' 
            login(request, user)
            return redirect('/')  # Replace with your desired redirect URL
        else:
            print("Form is not valid")
            print(form.errors)
    else:
        form = StudentRegistrationForm()
    return render(request, 'auth_login/register.html', {'form': form})

def student_login(request):
    if request.method == 'POST':
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')  # Use 'username' here
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None and user.groups.filter(name='Students').exists():
                login(request, user)
                print("login success")
                return redirect('/')  # Redirect to student dashboard
            else:
                form.add_error(None, 'Invalid email or password')
    else:
        form = StudentLoginForm()
    return render(request, 'auth_login/student_login.html', {'form': form})

from django.contrib import messages

def faculty_login(request):
    if request.method == 'POST':
        form = FacultyLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(f"Attempting login for user: {username} with password: {password}")
            
            user = authenticate(request, username=username, password=password)
            if user is None:
                print("Authentication failed: user is None")
                form.add_error(None, 'Invalid email or password')
            else:
                print(f"User authenticated: {user}")
                faculty_group = Group.objects.get(name='Faculty')
                if faculty_group in user.groups.all():
                    login(request, user)
                    print("Login success")
                    return redirect('/')  # Redirect to faculty dashboard
                else:
                    print(f"User is not in Faculty group. User groups: {user.groups.all()}")
                    form.add_error(None, 'You do not have permission to access this page')
        else:
            print("Form is not valid")
            print(form.errors)
    else:
        form = FacultyLoginForm()
    return render(request, 'auth_login/faculty_login.html', {'form': form})
