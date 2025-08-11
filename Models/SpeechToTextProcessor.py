import pandas as pd
from vosk import Model, KaldiRecognizer
import wave
import json
import os

# Укажите путь к модели Vosk (скачайте с https://alphacephei.com/vosk/models)
model_path = "vosk-model-small-ru-0.22"
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Модель {model_path} не найдена. Скачайте её с официального сайта.")

# Загрузка модели
model = Model(model_path)


# Функция для распознавания речи из WAV-файла
def speech_to_text(audio_path):
    # Проверяем, что файл существует
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Аудиофайл {audio_path} не найден.")
    with wave.open(audio_path, "rb") as wf:
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
            raise ValueError("Аудиофайл должен быть в формате WAV (16kHz, 16bit, mono).")
        recognizer = KaldiRecognizer(model, wf.getframerate())
        results = []
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                if "text" in result:
                    results.append(result["text"])
        final_result = json.loads(recognizer.FinalResult())
        if "text" in final_result:
            results.append(final_result["text"])
        return " ".join(results)
audio_file = "test.wav"  # Замените на ваш файл
recognized_text = speech_to_text(audio_file)
print("Распознанный текст:", recognized_text)