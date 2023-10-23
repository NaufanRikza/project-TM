from Camera import Camera
from Client import Client
from Positioner import Positioner
from WaterDripper import WaterDripper
from Button import Button
import RPi.GPIO as GPIO
from data.constant import Pins

class Controller:
    __camera = None
    __client = None
    __positioner = None
    __WaterDripper = None
    __startButton = None

    def __init__(self) -> None:
        GPIO.setmode(GPIO.BCM)
        self.__camera = Camera()
        self.__client = Client()
        self.__positioner = Positioner(Pins.SERVO_1, Pins.SERVO_2, Pins.SERVO_3)
        self.__WaterDripper = WaterDripper(Pins.MOTOR_CONTROLLER_IN1, Pins.MOTOR_CONTROLLER_IN2)
        self.__startButton = Button(Pins.START_BUTTON)


