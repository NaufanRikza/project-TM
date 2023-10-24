import RPi.GPIO as GPIO


class Positioner:
    __servo1 = None
    __servo2 = None
    __servo3 = None

    def __init__(self, servo1, servo2, servo3) -> None:
        try:
            GPIO.setup(servo1, GPIO.OUT)
            GPIO.setup(servo2, GPIO.OUT)
            GPIO.setup(servo3, GPIO.OUT)

            self.__servo1 = GPIO.PWM(servo1, 400)
            self.__servo2 = GPIO.PWM(servo2, 400)
            self.__servo3 = GPIO.PWM(servo3, 400)

            self.__servo1.start(60)
            self.__servo2.start(60)
            self.__servo3.start(60)

        except Exception as e:
            print(e)
            raise Exception("Positioner initialize error")

    def generatePWM(self, servo, dutycycle):
        if (servo == "servo1"):
            self.__servo1.ChangeDutyCycle(dutycycle)
        elif servo == "servo2":
            self.__servo2.ChangeDutyCycle(dutycycle)
        elif servo == "servo3":
            self.__servo3.ChangeDutyCycle(dutycycle)
        else:
            return
        pass
