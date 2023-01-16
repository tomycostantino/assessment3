import cv2
from tkinter import filedialog


class FaceRecognition:
    def __init__(self):
        pass

    def face_recognition_live(self):
        cap = cv2.VideoCapture(0)   # object that captures the live camera

        """Use cascade classifier from OpenCv so create the correspondent object"""
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        """Now loop until ESC is pressed, this will exit the live camera"""
        while True:
            ret, img = cap.read()   # read the camera, it returns a tuple
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            """Loop to create the rectangle on faces"""
            for (x, y, w, h) in faces:
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
        cv2.destroyAllWindows() # Closes the window

    def face_recognition_file(self):
        file = filedialog.askopenfilename() # Returns the name of the file
        img = cv2.imread(file)  # Reads the image

        # Use cascade classifier from OpenCv so create the correspondent object
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # read the camera, it returns a tuple
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # Loop to create the rectangle on faces
        for (x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w, y+h), (0, 255, 0), 2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]

        # Display live camera and rectangle if any face was detected
        cv2.imshow('PRESS ESC TO EXIT', img)
        # Loop until ESC key is pressed
        while True:
            # Check for ESC key to stop the recognition
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break
        cv2.destroyAllWindows()

