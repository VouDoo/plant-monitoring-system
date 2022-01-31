"""Capture to file

This script captures photos taken by the Raspberry Pi camera module and save them as files.
It captures a photo each time the button is pressed.

Before using this script, ensure that the /home/pi/camera directory exists.
"""

import RPi.GPIO as GPIO
from time import sleep, strftime
from picamera import PiCamera

CAMBTN = 23  # pin 16
CAMLED = 32

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(CAMLED, GPIO.OUT, initial=False)
GPIO.setup(CAMBTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

camera = PiCamera()

while True:
    GPIO.output(CAMLED, False)
    if GPIO.input(CAMBTN) == False:
        print("Capturing photo...")
        fpath = "/home/pi/camera/{}.jpg".format(strftime("%Y%m%d-%H%M%S"))
        GPIO.output(CAMLED, True)
        camera.start_preview()
        sleep(2)  # Camera warm-up time
        camera.capture(fpath, "jpeg")
        camera.stop_preview()
        print(f"Saved as {fpath}.")
