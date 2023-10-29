import RPi.GPIO as GPIO
import time


class WaterDripper:
    __in1 = None
    __in2 = None

    def __init__(self, in1, in2) -> None:
        try:
            self.__in1 = in1
            self.__in2 = in2
            GPIO.setup(self.__in2, GPIO.OUT)
            GPIO.setup(self.__in1, GPIO.OUT)
            GPIO.output(self.__in1, GPIO.LOW)
            GPIO.output(self.__in2, GPIO.LOW)
        except Exception as e:
            print(e)
            raise Exception("Water Dripper initialing error")

    def startDrip(self):
        try:
            GPIO.output(self.__in1, GPIO.HIGH)
            GPIO.output(self.__in2, GPIO.LOW)
        except Exception as e:
            print(e)
            raise Exception("Water Dripper start drip error")

    def stopDrip(self):
        try:
            GPIO.output(self.__in1, GPIO.LOW)
            GPIO.output(self.__in2, GPIO.LOW)
        except Exception as e:
            print(e)
            raise Exception("Water Dripper stop drip error")

    def dripTiming(self):
        try:
            self.startDrip()
            time.sleep(0.07)
            self.stopDrip()
        except Exception as e:
            print(e)
            raise Exception("Water Dripper drip timer drip error")
