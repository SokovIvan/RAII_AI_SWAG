from django import forms
from django.core.validators import FileExtensionValidator

class AudioUploadForm(forms.Form):
    audio_file = forms.FileField(
        label='',
        validators=[FileExtensionValidator(allowed_extensions=['mp3', 'wav', 'ogg', 'm4a'])],
        widget=forms.FileInput(attrs={
            'accept': 'audio/*',
            'class': 'form-control',
            'required': True
        })
    )