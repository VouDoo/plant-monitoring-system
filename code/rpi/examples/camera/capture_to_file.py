#!/usr/bin/python

"""Capture to file

This script captures photos taken by the Raspberry Pi camera module and save them as files.
It captures a photo each time the button is pressed.
"""

import os
from time import sleep, strftime
# GPIO module(s)
import RPi.GPIO as GPIO
# camera module(s)
from picamera import PiCamera


# GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# camera
CAMBTN = 23  # pin 16
CAMLED = 32  # camera's integrated pin
GPIO.setup(CAMLED, GPIO.OUT, initial=False)
GPIO.setup(CAMBTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
camera = PiCamera()

# create camera directory
camera_dir = "/home/pi/camera"
if not os.path.exists(camera_dir):
    os.makedirs(camera_dir)

print("Press the button to take a picture.")
while True:
    GPIO.output(CAMLED, False)  # turn off camera led
    if GPIO.input(CAMBTN) == False:
        print("Capturing photo...")
        fpath = "/home/pi/camera/{}.jpg".format(strftime("%Y%m%d-%H%M%S"))
        GPIO.output(CAMLED, True)  # turn on camera led
        camera.start_preview()
        sleep(2)  # Camera warm-up time
        camera.capture(fpath, "jpeg")
        camera.stop_preview()
        print(f"Saved as \"{fpath}\".")
