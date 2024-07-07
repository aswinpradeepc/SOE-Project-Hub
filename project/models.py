import time

from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.db import models
import PyPDF2
import requests
import urllib.request
import urllib.parse
import urllib.error
import ssl
from shlex import quote as shlex_quote


class Project(models.Model):
	project_id = models.AutoField(primary_key=True)
	project_name = models.CharField(max_length=255)
	project_description = models.TextField()

	abstract = models.FileField(upload_to='documents/', null=True, blank=True)
	srs = models.FileField(upload_to='documents/', null=True, blank=True)
	dfd = models.FileField(upload_to='documents/', null=True, blank=True)
	design = models.FileField(upload_to='documents/', null=True, blank=True)
	ppt = models.FileField(upload_to='documents/', null=True, blank=True)
	report = models.FileField(upload_to='documents/', null=True, blank=True)

	abstract_deadline = models.DateField(null=True, blank=True)
	srs_deadline = models.DateField(null=True, blank=True)
	dfd_deadline = models.DateField(null=True, blank=True)
	design_deadline = models.DateField(null=True, blank=True)
	ppt_deadline = models.DateField(null=True, blank=True)
	report_deadline = models.DateField(null=True, blank=True)

	abstract_marks = models.IntegerField(null=True, blank=True)
	srs_marks = models.IntegerField(null=True, blank=True)
	dfd_marks = models.IntegerField(null=True, blank=True)
	design_marks = models.IntegerField(null=True, blank=True)
	ppt_marks = models.IntegerField(null=True, blank=True)
	report_marks = models.IntegerField(null=True, blank=True)

	grade = models.CharField(max_length=10, null=True, blank=True)
	total_marks = models.IntegerField(null=True, blank=True)

	def __str__(self):
		return self.project_name


class Team(models.Model):
	member1 = models.ForeignKey('auth_login.StudentProfile', related_name='team_member1', on_delete=models.CASCADE)
	member2 = models.ForeignKey('auth_login.StudentProfile', related_name='team_member2', on_delete=models.CASCADE,
	                            blank=True, null=True)
	member3 = models.ForeignKey('auth_login.StudentProfile', related_name='team_member3', on_delete=models.CASCADE,
	                            blank=True, null=True)
	member4 = models.ForeignKey('auth_login.StudentProfile', related_name='team_member4', on_delete=models.CASCADE,
	                            blank=True, null=True)

	faculty = models.ForeignKey('auth_login.FacultyProfile', on_delete=models.CASCADE)
	project_id = models.ForeignKey(Project, on_delete=models.CASCADE)

	def __str__(self):
		return f'Team for Project {self.project_id}'

	class Meta:
		unique_together = ('project_id',)


class Announcement(models.Model):
	text = models.TextField()
	faculty = models.ForeignKey('auth_login.FacultyProfile', on_delete=models.CASCADE)


class PlagiarismCheck(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	pdf_file = models.FileField(upload_to='pdfs/')
	uploaded_at = models.DateTimeField(auto_now_add=True)
	text_content = models.TextField(blank=True)
	plagiarism_result = models.JSONField(null=True, blank=True)

	def extract_text(self):
		if self.pdf_file:
			with default_storage.open(self.pdf_file.name, 'rb') as pdf_file:
				pdf_reader = PyPDF2.PdfReader(pdf_file)
				text = ""
				for page in pdf_reader.pages:
					text += page.extract_text()
				self.text_content = text
				# replace and \n and all special characters with space
				self.text_content = " ".join(self.text_content.split())

				self.save()

	def check_plagiarism(self):
		if not self.text_content:
			self.extract_text()

		import os
		import requests

		url = "https://plagiarism-source-checker-with-links.p.rapidapi.com/data"

		payload = f"-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"text\"\r\n\r\n{self.text_content}\r\n-----011000010111000001101001--\r\n\r\n"
		headers = {
			"x-rapidapi-key": "d584ae3964msha8907f7375aa1e6p1176c8jsn20345a9bc6cc",
			"x-rapidapi-host": "plagiarism-source-checker-with-links.p.rapidapi.com",
			"Content-Type": "multipart/form-data; boundary=---011000010111000001101001"
		}

		response = requests.post(url, data=payload, headers=headers)

		print(response.json())
		self.plagiarism_result = response.json()



