from django import forms
from .models import AttachedFile

class AttachedFileForm(forms.ModelForm):
    class Meta:
        model = AttachedFile
        fields = ['file']