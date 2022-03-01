#!/usr/bin/env python

import RPi.GPIO


def init() -> None:
    RPi.GPIO.setmode(RPi.GPIO.BCM)
    RPi.GPIO.setwarnings(False)


def setup_out(pin: int, initial: bool = False) -> None:
    RPi.GPIO.setup(pin, RPi.GPIO.OUT, initial=initial)


def setup_button(pin: int) -> None:
    RPi.GPIO.setup(pin, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)


def input(pin: int) -> any:
    return RPi.GPIO.input(pin)


def output(pin: int, data: any) -> None:
    RPi.GPIO.output(pin, data)
