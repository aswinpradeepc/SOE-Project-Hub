from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import StudentProfile
from django.contrib.auth.models import Group

class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    register_number = forms.CharField(max_length=20, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'register_number', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            student_profile = StudentProfile(user=user, reg_number=self.cleaned_data['register_number'])
            student_profile.save()
            user.groups.add(Group.objects.get(name='Students'))
        return user

class FacultyLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email', 'required': 'required'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'required': 'required'}))

class StudentLoginForm(forms.Form):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email', 'required': 'required'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'required': 'required'}))
