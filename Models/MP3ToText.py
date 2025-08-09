from vosk import Model, KaldiRecognizer
import subprocess
import json

class SpeechToTextProcessor:
    def __init__(self):
        self.model = Model("vosk-model-small-ru-0.22\\vosk-model-small-ru-0.22")
    def speech_to_text(self,file_path):
        # Необходимо установить ffmpeg
        command = [
            "ffmpeg-7.1.1-essentials_build/bin/ffmpeg.exe", "-i", f"{file_path}",
            "-ar", "16000", "-ac", "1", "-f", "s16le", "-"
        ]
        process = subprocess.Popen(command, stdout=subprocess.PIPE)
        recognizer = KaldiRecognizer(self.model, 16000)
        while True:
            data = process.stdout.read(4000)
            if len(data) == 0:
                break
            if recognizer.AcceptWaveform(data):
                print(json.loads(recognizer.Result())["text"])
        return json.loads(recognizer.FinalResult())["text"]
#Пример
if __name__ == '__main__':
    spTp = SpeechToTextProcessor()
    spTp.speech_to_text("voices/0_voice.mp3")