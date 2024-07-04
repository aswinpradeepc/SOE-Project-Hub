# Generated by Django 5.0.6 on 2024-07-04 09:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth_login', '0003_alter_facultyprofile_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('project_id', models.AutoField(primary_key=True, serialize=False)),
                ('project_name', models.CharField(max_length=255)),
                ('project_description', models.TextField()),
                ('abstract', models.FileField(upload_to='documents/')),
                ('srs', models.FileField(upload_to='documents/')),
                ('dfd', models.FileField(upload_to='documents/')),
                ('design', models.FileField(upload_to='documents/')),
                ('ppt', models.FileField(upload_to='documents/')),
                ('report', models.FileField(upload_to='documents/')),
                ('abstract_deadline', models.DateField()),
                ('srs_deadline', models.DateField()),
                ('dfd_deadline', models.DateField()),
                ('design_deadline', models.DateField()),
                ('ppt_deadline', models.DateField()),
                ('report_deadline', models.DateField()),
                ('abstract_marks', models.IntegerField()),
                ('srs_marks', models.IntegerField()),
                ('dfd_marks', models.IntegerField()),
                ('design_marks', models.IntegerField()),
                ('ppt_marks', models.IntegerField()),
                ('report_marks', models.IntegerField()),
                ('grade', models.CharField(max_length=10)),
                ('total_marks', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth_login.facultyprofile')),
                ('member1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_member1', to='auth_login.studentprofile')),
                ('member2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_member2', to='auth_login.studentprofile')),
                ('member3', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_member3', to='auth_login.studentprofile')),
                ('member4', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_member4', to='auth_login.studentprofile')),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.project')),
            ],
            options={
                'unique_together': {('project_id',)},
            },
        ),
    ]