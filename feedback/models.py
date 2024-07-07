from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Feedback(models.Model):
	name = models.CharField(max_length=120)
	project = models.ForeignKey('project.Project', on_delete=models.CASCADE)
	message = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name


class Query(models.Model):
	name = models.CharField(max_length=120)
	sender = models.ForeignKey(User, on_delete=models.CASCADE,related_name='sender')
	recipient = models.ForeignKey(User, on_delete=models.CASCADE,related_name='recipient')
	message = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	reply = models.TextField(null=True, blank=True)

	def __str__(self):
		return self.name
