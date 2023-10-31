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
from dotenv import load_dotenv
import os


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
    __buttonProcess = None
    __buttonQueue = Queue(1)

    def __init__(self) -> None:
        try:
            load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))
            GPIO.setmode(GPIO.BCM)
            self.__client = Client(os.getenv("BASE_URL"))
            self.__camera = Camera(Pins.CAMERA_PORT)
            self.__positioner = Positioner(
                Pins.SERVO_1, Pins.SERVO_2, Pins.SERVO_3)
            self.__WaterDripper = WaterDripper(
                Pins.MOTOR_CONTROLLER_IN1, Pins.MOTOR_CONTROLLER_IN2)
            self.__startButton = Button(Pins.START_BUTTON)
            self.__ledIndicator = Led(Pins.LED_PORT)
            time.sleep(1)

        except Exception as e:
            print(e)

    def start(self):
        if not self.checkConnection():
            while True:
                if self.checkConnection():
                    break

        self.__getCommandProcess = Thread(
            target=self.getCommandHandle)
        self.__dripProcess = Process(
            target=self.drip,
            args=(self.__buttonQueue,)
        )
        self.__indicatorProcess = Thread(target=self.indicatorAct)
        self.__buttonProcess = Thread(target=self.button, args=(self.__buttonQueue,))
        self.__getCommandProcess.start()
        self.__indicatorProcess.start()
        self.__dripProcess.start()
        self.__buttonProcess.start()
        # self.__positioner.test()
        # pass

    def checkConnection(self) -> bool:
        if self.__client.ping():
            return True
        else:
            return False

    def getCommandHandle(self):
        print("command process start")
        while True:
            try:
                res = self.__client.get("/api/device-status")
                cmd = res["data"]["attributes"]
                capture = res["data"]["attributes"]["status"]
                print("capture : {}".format(capture))

                if capture:
                    self.__captureProcess = Process(target=self.capture)
                    self.__captureProcess.start()

                key = None
                if cmd["forward"]:
                    self.__positioner.move(self.__positioner.Movement.FORWARD)
                    key = "forward"
                elif cmd["backward"]:
                    self.__positioner.move(self.__positioner.Movement.BACKWARD)
                    key = "backward"
                elif cmd["left"]:
                    self.__positioner.move(self.__positioner.Movement.LEFT)
                    key = "left"
                elif cmd["right"]:
                    self.__positioner.move(self.__positioner.Movement.RIGHT)
                    key = "right"
                elif cmd["up"]:
                    self.__positioner.move(self.__positioner.Movement.UP)
                    key = "up"
                elif cmd["down"]:
                    self.__positioner.move(self.__positioner.Movement.DOWN)
                    key = "down"

                if key:
                    res = self.__client.put("/api/device-status", key)
                    print(res)
                time.sleep(0.2)
            except Exception as e:
                print(e)

    def capture(self):
        print("capture process start")
        try:
            print("capturing Image")
            if self.__camera.capture():
                img = open(
                    "../../temp/temp1.jpeg", "rb")
                res = self.__client.post(
                    "/api/captures", params={"populate": "*"}, files=img)
                print(res)
                if res["error"]["status"] == 200:
                    res = self.__client.put("/api/device-status", "status")
        except Exception as e:
            print(e)

    def button(self, buttonQueue : Queue):
        isDrip = False
        print("button process start")
        try:
            while True:
                if self.__startButton.isClicked():
                    isDrip = not isDrip
                    buttonQueue.put(isDrip)
                time.sleep(0.2)
        except Exception as e:
            print(e)

    def drip(self, buttonQueue : Queue):
        isDrip = False
        print("drip process start")
        try:
            while True:
                if buttonQueue.full():
                    isDrip = buttonQueue.get()

                if (isDrip):
                    self.__WaterDripper.startDrip()
                else:
                    self.__WaterDripper.stopDrip()

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
