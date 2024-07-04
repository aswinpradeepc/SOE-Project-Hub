from django import forms
from .models import Project

class DocumentUploadForm(forms.Form):
    file = forms.FileField(label='Select a file')

    def clean_file(self):
        file = self.cleaned_data['file']
        # Validate file size or other constraints if needed
        return file
