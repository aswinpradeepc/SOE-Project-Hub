from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from project.models import Project
from .models import Query, Feedback
from .forms import QueryForm, FeedbackForm
from django.contrib import messages


@login_required
def queries_feedback_view(request):
	queries = Query.objects.filter(sender=request.user).order_by('-created_at')
	feedbacks = Feedback.objects.filter().order_by('-created_at')

	if request.method == 'POST':
		if 'query_submit' in request.POST:
			query_form = QueryForm(request.POST)
			query_form.instance.sender = request.user
			if query_form.is_valid():
				query = query_form.save(commit=False)
				query.save()
				messages.success(request, 'Query submitted successfully!')
				return redirect('queries_feedback')
		elif 'feedback_submit' in request.POST:
			feedback_form = FeedbackForm(request.POST)
			if feedback_form.is_valid():
				feedback_form.save()
				messages.success(request, 'Feedback submitted successfully!')
				return redirect('queries_feedback')

	query_form = QueryForm()
	feedback_form = FeedbackForm()

	context = {
		'queries': queries,
		'feedbacks': feedbacks,
		'query_form': query_form,
		'feedback_form': feedback_form,
	}

	return render(request, 'feedback/queries_feedback.html', context)


@login_required
def faculty_dashboard(request, pk):
	queries = Query.objects.all().order_by('-created_at')
	feedbacks = Feedback.objects.all().order_by('-created_at')
	query_form = QueryForm()
	feedback_form = FeedbackForm()

	if request.method == 'POST':
		feedback_form = FeedbackForm(request.POST)
		project = get_object_or_404(Project, project_id=pk)
		if feedback_form.is_valid():
			feedback = feedback_form.save(commit=False)
			feedback.user = request.user
			feedback.project = project
			feedback.save()
			messages.success(request, 'Feedback submitted successfully.')
			return redirect('faculty_dashboard')

	context = {
		'queries': queries,
		'feedbacks': feedbacks,
		'query_form': query_form,
		'feedback_form': feedback_form,
		'is_faculty': True,
		'pk': pk
	}
	return render(request, 'feedback/queries_feedback.html', context)


@login_required
def reply_to_query(request, pk):
	query = get_object_or_404(Query, id=pk)
	if request.method == 'POST':
		query.reply = request.POST.get('reply')
		query.save()
		messages.success(request, 'Reply sent successfully.')
	return redirect('faculty_feedback')

