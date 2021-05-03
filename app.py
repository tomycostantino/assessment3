from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog
from tkinter import *
import cv2 #It does the face recognition
import numpy as np
import speech_recognition as sr #It does speech recognition
from time import sleep

"""This class is in charge of doing the face recognition process"""
class FaceRecognition:
    def __init__(self):
        pass

    def __del__(self):
        pass

    """
    Core function of the class
    It'll do the face recognition and create a a window that displays the camera
    and makes a rectangle where it detects a face
    """
    def camera_recognition(self):
        #object that allows to capture the video
        cap = cv2.VideoCapture(0)
        #Use cascade classifier from OpenCv so create the correspondent object
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        #Loop until ESC key is pressed
        while True:
            #read the camera, it returns a tuple
            ret, img = cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            #Loop to create the rectangle on faces
            for (x,y,w,h) in faces:
                cv2.rectangle(img, (x,y), (x+w, y+h), (0, 255, 0), 2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = img[y:y+h, x:x+w]

            #Display live camera and rectangle if any face was detected
            cv2.imshow('Live camera (PRESS ESC TO EXIT)', img)

            #Check for ESC key to stop the recognition
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break
        cap.release()
        cv2.destroyAllWindows()

"""Do the transcription from speech to text"""
class Speech2Text:
    def __init__(self):
        self.r = sr.Recognizer()
        self.audio = ''
    def __del__(self):
        pass

    #this function makes easier the comunication with the GUI by returning
    #the translation so it can be stored in a StringVar() later
    """Main function that interacts with the API"""
    def speech2text(self):
        with sr.Microphone() as source:
            self.r.adjust_for_ambient_noise(source)
            self.audio = self.r.listen(source)
            #Open microphone and start recording
            try:
                transcription = self.r.recognize_google(self.audio)
                return transcription

            except Exception as e:
                error = "Error please try again" + str(e)
                return error

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.talk = tk.StringVar()
        self.speechToText = tk.StringVar()  #This value will change every time we use speech to text
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.start_talking = tk.Button(self)
        self.start_talking["text"] = "Speech to text"
        self.start_talking["command"] = self.convert_into_text
        self.start_talking.pack(side="top")

        self.say_something= tk.Label(self)
        self.say_something["textvariable"] = self.talk
        self.say_something.pack(side="top")

        self.final_transcription = tk.Label(self)
        self.final_transcription["textvariable"] = self.speechToText
        self.final_transcription.pack(side="top")

        self.clear_speech = tk.Button(self)
        self.clear_speech['text'] = 'Clear'
        self.clear_speech['command'] = self.clear_words
        self.clear_speech.pack(side='top')

        self.open_camera = tk.Button(self)
        self.open_camera["text"] = "Face recognition"
        self.open_camera["command"] = self.face_recognition
        self.open_camera.pack(side="top")

        self.quit = tk.Button(self, text="QUIT APPLICATION", fg="red",command=self.master.destroy)
        self.quit.pack(side="bottom")

    def convert_into_text(self):
        transcription = Speech2Text()
        self.talk.set("Say something")
        self.update()
        self.speechToText.set('You said: ' + transcription.speech2text())

    def face_recognition(self):
        faces = FaceRecognition()
        faces.camera_recognition()

    def clear_words(self):
        self.talk.set('')
        self.speechToText.set('')

root = tk.Tk()
root.geometry("350x180")
app = App(master=root)
app.mainloop()
