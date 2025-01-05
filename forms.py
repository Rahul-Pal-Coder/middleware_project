from django import forms
from .models import XMLData

class XMLUploadForm(forms.ModelForm):
    class Meta:
        model = XMLData
        fields = ['xml_content']
