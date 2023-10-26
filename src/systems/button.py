import RPi.GPIO as GPIO

class Button:
    __pin = None
    def __init__(self, pin) -> None:
        try:
            self.__pin = pin
            GPIO.setup(self.__pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        except Exception as e:
            print(e)
            raise Exception("Button initilizing failed at pin {0} ".format(self.__pin))

    def isClicked(self):
        try:
            return GPIO.input(self.__pin)
        except Exception as e:
            print(e)
            raise Exception("Read button error")
