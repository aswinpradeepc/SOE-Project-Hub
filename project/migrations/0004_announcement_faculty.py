# Generated by Django 5.0.6 on 2024-07-06 09:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_login', '0004_studentprofile_project_id'),
        ('project', '0003_announcement'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcement',
            name='faculty',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='auth_login.facultyprofile'),
            preserve_default=False,
        ),
    ]
