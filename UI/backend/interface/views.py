import tempfile

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings
from .ModelsAI.ModelsUsage import ModelsUsage
import uuid
import logging

# Настройка логгера
logger = logging.getLogger(__name__)

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

                # Форматируем результат
                formatted_result = {
                    "prompt": result["prompt"],
                    "group": result["group"],
                    "task": result["task"],
                    "critical": result["critical"],
                    "analysis": (
                        f"Заявка - {result['prompt']}\n"
                        f"Группа - {result['group']}\n"
                        f"Задача - {result['task']}\n"
                        f"Критичность - {result['critical']}"
                    )
                }

                return JsonResponse({
                    'status': 'success',
                    'result': formatted_result
                })
            except Exception as e:
                return JsonResponse({
                    'status': 'error',
                    'message': str(e)
                }, status=500)

        # Обработка аудиофайла
        elif request.FILES.get('audio_file'):
            audio_file = request.FILES['audio_file']

            # Создаем MEDIA_ROOT если не существует
            media_root = settings.MEDIA_ROOT
            os.makedirs(media_root, exist_ok=True)

            # Создаем подпапку для аудио
            audio_dir = os.path.join(media_root, 'voices')
            os.makedirs(audio_dir, exist_ok=True)

            # Генерируем уникальное имя файла
            ext = os.path.splitext(audio_file.name)[1]
            unique_filename = f"{uuid.uuid4().hex}{ext}"
            file_path = os.path.join(audio_dir, unique_filename)

            # Сохраняем файл постоянно
            with open(file_path, 'wb+') as destination:
                for chunk in audio_file.chunks():
                    destination.write(chunk)

            try:
                # Обрабатываем файл
                result = models_processor.process_voice_file(file_path)

                # Форматируем результат
                formatted_result = {
                    "prompt": result["prompt"],
                    "group": result["group"],
                    "task": result["task"],
                    "critical": result["critical"],
                    "analysis": (
                        f"Заявка - {result['prompt']}\n"
                        f"Группа - {result['group']}\n"
                        f"Задача - {result['task']}\n"
                        f"Критичность - {result['critical']}"
                    ),
                    "file_path": file_path  # Добавляем путь для отладки
                }

                return JsonResponse({
                    'status': 'success',
                    'result': formatted_result
                })
            except Exception as e:
                return JsonResponse({
                    'status': 'error',
                    'message': str(e)
                }, status=500)

    return JsonResponse({
        'status': 'error',
        'message': 'Необходимо загрузить аудиофайл или ввести текстовую заявку'
    }, status=400)