from django.db import models
from django.contrib.auth.models import User

class FacultyProfile(models.Model):
    DEPARTMENT_CHOICES = [
        ('CS', 'Computer Science'),
        ('IT', 'Information Technology'),
        ('EEE', 'Electrical and Electronics Engineering'),
        ('SFE', 'Safety Engineering'),
        ('ECE', 'Electronics and Communication Engineering'),
        ('ME', 'Mechanical Engineering'),
        ('CE', 'Civil Engineering'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='faculty_profile')
    phone_number = models.CharField(max_length=15)
    dept = models.CharField(
        max_length=100,
        choices=DEPARTMENT_CHOICES,
        default='CS', 
    )
    photo = models.ImageField(upload_to='faculty_photos/')
    team_count = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(4)])

    def __str__(self):
        return f'{self.user.username} - Faculty'

    class Meta:
        verbose_name = 'Faculty Profile'
        verbose_name_plural = 'Faculty Profiles'

class StudentProfile(models.Model):
    DEPARTMENT_CHOICES = [
        ('CS', 'Computer Science'),
        ('IT', 'Information Technology'),
        ('EEE', 'Electrical and Electronics Engineering'),
        ('SFE', 'Safety Engineering'),
        ('ECE', 'Electronics and Communication Engineering'),
        ('ME', 'Mechanical Engineering'),
        ('CE', 'Civil Engineering'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    reg_number = models.CharField(max_length=20)
    dept = models.CharField(
        max_length=100,
        choices=DEPARTMENT_CHOICES,
        default='CS',  # Set a default value if necessary
    )

    def __str__(self):
        return f'{self.user.username} - Student'

    class Meta:
        verbose_name = 'Student Profile'
        verbose_name_plural = 'Student Profiles'

