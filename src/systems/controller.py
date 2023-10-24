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
    __commandQueue = None
    __captureQueue = None

    def __init__(self) -> None:
        try:
            GPIO.setmode(GPIO.BCM)
            self.__client = Client("http://193.203.164.177:1337")
            # self.__camera = Camera(Pins.CAMERA_PORT.value)
            self.__positioner = Positioner(
                Pins.SERVO_1.value, Pins.SERVO_2.value, Pins.SERVO_3.value)
            self.__WaterDripper = WaterDripper(
                Pins.MOTOR_CONTROLLER_IN1.value, Pins.MOTOR_CONTROLLER_IN2.value)
            self.__startButton = Button(Pins.START_BUTTON.value)
            self.__ledIndicator = Led(Pins.LED_PORT.value)

            self.__commandQueue = Queue(1)
            self.__captureQueue = Queue(1)

            # self.__getCommandProcess = Process(
            #     target=self.getCommandHandle, args=(self.__commandQueue, self.__captureQueue,))
            # self.__getCommandProcess.start()

            # self.__movementProcess = Process(
            #     target=self.movement, args=(self.__commandQueue,))
            # self.__movementProcess.start()

            self.__captureQueue = Process(
                target=self.capture, args=(self.__captureQueue,))
            self.__captureQueue.start()

        except Exception as e:
            print(e)

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
                # print(res)
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
                    pass
                # print('from command job')
                print(data)
        except Exception as e:
            print(e)
        # self.__camera.capture()

    def capture(self, captureQueue: Queue):
        try:
            print("capture job start")
            while True:
                # print(captureQueue.full())
                status = False
                if captureQueue.full():
                    status = captureQueue.get()

                if status:
                    img = open(
                        "/home/pi/Documents/project-TM/temp/code.png", 'rb')
                    res = self.__client.post(
                        "/api/captures", params={"populate": "*"}, files={"img-capture": img})
                    print(res)
        except Exception as e:
            print(e)
