
import math


class Pins:
    SERVO_1 = 12
    SERVO_2 = 18
    SERVO_3 = 13
    START_BUTTON = 23
    MOTOR_CONTROLLER_IN1 = 24
    MOTOR_CONTROLLER_IN2 = 25
    BUZZER = 8
    LED_PORT = 4
    CAMERA_PORT = 0


class InverseKinematics:
    RF = 60
    RE = 150
    F = 127
    E = 45
    SQRT3 = math.sqrt(3.0)
    PI = 3.141592653
    SIN120 = SQRT3/2.0
    COS120 = -0.5
    TAN60 = SQRT3
    SIN30 = 0.5
    TAN30 = 1/SQRT3
