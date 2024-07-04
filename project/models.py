from django.db import models
from auth_login.models import StudentProfile, FacultyProfile

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
