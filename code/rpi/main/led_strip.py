#!/usr/bin/env python

import logging
import time
import enum
from neopixel import NeoPixel

# internal module(s)
import config
import gpio


class LedMode(enum.Enum):
    OFF = 0
    PLANT = 1
    CAMERA = 2


class LedStrip(object):
    def __init__(self):
        logging.info(f"Initialize LED strip object.")

        self.__gpio_button = config.LED_STRIP_BUTTON_GPIO
        gpio.setup_button(self.__gpio_button)
        logging.info(f"LED strip button is initiated on GPIO {self.__gpio_button}.")

        self.__pin = config.LED_STRIP_PIN
        logging.info(f"LED strip is initiated on PIN {self.__pin}.")

        self.__count = config.LED_STRIP_LED_COUNT
        logging.info(f"LED strip is initiated with {self.__count} LEDs.")

        self.__pixels = NeoPixel(self.__pin, self.__count)

        self.set_mode(LedMode.OFF)
        self.__currmode = LedMode.OFF
        self.__forceoff = False

    def __color_one(self, index: int, red: int, green: int, blue: int) -> None:
        """Set color for a single LED at specific index."""
        self.__pixels[index] = (red, green, blue)

    def __color_all(self, red: int, green: int, blue: int) -> None:
        """Set color for every LED."""
        self.__pixels.fill((red, green, blue))

    def get_currmode(self) -> LedMode:
        return self.__currmode

    def set_mode(self, mode: LedMode, become_current: bool = True) -> None:
        """Set LED mode."""
        if mode == LedMode.OFF:
            self.__color_all(0, 0, 0)
        elif mode == LedMode.PLANT:
            for i in range(0, self.__count):
                if i % 5 == 0:
                    self.__color_one(i, 0, 0, 255)
                else:
                    self.__color_one(i, 255, 0, 0)
        elif mode == LedMode.CAMERA:
            td = 0.05  # transition delay in seconds
            self.__color_all(0, 0, 0)
            middle = self.__count // 2
            self.__color_one(middle, 255, 255, 255)
            time.sleep(td)
            for i in range(1, middle + 1):
                if middle + i < self.__count:
                    self.__color_one(middle + i, 255, 255, 255)
                self.__color_one(middle - i, 255, 255, 255)
                time.sleep(td)
        else:
            logging.error(f'Unknown "{mode.name}" LED mode.')

        if become_current:
            self.__currmode = mode

    def enable_force_off(self, state: bool) -> None:
        self.__forceoff = state

    def is_force_off_enabled(self) -> bool:
        return self.__forceoff

    def is_button_pressed(self) -> bool:
        """Get state of the button and return True is the button is pressed."""
        state = gpio.input(self.__gpio_button)
        if state == 0:
            return True
        return False
