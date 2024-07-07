from .models import Project, Team, Announcement
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import DocumentUploadForm
from auth_login.models import FacultyProfile
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import PlagiarismCheck
from .forms import PlagiarismCheckForm


@login_required
def student_dashboard(request):
	student_profile = request.user.student_profile
	team = Team.objects.filter(Q(member1=student_profile) |
	                           Q(member2=student_profile) |
	                           Q(member3=student_profile) |
	                           Q(member4=student_profile)).first()
	project = team.project_id

	team_members = [
		str(member).replace(' - Student', '') for member in [team.member1, team.member2, team.member3, team.member4]
		if member is not None
	]
	faculty_name = str(team.faculty).replace(' - Faculty', '')

	submission_documents = [
		{'name': 'abstract', 'file': project.abstract, 'deadline': project.abstract_deadline,
		 'marks': project.abstract_marks},
		{'name': 'srs', 'file': project.srs, 'deadline': project.srs_deadline, 'marks': project.srs_marks},
		{'name': 'dfd', 'file': project.dfd, 'deadline': project.dfd_deadline, 'marks': project.dfd_marks},
		{'name': 'design', 'file': project.design, 'deadline': project.design_deadline, 'marks': project.design_marks},
		{'name': 'ppt', 'file': project.ppt, 'deadline': project.ppt_deadline, 'marks': project.ppt_marks},
		{'name': 'report', 'file': project.report, 'deadline': project.report_deadline, 'marks': project.report_marks},
	]

	context = {
		'project': project,
		'team_members': team_members,
		'faculty': faculty_name,
		'submission_documents': submission_documents,
		'project_id': project.project_id,
	}
	return render(request, 'project/student_dashboard.html', context)


@login_required
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


@login_required
def faculty_dashboard(request):
	faculty = FacultyProfile.objects.get(user=request.user)
	teams = Team.objects.filter(faculty=faculty)
	announcements = Announcement.objects.all()
	context = {
		'faculty_name': faculty.user.username,
		'teams': teams,
		'announcements': announcements,
	}
	return render(request, 'project/faculty_dashboard.html', context)


def make_announcement(request):
	if request.method == 'POST':
		text = request.POST['announcement_text']
		Announcement.objects.create(text=text)
	return redirect('faculty_dashboard')


def upload_document(request, project_id, document):
	project = get_object_or_404(Project, pk=project_id)
	if request.method == 'POST' and 'file' in request.FILES:
		file = request.FILES['file']
		if document in ['abstract', 'srs', 'dfd', 'design', 'ppt', 'report']:
			setattr(project, document, file)
			project.save()
			messages.success(request, f"{document.capitalize()} uploaded successfully!")
		else:
			messages.error(request, "Invalid document type.")
	else:
		messages.error(request, "No file was uploaded.")
	return redirect('student_dashboard')


def adjust_deadline(request, project_id, document):
	project = get_object_or_404(Project, pk=project_id)
	if request.method == 'POST':
		deadline = request.POST.get('deadline')
		setattr(project, f'{document}_deadline', deadline)
		project.save()
		return redirect(reverse('project_detail', args=[project_id]))
	return redirect(reverse('project_detail', args=[project_id]))


def evaluate_document(request, project_id, document):
	project = get_object_or_404(Project, pk=project_id)
	if request.method == 'POST':
		marks = request.POST.get('marks')
		setattr(project, f'{document}_marks', marks)
		project.save()
		return redirect(reverse('project_detail', args=[project_id]))
	return redirect(reverse('project_detail', args=[project_id]))


@login_required
def project_detail(request, project_id):
	project = get_object_or_404(Project, pk=project_id)
	team = Team.objects.filter(project_id=project).first()

	team_members = [
		str(member).replace(' - Student', '') for member in [team.member1, team.member2, team.member3, team.member4]
		if member is not None
	]
	submission_documents = [
		{
			'name': 'abstract',
			'file': project.abstract,
			'deadline': project.abstract_deadline,
			'marks': project.abstract_marks,
		},
		{
			'name': 'srs',
			'file': project.srs,
			'deadline': project.srs_deadline,
			'marks': project.srs_marks,
		},
		{
			'name': 'dfd',
			'file': project.dfd,
			'deadline': project.dfd_deadline,
			'marks': project.dfd_marks,
		},
		{
			'name': 'design',
			'file': project.design,
			'deadline': project.design_deadline,
			'marks': project.design_marks,
		},
		{
			'name': 'ppt',
			'file': project.ppt,
			'deadline': project.ppt_deadline,
			'marks': project.ppt_marks,
		},
		{
			'name': 'report',
			'file': project.report,
			'deadline': project.report_deadline,
			'marks': project.report_marks,
		},
	]
	context = {
		'project': project,
		'team_members': team_members,
		'submission_documents': submission_documents,
		'project_id': project_id
	}
	return render(request, 'project/project_detail.html', context)


@login_required
def adjust_deadline(request, project_id, document):
	project = get_object_or_404(Project, pk=project_id)
	if request.method == 'POST':
		deadline = request.POST.get('deadline')
		setattr(project, f'{document}_deadline', deadline)
		project.save()
		messages.success(request, f"Deadline for {document} has been updated.")
	return redirect('project_detail', project_id=project_id)


@login_required
def evaluate_document(request, project_id, document):
	project = get_object_or_404(Project, pk=project_id)
	if request.method == 'POST':
		marks = request.POST.get('marks')
		setattr(project, f'{document}_marks', marks)
		project.save()
		messages.success(request, f"Marks for {document} have been updated.")
	return redirect('project_detail', project_id=project_id)


from django.http import FileResponse
from django.shortcuts import get_object_or_404


def document_view(request, document_path):
	# Example assuming Document model has a field 'file' storing the document path
	document = get_object_or_404(Project, abstract=document_path)
	# Adjust how you fetch and serve the file based on your model and storage system
	document_file = document.file.path  # Assuming 'file' is a FileField
	return FileResponse(open(document_file, 'rb'), content_type='application/pdf')




@login_required
def upload_and_check(request):
	if request.method == 'POST':
		form = PlagiarismCheckForm(request.POST, request.FILES)
		if form.is_valid():
			plagiarism_check = form.save(commit=False)
			plagiarism_check.user = request.user
			plagiarism_check.save()

			plagiarism_check.extract_text()
			plagiarism_check.check_plagiarism()

			return redirect('plagiarism_result', pk=plagiarism_check.pk)
	return redirect("faculty_dashboard")


@login_required
def plagiarism_result(request, pk):
	plagiarism_check = PlagiarismCheck.objects.get(pk=pk)
	return render(request, 'feedback/plagiarism_result.html', {'plagiarism_check': plagiarism_check})
