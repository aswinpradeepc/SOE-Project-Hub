from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .forms import *
from django.contrib.auth.models import Group
from django.contrib import messages
from project.models import Team, Project
from .models import FacultyProfile, StudentProfile
from django.contrib.auth.decorators import login_required


def ask_login(request):
    return render(request, 'auth_login/ask_login.html')

@login_required
def team_selection(request):
    return render(request, 'auth_login/team_selection.html')

@login_required
def join_team(request):
    if request.method == 'POST':
        team_code = request.POST.get('team-code')
        print(team_code)
        # Assuming project_id is shared with the student somehow, perhaps via a query parameter or session
        project_id = team_code  # Adjust this based on how project_id is passed
        
        try:
            team = Team.objects.get(project_id=project_id)
            student_profile = request.user.student_profile
            
            # Assign student to the team
            if not team.member2:
                team.member2 = student_profile
            elif not team.member3:
                team.member3 = student_profile
            elif not team.member4:
                team.member4 = student_profile
            else:
                messages.error(request, 'Team is already full.')
                return redirect('join_team')  # Redirect to join team page with error message

            team.save()
            messages.success(request, 'You have successfully joined the team.')
            return redirect('student_dashboard')  # Redirect to student dashboard upon success

        except Team.DoesNotExist:
            messages.error(request, 'Invalid team code or project ID.')
            return redirect('join_team')  # Redirect to join team page with error message

    return render(request, 'auth_login/join-team.html')


@login_required
def create_team(request):
    if request.method == 'POST':
        faculty_id = request.POST.get('faculty')
        project_title = request.POST.get('project-title')
        project_description = request.POST.get('project-description')

        faculty = FacultyProfile.objects.get(id=faculty_id)
        faculty.team_count += 1
        faculty.save()

        # Create the Project instance with necessary fields
        project = Project.objects.create(
            project_name=project_title,
            project_description=project_description
        )

        # Create the Team instance
        Team.objects.create(
            member1=request.user.student_profile,
            faculty=faculty,
            project_id=project
        )

        return redirect('/project/student_dashboard')  # Replace with your success URL/view name

    else:
        faculty_members = FacultyProfile.objects.all()
        return render(request, 'auth_login/create-team.html', {'faculty_members': faculty_members})


def register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        print(form)
        if form.is_valid():
            user = form.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend' 
            students_group, created = Group.objects.get_or_create(name='Students')
            user.groups.add(students_group)
            login(request, user)
            return redirect('/auth/team_selection')  # Replace with your desired redirect URL
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
                return redirect('/project/student_dashboard')  # Redirect to student dashboard
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
                    return redirect('/project/faculty_dashboard')  # Redirect to faculty dashboard
                else:
                    print(f"User is not in Faculty group. User groups: {user.groups.all()}")
                    form.add_error(None, 'You do not have permission to access this page')
        else:
            print("Form is not valid")
            print(form.errors)
    else:
        form = FacultyLoginForm()
    return render(request, 'auth_login/faculty_login.html', {'form': form})
