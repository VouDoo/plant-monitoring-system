#!/usr/bin/env python

import os
import logging
import time
from picamera import PiCamera

# internal module(s)
import config
import gpio


class Camera(object):
    def __init__(self):
        logging.info(f"Initialize camera object.")

        self.__gpio_led = 32  # camera's integrated pin
        gpio.setup_out(self.__gpio_led)
        self.__gpio_button = config.CAMERA_BUTTON_GPIO
        gpio.setup_button(self.__gpio_button)
        logging.info(f"Camera button is initiated on GPIO {self.__gpio_button}.")

        self.__led_on(False)  # ensure LED is turned off

        self.__camera = PiCamera()
        self.__camera.rotation = config.CAMERA_ROTATION
        logging.info(f"Camera rotation is set to {self.__camera.rotation}.")

        self.__capture_dir = config.CAMERA_CAPTURE_DIR
        logging.info(f'Camera capture directory is set to "{self.__capture_dir}".')
        if not os.path.exists(self.__capture_dir):
            os.makedirs(self.__capture_dir)
            logging.info(f"Camera capture directory created as it did not exist.")

    def __led_on(self, state: bool) -> None:
        """Set camera's LED state."""
        gpio.output(self.__gpio_led, state)

    def capture(self) -> None:
        """Capture a photo with the camera module and save it as a file."""
        now = time.strftime("%Y%m%d-%H%M%S")
        filepath = os.path.join(self.__capture_dir, f"{now}.jpg")

        self.__led_on(True)
        self.__camera.start_preview()
        time.sleep(3)  # camera warm-up time
        self.__camera.capture(filepath, "jpeg")
        self.__camera.stop_preview()
        self.__led_on(False)
        logging.info(f'Captured photo saved as "{filepath}".')

    def is_button_pressed(self) -> bool:
        """Get state of the button and return True is the button is pressed."""
        state = gpio.input(self.__gpio_button)
        if state == 0:
            return True
        return False
