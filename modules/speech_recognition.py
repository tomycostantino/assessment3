import speech_recognition as sr


class Speech2Text:
    def __init__(self):
        self._sr = sr.Recognizer()

    def transform2text(self, filename: str):
        file = open(filename, mode='rb')
        audio = sr.AudioFile(file)

        with audio as source:
            audio = self._sr.record(source)
            transcription = self._sr.recognize_google(audio)
            return transcription
