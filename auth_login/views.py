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

def faculty_login(request):
    print("Faculty login view called")
    if request.method == 'POST':
        print("POST request received")
        form = FacultyLoginForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            print(f"Email: {email}, Password: {password}")
            user = authenticate(request, username=email, password=password)
            if user is not None:
                print(f"Authenticated user: {user}")
                if user.groups.filter(name='Faculty').exists():
                    print("User is in Faculty group")
                    login(request, user)
                    return redirect('faculty_dashboard')
                else:
                    print("User is not in Faculty group")
                    form.add_error(None, 'Invalid email or password')
            else:
                print("Authentication failed")
                form.add_error(None, 'Invalid email or password')
        else:
            print("Form is not valid")
            print(form.errors)  # Print form errors for debugging
    else:
        print("GET request received")
        form = FacultyLoginForm()
    return render(request, 'auth_login/faculty_login.html', {'form': form})

    print("Faculty login view called")
    if request.method == 'POST':
        print("POST request received")
        form = FacultyLoginForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            print(f"Email: {email}, Password: {password}")  # Detailed debug print
            user = authenticate(request, username=email, password=password)
            if user is not None:
                print(f"Authenticated user: {user}")
                if user.groups.filter(name='Faculty').exists():
                    print("User is in Faculty group")
                    login(request, user)
                    return redirect('/')
                else:
                    print("User is not in Faculty group")
                    form.add_error(None, 'Invalid email or password')
            else:
                print("Authentication failed")
                form.add_error(None, 'Invalid email or password')
        else:
            print("Form is not valid")
            print(form.errors)  # Print form errors for debugging
    else:
        print("GET request received")
        form = FacultyLoginForm()
    return render(request, 'auth_login/faculty_login.html', {'form': form})

