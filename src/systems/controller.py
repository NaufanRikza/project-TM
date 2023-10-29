from systems.camera import Camera
from systems.client import Client
from systems.positioner import Positioner
from systems.waterDripper import WaterDripper
from systems.button import Button
from systems.led import Led
import RPi.GPIO as GPIO
from data.constant import Pins
import time
from multiprocessing import Process, Queue
from threading import Thread


class Controller:
    __camera = None
    __client = None
    __positioner = None
    __WaterDripper = None
    __startButton = None
    __ledIndicator = None
    __getCommandProcess = None
    __captureProcess = None
    __dripProcess = None
    __indicatorProcess = None

    def __init__(self) -> None:
        try:
            GPIO.setmode(GPIO.BCM)
            self.__client = Client("http://192.168.1.3:4000")
            self.__camera = Camera(Pins.CAMERA_PORT)
            self.__positioner = Positioner(
                Pins.SERVO_1, Pins.SERVO_2, Pins.SERVO_3)
            self.__WaterDripper = WaterDripper(
                Pins.MOTOR_CONTROLLER_IN1, Pins.MOTOR_CONTROLLER_IN2)
            self.__startButton = Button(Pins.START_BUTTON)
            self.__ledIndicator = Led(Pins.LED_PORT)

            self.__getCommandProcess = Thread(
                target=self.getCommandHandle)
            self.__dripProcess = Process(
                target=self.drip
            )
            self.__indicatorProcess = Thread(target=self.indicatorAct)
            time.sleep(1)

        except Exception as e:
            print(e)

    def start(self):
        # if self.checkConnection():
        #     self.__getCommandProcess.start()
        #     self.__indicatorProcess.start()
        #     self.__dripProcess.start()
        # self.__positioner.test()
        pass

    def checkConnection(self) -> bool:
        if self.__client.ping():
            return True
        else:
            return False

    def getCommandHandle(self):
        isCaptured = False
        try:
            print("job start")
            while True:
                res = self.__client.get("/api/device-status")
                cmd = res["data"]["attributes"]
                capture = res["data"]["attributes"]["status"]

                if capture and not isCaptured:
                    isCaptured = True
                    self.__captureProcess = Process(target=self.capture)
                    self.__captureProcess.start()

                if cmd["forward"]:
                    self.__positioner.moveForward()
                elif cmd["backward"]:
                    self.__positioner.moveBackward()
                elif cmd["left"]:
                    print("here")
                    self.__positioner.moveLeft()
                elif cmd["right"]:
                    self.__positioner.moveRight()

                time.sleep(0.3)
        except Exception as e:
            print(e)

    def capture(self):
        try:
            print("capturing Image")
            self.__camera.capture()
        except Exception as e:
            print(e)

    def drip(self):
        isDrip = False
        try:
            print("drip process start")
            while True:
                # if self.__startButton.isClicked():
                #     isDrip = not isDrip

                # if(isDrip) :
                #     self.__WaterDripper.startDrip()
                # else:
                #     self.__WaterDripper.stopDrip()

                if self.__startButton.isClicked():
                    self.__WaterDripper.dripTiming()
                time.sleep(0.2)

        except Exception as e:
            print(e)

    def indicatorAct(self):
        try:
            while True:
                self.__ledIndicator.on()
                time.sleep(0.3)
                self.__ledIndicator.off()
                time.sleep(0.3)
        except Exception as e:
            print(e)

    def main(self):
        while not self.__startButton.isClicked():
            pass

        print("start")
