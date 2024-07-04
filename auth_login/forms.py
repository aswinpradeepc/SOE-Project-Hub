from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import StudentProfile
from django.contrib.auth.models import Group

class StudentRegistrationForm(UserCreationForm):
    DEPARTMENT_CHOICES = [
        ('CS', 'Computer Science'),
        ('IT', 'Information Technology'),
        ('EEE', 'Electrical and Electronics Engineering'),
        ('SFE', 'Safety Engineering'),
        ('ECE', 'Electronics and Communication Engineering'),
        ('ME', 'Mechanical Engineering'),
        ('CE', 'Civil Engineering'),
    ]

    email = forms.EmailField(required=True)
    register_number = forms.CharField(max_length=20)
    dept = forms.ChoiceField(choices=DEPARTMENT_CHOICES, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'register_number', 'dept')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            student_profile = StudentProfile(user=user, reg_number=self.cleaned_data['register_number'], dept=self.cleaned_data['dept'])
            student_profile.save()
        return user

class StudentLoginForm(forms.Form):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email', 'required': 'required'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'required': 'required'}))

class FacultyLoginForm(forms.Form):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email', 'required': 'required'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'required': 'required'}))
