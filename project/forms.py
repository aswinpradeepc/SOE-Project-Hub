from django import forms
from .models import Project

from django import forms
from .models import PlagiarismCheck


class DocumentUploadForm(forms.Form):
	file = forms.FileField(label='Select a file')

	def clean_file(self):
		file = self.cleaned_data['file']
		# Validate file size or other constraints if needed
		return file


class PlagiarismCheckForm(forms.ModelForm):
	class Meta:
		model = PlagiarismCheck
		fields = ['pdf_file']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['pdf_file'].widget.attrs.update({'class': 'form-control-file'})

	def clean_pdf_file(self):
		pdf_file = self.cleaned_data.get('pdf_file')
		if pdf_file:
			if not pdf_file.name.lower().endswith('.pdf'):
				raise forms.ValidationError("Only PDF files are allowed.")
			if pdf_file.size > 5 * 1024 * 1024:  # 5 MB limit
				raise forms.ValidationError("File size must be under 5 MB.")
		return pdf_file
