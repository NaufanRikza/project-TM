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
    __movementProcess = None
    __captureProcess = None
    __indicatorProcess = None
    __commandQueue = None
    __captureQueue = None

    def __init__(self) -> None:
        try:
            GPIO.setmode(GPIO.BCM)
            self.__client = Client("http://193.203.164.177:1337")
            # self.__camera = Camera(Pins.CAMERA_PORT.value)
            self.__positioner = Positioner(
                Pins.SERVO_1, Pins.SERVO_2, Pins.SERVO_3)
            self.__WaterDripper = WaterDripper(
                Pins.MOTOR_CONTROLLER_IN1, Pins.MOTOR_CONTROLLER_IN2)
            self.__startButton = Button(Pins.START_BUTTON)
            self.__ledIndicator = Led(Pins.LED_PORT)

            self.__commandQueue = Queue(1)
            self.__captureQueue = Queue(1)

            self.__getCommandProcess = Process(
                target=self.getCommandHandle, args=(self.__commandQueue, self.__captureQueue,))
            # self.__getCommandProcess.start()

            self.__movementProcess = Process(
                target=self.movement, args=(self.__commandQueue,))
            # self.__movementProcess.start()

            self.__captureQueue = Process(
                target=self.capture, args=(self.__captureQueue,))
            # self.__captureQueue.start()

            self.__indicatorProcess = Process(target=self.indicatorAct)

        except Exception as e:
            print(e)

    def start(self):
        print("checking connection...")
        if self.checkConnection():
            print("Connection Online")
            self.startProcesses()

            while True:
                if self.__startButton.isClicked():
                    print("clicked")
        else:
            print("no connection")

    def startProcesses(self):
        # self.__getCommandProcess.start()
        # self.__movementProcess.start()
        # self.__captureQueue.start()
        # self.__ledIndicator.on()
        self.__indicatorProcess.start()

    def checkConnection(self) -> bool:
        if self.__client.ping():
            return True
        else:
            return False

    def getCommandHandle(self, commandQueue: Queue, captureQueue: Queue):
        try:
            print("job start")
            while True:
                res = self.__client.get("/api/device-status")
                cmd = res["data"]["attributes"]
                capture = res["data"]["attributes"]["status"]

                if commandQueue.full():
                    commandQueue.get()

                if captureQueue.full():
                    captureQueue.get()

                commandQueue.put(cmd)
                captureQueue.put(capture)

                time.sleep(0.3)
        except Exception as e:
            print(e)

    def movement(self, commandQueue: Queue):
        try:
            print("get command start")
            while True:
                # pass
                data = None
                if commandQueue.full():
                    data = commandQueue.get()
                if data:
                    # print(data)
                    pass
                # print('from command job')

        except Exception as e:
            print(e)
        # self.__camera.capture()

    def capture(self, captureQueue: Queue):
        try:
            print("capture job start")
            while True:
                status = False
                if captureQueue.full():
                    status = captureQueue.get()

                if status:
                    img = open(
                        "/home/pi/Documents/project-TM/temp/code.png", 'rb')
                    res = self.__client.post(
                        "/api/captures", params={"populate": "*"}, files={"img-capture": img})
                    # print(res)
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
