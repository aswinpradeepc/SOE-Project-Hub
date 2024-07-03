from django.db import models
from django.contrib.auth.models import User

class FacultyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='faculty_profile')
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    dept = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='faculty_photos/')
    team_count = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(4)])

    def __str__(self):
        return f'{self.user.username} - Faculty'

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    reg_number = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.user.username} - Student'
