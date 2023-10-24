import cv2 as cv

class Camera:
    __camera = None

    def __init__(self, port):
        try:
            self.__camera = cv.VideoCapture(0)
            self.__camera.set(cv.CAP_PROP_POS_FRAMES, 200)
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
            ret, image = self.__camera.read()
            if(not ret):
                return
            
            cv.imwrite("/home/pi/Documents/projects/project-TM/temp/temp.jpeg", image)
            self.__camera.release()

        except Exception as e:
            self.__camera.release()
            print(e)
            raise Exception("Camera capture error")

