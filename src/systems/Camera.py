from cv2 import *

class Camera:
    __camera = None

    def __init__(self, port):
        try:
            self.__camera = VideoCapture(port)
        except Exception as e:
            print(e)
            raise Exception("Camera initialization error")
    
    def cameraCapture(self):
        try:
            ret, image = self.__camera.read()

