from django import forms
from django.db.models import Q

from project.models import Team
from .models import Query, Feedback


class QueryForm(forms.ModelForm):
	class Meta:
		model = Query
		fields = ['name', 'message']


	def save(self, commit=True):
		# self.instance.sender  as request.user
		team = Team.objects.filter(Q(member1=self.instance.sender.student_profile) | Q(member2=self.instance.sender.student_profile) | Q(member3=self.instance.sender.student_profile) | Q(member4=self.instance.sender.student_profile)).first()
		self.instance.recipient = team.faculty.user
		# sender a user requesting
		return super(QueryForm, self).save(commit=commit)

class FeedbackForm(forms.ModelForm):
	class Meta:
		model = Feedback
		fields = ['name', 'message']
