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
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            print(email,password)
            if user is not None and user.groups.filter(name='Students').exists():
                login(request, user)
                return redirect('student_dashboard')  # Redirect to student dashboard
            else:
                form.add_error(None, 'Invalid email or password')
    else:
        form = StudentLoginForm()
    return render(request, 'auth_login/student_login.html', {'form': form})

def faculty_login(request):
    if request.method == 'POST':
        form = FacultyLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None and user.groups.filter(name='Faculty').exists():
                login(request, user)
                return redirect('faculty_dashboard')  # Redirect to faculty dashboard
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = FacultyLoginForm()
    return render(request, 'auth_login/faculty_login.html', {'form': form})
