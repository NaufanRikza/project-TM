import cv2 as cv
import time
import subprocess

class Camera:
    __camera = None
    __port = None
    def __init__(self, port):
        try:
            self.__port = port
            print("camera opened")
        except Exception as e:
            print(e)
            raise Exception("Camera initialization error")
        
    def openCamera(self):
        try:
            while True:
                ret, image = self.__camera.read()
                if not ret:
                    return

                cv.imshow('video', image)

                key = cv.waitKey(1)
                if key == 27:
                    break

            self.__camera.release()
            cv.destroyAllWindows()

        except Exception as e:
            self.__camera.release()
            print(e)
            raise Exception("Camera capture error")

    
    def capture(self):
        try:
            # self.__camera = cv.VideoCapture("/dev/video0")
            # time.sleep(0.8)
            # ret, image = self.__camera.read()
            # if not ret:
            #     print("capture failed")
            #     return False
            
            # cv.imwrite("/home/pi/Documents/project/project-TM/temp/temp1.jpeg", image)
            res = subprocess.run(["sudo","fswebcam","-r","640x480","--no-banner","--jpeg","95","-S","50","/home/pi/Documents/project/project-TM/temp/temp1.jpeg"])
            print(res)
            print("capture success")
            return True
        except Exception as e:
            print(e)
            return False

