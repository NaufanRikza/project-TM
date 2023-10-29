import RPi.GPIO as GPIO
import time
import math
from data.constant import InverseKinematics
from enum import Enum

# all measurement is in mm


class Positioner:
    __servo1 = None
    __servo2 = None
    __servo3 = None
    __K1 = 45
    __K2 = 18
    __NEUTRAL_DEG = 80

    __MAX_DUTY = 12.5
    __MIN_DUTY = 2.5

    class Position:
        MAX_POSITIVE_X = 45
        MIN_NEGATIVE_X = -MAX_POSITIVE_X
        MAX_POSITIVE_Y = 45
        MIN_NEGATIVE_Y = -MAX_POSITIVE_Y
        MAX_POSITIVE_Z = 90
        MIN_NEGATIVE_Z = 130
        x = 0
        y = 0
        z = 89

    class Movement(Enum):
        FORWARD = 0
        BACKWARD = 1
        LEFT = 2
        RIGHT = 3
        UP = 4
        DOWN = 4

    __position = Position()
    __tetha = {"servo1": __NEUTRAL_DEG,
               "servo2": __NEUTRAL_DEG, "servo3": __NEUTRAL_DEG}

    def __init__(self, servo1, servo2, servo3) -> None:
        try:
            GPIO.setup(servo1, GPIO.OUT)
            GPIO.setup(servo2, GPIO.OUT)
            GPIO.setup(servo3, GPIO.OUT)

            self.__servo1 = GPIO.PWM(servo1, 50)
            self.__servo2 = GPIO.PWM(servo2, 50)
            self.__servo3 = GPIO.PWM(servo3, 50)

            self.start()

        except Exception as e:
            print(e)
            raise Exception("Positioner initialize error")

    def degToDuty(self, deg):
        return round((deg + self.__K1)/self.__K2, 1)

    def rotateAxis(self, x0, y0, deg):
        deg = InverseKinematics.PI/180*deg
        sinDeg = math.sin(deg)
        cosDeg = math.cos(deg)
        x1 = (cosDeg * x0) - (sinDeg * y0)
        y1 = (sinDeg * x0) + (cosDeg * y0)
        return round(x1), round(y1)

    def calcAngleYZ(self, x0, y0, z0):
        y1 = -0.5 * InverseKinematics.SIN30 * InverseKinematics.F
        y0 -= 0.5 * InverseKinematics.SIN30 * InverseKinematics.E

        a = (pow(x0, 2) + pow(y0, 2) + pow(z0, 2) + pow(InverseKinematics.RF,
             2) - pow(InverseKinematics.RE, 2) - pow(y1, 2)) / (2 * z0)

        b = (y1-y0)/z0
        d = -(a+b*y1)*(a+b*y1)+InverseKinematics.RF * \
            (b*b*InverseKinematics.RF+InverseKinematics.RF)
        # print(d)

        if d < 0:
            return False, None
        yj = (y1 - a*b - math.sqrt(d))/(b*b + 1)
        zj = a + b*yj

        # ((yj>y1)?180.0:0.0)
        c = None
        if yj > y1:
            c = 180.0
        else:
            c = 0.0

        final = round(180.0*math.atan(-zj/(y1 - yj)) /
                      (InverseKinematics.PI + c), 1)
        return True, final

    def calcInverseKinematic(self, x0, y0, z0):
        stat = None
        if (x0 > 0 or y0 > 0):
            x0, y0 = self.rotateAxis(x0, y0, 30)
            print(x0, y0)

        stat, self.__tetha["servo1"] = self.calcAngleYZ(x0, y0, z0)
        if stat:
            stat, self.__tetha["servo2"] = self.calcAngleYZ(
                x0*InverseKinematics.COS120 - y0*InverseKinematics.SIN120, y0*InverseKinematics.COS120+x0*InverseKinematics.SIN120, z0)
        if stat:
            stat, self.__tetha["servo3"] = self.calcAngleYZ(
                x0*InverseKinematics.COS120 + y0*InverseKinematics.SIN120, y0*InverseKinematics.COS120-x0*InverseKinematics.SIN120, z0)
        return stat

    def write(self, servo, deg):
        norm_deg = self.__NEUTRAL_DEG + deg
        duty = self.degToDuty(norm_deg)
        if duty > self.__MAX_DUTY:
            duty = self.__MAX_DUTY
        if duty < self.__MIN_DUTY:
            duty = self.__MIN_DUTY
        self.generatePWM(servo=servo, dutycycle=duty)

    def start(self):
        stat = self.calcInverseKinematic(
            self.__position.x, self.__position.y, self.__position.z)
        if not stat:
            raise Exception("Error Inverse")
        duty1 = self.degToDuty(self.__NEUTRAL_DEG + self.__tetha["servo1"])
        duty2 = self.degToDuty(self.__NEUTRAL_DEG + self.__tetha["servo2"])
        duty3 = self.degToDuty(self.__NEUTRAL_DEG + self.__tetha["servo3"])

        self.__servo1.start(duty1)
        self.__servo2.start(duty2)
        self.__servo3.start(duty3)

    def generatePWM(self, servo, dutycycle):
        if (servo == "servo1"):
            self.__servo1.ChangeDutyCycle(dutycycle)
        elif servo == "servo2":
            self.__servo2.ChangeDutyCycle(dutycycle)
        elif servo == "servo3":
            self.__servo3.ChangeDutyCycle(dutycycle)
        else:
            return

        # self.__posNow[servo] = dutycycle

    def move(self, movement: Movement):
        if movement == self.Movement.FORWARD:
            self.__position.y += 1
        elif movement == self.Movement.BACKWARD:
            self.__position.y -= 1
        elif movement == self.Movement.LEFT:
            self.__position.x -= 1
        elif movement == self.Movement.RIGHT:
            self.__position.x += 1

        stat = self.calcInverseKinematic(
            self.__position.x, self.__position.y, self.__position.z)
        if not stat:
            raise Exception("Error Inverse")

        self.write("servo1", self.__tetha["servo1"])
        self.write("servo2", self.__tetha["servo2"])
        self.write("servo3", self.__tetha["servo3"])

    def test(self):
        while True:
            for i in range(0, 41, 1):
                stat = self.calcInverseKinematic(0, i, 90)
                self.write("servo1", self.__tetha["servo1"])
                self.write("servo2", self.__tetha["servo2"])
                self.write("servo3", self.__tetha["servo3"])
                time.sleep(0.02)

            for i in range(40, 1, -1):
                stat = self.calcInverseKinematic(0, i, 90)
                self.write("servo1", self.__tetha["servo1"])
                self.write("servo2", self.__tetha["servo2"])
                self.write("servo3", self.__tetha["servo3"])
                time.sleep(0.02)

            for i in range(0, -41, -1):
                stat = self.calcInverseKinematic(0, i, 90)
                self.write("servo1", self.__tetha["servo1"])
                self.write("servo2", self.__tetha["servo2"])
                self.write("servo3", self.__tetha["servo3"])
                time.sleep(0.02)

            for i in range(-40, 1, 1):
                stat = self.calcInverseKinematic(0, i, 90)
                self.write("servo1", self.__tetha["servo1"])
                self.write("servo2", self.__tetha["servo2"])
                self.write("servo3", self.__tetha["servo3"])
                time.sleep(0.02)

            # break

            # for i in range(40, 10, -10):

            #     stat = self.calcInverseKinematic(i, 0, 100)
            #     print(stat)
            #     print("s1 : {0}, s2 : {1}, s3 : {2}".format(
            #         self.__tetha["servo1"], self.__tetha["servo2"], self.__tetha["servo3"]))
            #     self.write("servo1", self.__tetha["servo1"])
            #     self.write("servo2", self.__tetha["servo2"])
            #     self.write("servo3", self.__tetha["servo3"])
            #     time.sleep(1)
        # self.generatePWM(servo="servo1", dutycycle=60)
