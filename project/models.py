from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.db import models
import PyPDF2
import requests


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

	def __str__(self):
		return self.text[:50]  # Display first 50 characters


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

		url = "https://plagiarism-source-checker-with-links.p.rapidapi.com/data"
		headers = {
			"Content-Type": "multipart/form-data",
			"x-rapidapi-host": "plagiarism-source-checker-with-links.p.rapidapi.com",
			"x-rapidapi-key": "03f37734a4mshc7064a7f2aaf43cp104d0ejsn4ba7dc3c35f5"
		}
		payload = {"text": "BMI is a measurement of a person'\''s leanness or corpulence based on their height and weight, and is intended to quantify tissue mass. It is widely used as a general indicator of whether a person has a healthy body weight for their height. Specifically, the value obtained from the calculation of BMI is used to categorize whether a person is underweight, normal weight, overweight, or obese depending on what range the value falls between. These ranges of BMI vary based on factors such as region and age, and are sometimes further divided into subcategories such as severely underweight or very severely obese. Being overweight or underweight can have significant health effects, so while BMI is an imperfect measure of healthy body weight, it is a useful indicator of whether any additional testing or action is required"}
		print(payload)

		try:
			response = requests.post(url, headers=headers, data=payload)
			self.plagiarism_result = response.json()
			print(self.plagiarism_result)
			self.save()
			pass
		except requests.exceptions.RequestException as e:
			print(f"An error occurred: {e}")
			self.plagiarism_result = {"error": str(e)}
			self.save()

	def __str__(self):
		return f"Plagiarism Check for {self.user.username} - {self.uploaded_at}"
