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
import json


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
            load_dotenv(dotenv_path="/home/pi/Documents/project/project-TM/src/.env")
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
        )
        self.__indicatorProcess = Thread(target=self.indicatorAct)
        self.__getCommandProcess.start()
        self.__indicatorProcess.start()
        self.__dripProcess.start()

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
                # print(cmd)

                if capture:
                    self.__captureProcess = Process(target=self.capture)
                    self.__captureProcess.start()
                    self.__captureProcess.join()
                    self.__captureProcess.kill()

                if cmd["forward"]:
                    print("forward")
                    self.__positioner.move(self.__positioner.Movement.FORWARD)
                elif cmd["backward"]:
                    print("backward")
                    self.__positioner.move(self.__positioner.Movement.BACKWARD)
                elif cmd["left"]:
                    print("left")
                    self.__positioner.move(self.__positioner.Movement.LEFT)
                elif cmd["right"]:
                    print("right")
                    self.__positioner.move(self.__positioner.Movement.RIGHT)
                elif cmd["up"]:
                    print("up")
                    self.__positioner.move(self.__positioner.Movement.UP)
                elif cmd["down"]:
                    print("down")
                    self.__positioner.move(self.__positioner.Movement.DOWN)

                # if key:
                #     res = self.__client.put("/api/device-status", key)
                # res = self.__client.put("/api/device-status")
                time.sleep(0.2)
            except Exception as e:
                print(e)

    def capture(self):
        print("capture process start")
        try:
            if self.__camera.capture():
                img = open(
                    "/home/pi/Documents/project/project-TM/temp/temp1.jpeg", "rb")
                files = {"files.capturedImage" :  (img.name, img)}
                data =  {"data" : json.dumps({"result" : 0})}
                res = self.__client.post("/api/captures", files=files, data=data)
                print(res)
                res = self.__client.put("/api/device-status")
                print(res)
                # time.sleep(1)
                # print("kill process")
            else:
                return
        except Exception as e:
            print(e)
        

    # def button(self, buttonQueue : Queue):
    #     isDrip = False
    #     print("button process start")
    #     try:
    #         while True:
    #             if self.__startButton.isClicked():
    #                 isDrip = True
    #                 buttonQueue.put(isDrip)
    #             else:
    #                 isDrip = False
    #                 buttonQueue.put(isDrip)
    #     except Exception as e:
    #         print(e)

    def drip(self):
        print("drip process start")
        try:
            while True:
                if self.__startButton.isClicked():
                    # print("on")
                    self.__WaterDripper.startDrip()
                else:
                    # print("off")
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
