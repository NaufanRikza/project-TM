import RPi.GPIO as GPIO
class Positioner :
    __servo1 = None
    __servo2 = None
    __servo3 = None

    def __init__(self, servo1, servo2, servo3) -> None:
        try:
            self.__servo1 = servo1
            self.__servo2 = servo2
            self.__servo3 = servo3

            GPIO.setup(self.__servo1, GPIO.OUT)
            GPIO.setup(self.__servo2, GPIO.OUT)
            GPIO.setup(self.__servo3, GPIO.OUT)
        except Exception as e:
            raise Exception("Positioner initialize error")