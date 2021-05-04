import tkinter as tk    #GUI library
from tkinter import filedialog  #Lets me open the audiofile
from tkinter import *
import cv2 #It does the face recognition
import numpy as np
import io
import speech_recognition as sr #It does speech recognition
from time import sleep
"""
The app will be based all on this class
Here is where I declare the widgets and functions my app will perform
Inheriths from tkinter.Frame
"""
class App(tk.Frame):
    """Constructor for class"""
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.start_talk = tk.StringVar() #This will print on the screen a message for user to start talking
        self.speechToText = tk.StringVar()  #This value will change every time we use speech to text
        self.pack(expand=True, fill=BOTH)
        self.create_widgets()

    """Here I'll define the widgets to use and it is called when the app is started"""
    def create_widgets(self):

        """This button will do the speech recognition with the microphone"""
        self.mic = tk.Button(self, fg='green', padx=5, pady=5)
        self.mic["text"] = "Speech to text with microphone"
        self.mic["command"] = self.speech2textMic
        self.mic.place(x=10, y=10)

        """This button will do the speech recognition with the audiofile chosen"""
        self.audiofile = tk.Button(self, fg='blue', padx=5, pady=5)
        self.audiofile["text"] = "Speech to text with audiofile"
        self.audiofile["command"] = self.speech2textFile
        self.audiofile.place(x=250, y=10)

        """Tells the user the extension of audio to use"""
        self.reminder_audio = tk.Label(self)
        self.reminder_audio['text'] = 'Audio in .wav format'
        self.reminder_audio.place(x=290, y=43)

        """This label will print on screen when the microphone is open so user can start talking"""
        self.say_something= tk.Label(self)
        self.say_something["textvariable"] = self.start_talk
        self.say_something.place(x=100,y=50)

        """This label will print on screen the translation of the speech to text
         whether it comes from mic or audiofile"""
        self.final_transcription = tk.Label(self)
        self.final_transcription["textvariable"] = self.speechToText
        self.final_transcription.place(x=10, y=90)

        """This button allows the user to clear the screen when they already used
        speech recognition and there is something printed on screen"""
        self.clear_speech = tk.Button(self, fg='purple', padx=5, pady=5)
        self.clear_speech['text'] = 'Clear words'
        self.clear_speech['command'] = self.clear_words
        self.clear_speech.place(x=200, y=115)

        """Reminds user to clear the words before use it again"""
        self.reminder_clear = tk.Label(self)
        self.reminder_clear['text'] = 'Press clear button before use again'
        self.reminder_clear.place(x=142, y=150)

        """This button will call the function in charge of the face detection with the camera"""
        self.open_camera = tk.Button(self, fg='orange', padx=5, pady=5)
        self.open_camera["text"] = "Face recognition live camera"
        self.open_camera["command"] = self.face_recognition_camera
        self.open_camera.place(x=10,y=190)

        """This button will call the function in charge of the face detection with the photo"""
        self.open_image = tk.Button(self, fg='brown', padx=5, pady=5)
        self.open_image["text"] = "Face recognition select image"
        self.open_image["command"] = self.face_recognition_file
        self.open_image.place(x=250, y=190)

        """Tells user the extension of image to use"""
        self.reminder = tk.Label(self)
        self.reminder['text'] = 'Image must be jpg or jpeg'
        self.reminder.place(x=280, y=225)


        """This is a handy button for the user to exit the app in a simple way"""
        self.quit = tk.Button(self, text="QUIT APPLICATION", fg="red",command=self.master.destroy)
        self.quit.pack(side=BOTTOM)

    """Function that prints on the screen when to say something and then the translation
    of what the user has said"""
    def speech2textMic(self):
        r = sr.Recognizer() #Create object that will do the recognition

        with sr.Microphone() as source: #Open microphone
            r.adjust_for_ambient_noise(source)
            self.start_talk.set("Say something") #Print on screen for user to start talking
            self.update()   #Update the GUI with no need to go back to main loop
            audio = r.listen(source) #start recording

            #Use try block to check whether there has been anything said
            try:
                transcription = r.recognize_google(audio) #Do recognition
                self.speechToText.set('You said: ' + transcription) #Print on screen the transcription

            except Exception as e:
                self.speechToText.set("Error please try again" + str(e))

    """Function that prints on the screen what the audio input said"""
    def speech2textFile(self):
        r = sr.Recognizer() #Create recognizer
        file = filedialog.askopenfile(mode='rb')   #Open audiofile and assign it to variable
        audio = sr.AudioFile(file)  #Read it as an audiofile

        with audio as source:
            audio = r.record(source)    #Record what audio says, it is not the same as function .listen()
            transcription = r.recognize_google(audio) #Do the recognition
            self.start_talk.set('The file says: ')
            self.speechToText.set(transcription)    #Print on screen what the audiofile says

    """
    Does the face recognition and create a a window that displays the camera
    and makes a rectangle where it detects a face
    """
    def face_recognition_camera(self):
        cap = cv2.VideoCapture(0)   #object that captures the live camera

        """Use cascade classifier from OpenCv so create the correspondent object"""
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        """Now loop until ESC is pressed, this will exit the live camera"""
        while True:
            ret, img = cap.read()   #read the camera, it returns a tuple
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            """Loop to create the rectangle on faces"""
            for (x,y,w,h) in faces:
                cv2.rectangle(img, (x,y), (x+w, y+h), (0, 255, 0), 2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = img[y:y+h, x:x+w]

            """Display live camera and rectangle if any face was detected"""
            cv2.imshow('Live camera (PRESS ESC TO EXIT)', img)

            """Check for ESC key to stop the recognition"""
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break

        cap.release()
        cv2.destroyAllWindows() #Closes the window

    """
    Does the face recognition and create a a window that displays the file chosen
    and makes a rectangle on the face
    """
    def face_recognition_file(self):
        file = filedialog.askopenfilename() #Returns the name of the file
        img = cv2.imread(file)  #Reads the image

        #Use cascade classifier from OpenCv so create the correspondent object
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        #read the camera, it returns a tuple
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        #Loop to create the rectangle on faces
        for (x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w, y+h), (0, 255, 0), 2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]

        #Display live camera and rectangle if any face was detected
        cv2.imshow('PRESS ESC TO EXIT', img)
        #Loop until ESC key is pressed
        while True:
            #Check for ESC key to stop the recognition
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break
        cv2.destroyAllWindows()

    def clear_words(self):
        self.start_talk.set('')
        self.speechToText.set('')

root = tk.Tk() #Create the root for our app
root.geometry("500x300")    #Assign the size of the window
app = App(master=root) #Now create the app itself
app.mainloop()  #main loop where the app will run on
