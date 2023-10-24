import RPi.GPIO as GPIO

class Led:
    __port = None
    __inverted = None
    def __init__(self, port, inverted=False) -> None:
        try:
            self.__port = port
            self.__inverted = inverted
            GPIO.setup(port, GPIO.OUT)
        except Exception as e:
            print(e)
            raise Exception("Led initialization error");

    def on(self):
        if self.__inverted:
            GPIO.output(self.__port, GPIO.LOW)
        else:
            GPIO.output(self.__port, GPIO.HIGH)

    def off(self):
        if self.__inverted:
            GPIO.output(self.__port, GPIO.HIGH)
        else:
            GPIO.output(self.__port, GPIO.LOW)