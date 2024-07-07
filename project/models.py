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

	def check_plagiarism(self, max_retries=3, initial_delay=1):
		if not self.text_content:
			self.extract_text()

		url = "https://plagiarism-source-checker-with-links.p.rapidapi.com/data"

		headers = {
			"Content-Type": "multipart/form-data",
			"x-rapidapi-host": "plagiarism-source-checker-with-links.p.rapidapi.com",
			"x-rapidapi-key": "03f37734a4mshc7064a7f2aaf43cp104d0ejsn4ba7dc3c35f5"
		}

		text = self.text_content
		data = {'text': text}

		for attempt in range(max_retries):
			try:
				response = requests.post(url, headers=headers, data=data, verify=False)
				response.raise_for_status()

				self.plagiarism_result = response.text
				print(self.plagiarism_result)
				self.save()
				return  # Success, exit the function
			except requests.exceptions.HTTPError as e:
				if e.response.status_code == 429:
					if attempt < max_retries - 1:
						delay = initial_delay * (2 ** attempt)
						print(f"Rate limit exceeded. Retrying in {delay} seconds...")
						time.sleep(delay)
					else:
						print("Max retries reached. Please try again later.")
				else:
					print(f"HTTP error occurred: {e}")
					break  # Exit for non-429 errors
			except requests.exceptions.RequestException as e:
				print(f"An error occurred: {e}")
				break  # Exit for other request exceptions


