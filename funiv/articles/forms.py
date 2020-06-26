from django import forms
from upload.models import Document

class DocumentUpdateForm(forms.ModelForm):

    class Meta:
        model = Document
        fields = ['upload', 'title', 'content', 'thumbnail', 'category', ]
