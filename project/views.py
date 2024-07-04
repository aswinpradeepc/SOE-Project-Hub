from django.shortcuts import render, get_object_or_404
from .models import Project, Team
from django.contrib.auth.decorators import login_required

@login_required
def student_dashboard(request):

    student_profile = request.user.student_profile

    # Find the team where the student is a member
    team = get_object_or_404(Team, member1=student_profile)

    # Access the project through the team
    project_id = team.project_id

    project = Project.objects.get(project_name=project_id)
    
    # Process team members and faculty
    team_members = [
        str(member).replace(' - Student', '') for member in [team.member1, team.member2, team.member3, team.member4] 
        if member is not None
    ]
    faculty_name = str(team.faculty).replace(' - Faculty', '')

    # Prepare submission documents
    submission_documents = [
        {'name': 'Abstract', 'file': project.abstract, 'deadline': project.abstract_deadline},
        {'name': 'SRS', 'file': project.srs, 'deadline': project.srs_deadline},
        {'name': 'DFD', 'file': project.dfd, 'deadline': project.dfd_deadline},
        {'name': 'Design', 'file': project.design, 'deadline': project.design_deadline},
        {'name': 'PPT', 'file': project.ppt, 'deadline': project.ppt_deadline},
        {'name': 'Report', 'file': project.report, 'deadline': project.report_deadline},
    ]

    context = {
        'project': project,
        'team_members': team_members,
        'faculty': faculty_name,
        'project_id': project_id,
        'submission_documents': submission_documents,
    }
    return render(request, 'project/student_dashboard.html', context)


from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from .models import Project
from .forms import DocumentUploadForm

def upload_document(request, project_id, document):
    # Fetch the project based on project_id
    project = get_object_or_404(Project, project_id=project_id)

    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded file to the respective document field
            uploaded_file = form.cleaned_data['file']
            if document == 'abstract':
                project.abstract = uploaded_file
                project.save()
            elif document == 'srs':
                project.srs = uploaded_file
                project.save()
            elif document == 'dfd':
                project.dfd = uploaded_file
                project.save()
            elif document == 'design':
                project.design = uploaded_file
                project.save()
            elif document == 'ppt':
                project.ppt = uploaded_file
                project.save()
            elif document == 'report':
                project.report = uploaded_file
                project.save()
            
            messages.success(request, f"{document.capitalize()} uploaded successfully!")
            return redirect(reverse('student_dashboard'))  # Replace with your dashboard URL name
        else:
            messages.error(request, "Error uploading the document. Please try again.")
    else:
        form = DocumentUploadForm()

    context = {
        'form': form,
        'project': project,
        'document_name': document.capitalize(),
    }
    return render(request, 'project/document_upload.html', context)
