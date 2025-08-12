from django.shortcuts import render, redirect
from .forms import AudioUploadForm
import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.contrib import messages
from .utils import process

def upload_audio(request):
    if request.method == 'POST':
        form = AudioUploadForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, "processing/error_upload.html")
        audio_file = request.FILES['audio_file']
        file_name = default_storage.save(
            f'audio_uploads/{os.path.basename(audio_file.name)}',
            audio_file
        )
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        process(file_path)
    else:
        render(request, "processing/upload.html")
    
def index(request):
    return render(request, "processing/index.html")