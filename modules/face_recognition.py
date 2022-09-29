import cv2


class FaceRecognition:
    def __init__(self):
        '''
        Initialize the face recognition module
        '''

        self._recognizer = cv2.VideoCapture(0)
        self._face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def _detect_face_live(self):
        '''
        Detects faces in live camera
        '''

        while True:
            ret, img = self._recognizer.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self._face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

            cv2.imshow('Live camera (PRESS ESC TO EXIT)', img)
