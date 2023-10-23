
# from systems.Controller import Controller
# import requests
# res = requests.get("http://localhost:4000")
# print(res.json())

# data = Controller()
# print(data.getData())
import cv2 as cv
# import time

cam = cv.VideoCapture(0, cv.CAP_DSHOW)
while True:
    ret, frame = cam.read()
    if ret:
        # cv.imshow('test', frame)
        # cv.imwrite('D:\\Project\\Project-TeknikMesin\\temp\\test.jpg', frame)
        cv.imshow('video', frame)

        key = cv.waitKey(1)
        if key == 27:
            break

cam.release()