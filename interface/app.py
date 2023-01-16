import tkinter as tk    #GUI library

from interface.file_s2t import FileSpeech2Text
from interface.live_s2t import LiveSpeech2Text
from modules.face_recognition import FaceRecognition


class App(tk.Tk):
    """Constructor for class"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_widgets()

    """Here I'll define the widgets to use and it is called when the app is started"""
    def create_widgets(self):
        """This button will do the speech recognition with the microphone"""
        live_s2t = tk.Button(self, fg='black', width=25, padx=5, pady=10)
        live_s2t["text"] = "Speech to text with microphone"
        live_s2t["command"] = self.speech2text_mic
        live_s2t.pack()

        """This button will do the speech recognition with the audiofile chosen"""
        file_s2t = tk.Button(self, fg='black', width=25, padx=5, pady=10)
        file_s2t["text"] = "Speech to text with audiofile"
        file_s2t["command"] = self.speech2text_file
        file_s2t.pack()

        """This button will call the function in charge of the face detection with the camera"""
        live_face_det = tk.Button(self, fg='black', width=25, padx=5, pady=10)
        live_face_det["text"] = "Face recognition with live camera"
        live_face_det["command"] = self.face_recognition_camera
        live_face_det.pack()

        """This button will call the function in charge of the face detection with the photo"""
        file_face_det = tk.Button(self, fg='black', width=25, padx=5, pady=10)
        file_face_det["text"] = "Face recognition select image"
        file_face_det["command"] = self.face_recognition_file
        file_face_det.pack()

        """This is a handy button for the user to exit the app in a simple way"""
        self.quit = tk.Button(self, text="QUIT APPLICATION", fg="red", command=self.destroy)
        self.quit.pack()

    """Function that prints on the screen when to say something and then the translation
    of what the user has said"""
    def speech2text_mic(self):
        popup = LiveSpeech2Text(self)
        popup.wm_title('Speech to text with microphone')

    """Function that prints on the screen what the audio input said"""
    def speech2text_file(self):
        popup = FileSpeech2Text(self)
        popup.wm_title('Speech to text with file')

    """
    Does the face recognition and create a a window that displays the camera
    and makes a rectangle where it detects a face
    """
    def face_recognition_camera(self):
        face_recognizer = FaceRecognition()
        face_recognizer.face_recognition_live()

    """
    Does the face recognition and create a a window that displays the file chosen
    and makes a rectangle on the face
    """
    def face_recognition_file(self):
        face_recognizer = FaceRecognition()
        face_recognizer.face_recognition_file()
