#!/usr/bin/env python

import os
import logging
import time
import picamera

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

        self.__camera = picamera.PiCamera()
        self.__camera.rotation = config.CAMERA_ROTATION
        logging.info(f"Camera rotation is set to {self.__camera.rotation}.")

        self.__output_dir = config.CAMERA_OUTPUT_DIR
        logging.info(f'Camera output directory is set to "{self.__output_dir}".')
        if not os.path.exists(self.__output_dir):
            os.makedirs(self.__output_dir)
            logging.info(f"Camera output directory created as it did not exist.")
        self.__last_output_file = None

    def __led_on(self, state: bool) -> None:
        """Set camera's LED state."""
        gpio.output(self.__gpio_led, state)

    def capture(self) -> None:
        """Capture a photo with the camera module and save it as a file."""
        now = time.strftime("%Y%m%d-%H%M%S")
        filepath = os.path.join(self.__output_dir, f"capture_{now}.jpg")

        self.__led_on(True)
        self.__camera.start_preview()
        time.sleep(3)  # camera warm-up time
        self.__camera.capture(filepath, "jpeg")
        self.__camera.stop_preview()
        self.__led_on(False)
        self.__last_output_file = filepath
        logging.info(f'Captured photo saved as "{filepath}".')

    def get_last_output(self) -> str:
        """Get path of the last output file."""
        return self.__last_output_file

    def is_button_pressed(self) -> bool:
        """Get state of the button and return True is the button is pressed."""
        state = gpio.input(self.__gpio_button)
        if state == 0:
            return True
        return False