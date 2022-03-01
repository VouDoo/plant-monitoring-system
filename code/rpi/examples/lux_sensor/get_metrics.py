#!/usr/bin/python

"""Get lux metrics

This script gets lux and light metrics from the VEML7700 sensor.
"""

from time import sleep
# lux sensor module(s)
from board import SDA, SCL
from busio import I2C
import adafruit_veml7700


# lux sensor
lux_sensor = adafruit_veml7700.VEML7700(I2C(SCL, SDA))

while True:
    print(f"Lux sensor: ambient light={lux_sensor.light}, lux={lux_sensor.lux}")
    sleep(1)
