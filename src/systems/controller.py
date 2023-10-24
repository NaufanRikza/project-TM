from systems.camera import Camera
from systems.client import Client
from systems.positioner import Positioner
from systems.waterDripper import WaterDripper
from systems.button import Button
from systems.led import Led
import RPi.GPIO as GPIO
from data.constant import Pins

class Controller:
    __camera = None
    __client = None
    __positioner = None
    __WaterDripper = None
    __startButton = None
    __ledIndicator = None

    def __init__(self) -> None:
        GPIO.setmode(GPIO.BCM)
        self.__client = Client("http://192.168.1.1")
        self.__camera = Camera(Pins.CAMERA_PORT)
        # self.__positioner = Positioner(Pins.SERVO_1, Pins.SERVO_2, Pins.SERVO_3)
        # self.__WaterDripper = WaterDripper(Pins.MOTOR_CONTROLLER_IN1, Pins.MOTOR_CONTROLLER_IN2)
        # self.__startButton = Button(Pins.START_BUTTON)
        # self.__ledIndicator = Led(Pins.LED_PORT)

    def checkConnection(self) -> bool:
        if self.__client.ping():
            print("internet connection detected")
        else:
            print("internet connection not detected")
            while True:
                pass

    def handle(self):
        # self.checkConnection()
        self.__camera.capture()


