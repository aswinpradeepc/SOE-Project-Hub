from django import forms
from .models import SupportTicket

class SupportTicketForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control w-100', 'cols': 30, 'rows': 9, 'placeholder': 'Enter Message'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email address'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Subject'}),
        }
