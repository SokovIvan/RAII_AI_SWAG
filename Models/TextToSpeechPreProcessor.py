import pandas as pd
import pyttsx3
import time


def text_to_speech(text, output_file):
    """Функция для генерации речи и сохранения в файл."""
    engine = pyttsx3.init()  # Инициализируем движок заново для каждого файла
    engine.setProperty('rate', 150)

    # Выбираем русский голос (если доступен)
    voices = engine.getProperty('voices')
    russian_voice = None
    for voice in voices:
        if 'ru' in voice.id.lower() or 'russian' in voice.name.lower():
            russian_voice = voice.id
            break

    if russian_voice:
        engine.setProperty('voice', russian_voice)

    engine.save_to_file(str(text), output_file)
    engine.runAndWait()  # Дожидаемся завершения
    engine.stop()  # Останавливаем движок
    del engine  # Освобождаем ресурсы
    time.sleep(0.3)  # Небольшая задержка для стабильности


# Чтение Excel-файла
file_path = "L_proceed.xlsx"
df = pd.read_excel(file_path)

if 'A' in df.columns:
    for idx, text in enumerate(df['A'][:100]):  # Первые 100 строк
        if pd.isna(text):  # Пропускаем пустые значения
            continue

        print(f"{idx}: {text}")
        output_file = f"{idx}_voice.mp3"

        text_to_speech(text, output_file)
        print(f"Сохранено в {output_file}")