#!/usr/bin/env python

import logging
import busio
import adafruit_veml7700

# internal module(s)
import config


class LuxSensor(object):
    def __init__(self):
        logging.info(f"Initialize Lux sensor object.")

        self.__sensor = adafruit_veml7700.VEML7700(
            busio.I2C(config.LUX_SENSOR_SCL_PIN, config.LUX_SENSOR_SDA_PIN)
        )

    def get_lux(self) -> int:
        return self.__sensor.lux

    def get_light(self) -> int:
        return self.__sensor.light
