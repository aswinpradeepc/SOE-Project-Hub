# myapp/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import StudentProfile, FacultyProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.groups.filter(name='Students').exists():
            StudentProfile.objects.create(user=instance)
        elif instance.groups.filter(name='Faculty').exists():
            FacultyProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.groups.filter(name='Students').exists():
        instance.student_profile.save()
    elif instance.groups.filter(name='Faculty').exists():
        instance.faculty_profile.save()
