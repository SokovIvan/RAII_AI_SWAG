from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings
from .ModelsAI.ModelsUsage import ModelsUsage
import uuid

# Создаем единственный экземпляр ModelsUsage
models_processor = ModelsUsage()


def home(request):
    return render(request, "index.html")


def upload(request):
    return render(request, "upload_sound.html")


@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        # Обработка текстового ввода
        if 'title' in request.POST and request.POST['title'].strip():
            text = request.POST['title'].strip()
            try:
                result = models_processor.process_text(text)
                return JsonResponse({
                    'status': 'success',
                    'result': result
                })
            except Exception as e:
                return JsonResponse({
                    'status': 'error',
                    'message': str(e)
                }, status=500)

        # Обработка аудиофайла
        elif request.FILES.get('audio_file'):
            audio_file = request.FILES['audio_file']

            # Генерируем уникальное имя файла
            file_ext = os.path.splitext(audio_file.name)[1]
            file_name = f"{uuid.uuid4()}{file_ext}"
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)

            # Создаем директорию MEDIA_ROOT, если она не существует
            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

            # Сохраняем файл
            with open(file_path, 'wb+') as destination:
                for chunk in audio_file.chunks():
                    destination.write(chunk)

            # Обрабатываем файл
            try:
                result = models_processor.process_voice_file(file_path)

                # Удаляем временный файл после обработки
                if os.path.exists(file_path):
                    os.remove(file_path)

                return JsonResponse({
                    'status': 'success',
                    'result': result
                })
            except Exception as e:
                # Удаляем файл в случае ошибки
                if os.path.exists(file_path):
                    os.remove(file_path)
                return JsonResponse({
                    'status': 'error',
                    'message': str(e)
                }, status=500)

    return JsonResponse({
        'status': 'error',
        'message': 'Необходимо загрузить аудиофайл или ввести текстовую заявку'
    }, status=400)