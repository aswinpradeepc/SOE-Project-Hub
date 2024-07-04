from django.shortcuts import render
from .models import Project, Team

# def student_dashboard(request):
#     project_id = 1
#     project = Project.objects.get(project_id=project_id)
#     team = Team.objects.get(project_id=project)
#     team_members = [team.member1, team.member2, team.member3, team.member4]
#     print(team,project)
#     faculty = team.faculty

#     context = {
#         'project': project,
#         'team_members': team_members,
#         'faculty': faculty,
#         'project_id': project_id
#     }
#     return render(request, 'project/project_dashboard.html', context)

def student_dashboard(request):
    project_id = 1
    project = Project.objects.get(project_id=project_id)
    team = Team.objects.get(project_id=project)
    
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
    return render(request, 'project/project_dashboard.html', context)