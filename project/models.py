from django.db import models
from auth_login.models import StudentProfile, FacultyProfile
from django.contrib.auth.models import User


class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=255)
    project_description = models.TextField()
    abstract = models.FileField(upload_to='documents/')
    srs = models.FileField(upload_to='documents/')
    dfd = models.FileField(upload_to='documents/')
    design = models.FileField(upload_to='documents/')
    ppt = models.FileField(upload_to='documents/')
    report = models.FileField(upload_to='documents/')
    abstract_deadline = models.DateField()
    srs_deadline = models.DateField()
    dfd_deadline = models.DateField()
    design_deadline = models.DateField()
    ppt_deadline = models.DateField()
    report_deadline = models.DateField()
    abstract_marks = models.IntegerField()
    srs_marks = models.IntegerField()
    dfd_marks = models.IntegerField()
    design_marks = models.IntegerField()
    ppt_marks = models.IntegerField()
    report_marks = models.IntegerField()
    grade = models.CharField(max_length=10)
    total_marks = models.IntegerField()

    def __str__(self):
        return self.project_name
    
class Team(models.Model):
    member1 = models.ForeignKey(StudentProfile, related_name='team_member1', on_delete=models.CASCADE)
    member2 = models.ForeignKey(StudentProfile, related_name='team_member2', on_delete=models.CASCADE, blank=True, null=True)
    member3 = models.ForeignKey(StudentProfile, related_name='team_member3', on_delete=models.CASCADE, blank=True, null=True)
    member4 = models.ForeignKey(StudentProfile, related_name='team_member4', on_delete=models.CASCADE, blank=True, null=True)
    faculty = models.ForeignKey(FacultyProfile, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return f'Team for Project {self.project_id}'

    class Meta:
        unique_together = ('project_id',)