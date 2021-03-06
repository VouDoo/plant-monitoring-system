#!/usr/bin/env python

import board

LED_STRIP_PIN = board.D18
LED_STRIP_LED_COUNT = 30
LED_STRIP_BUTTON_GPIO = 24

LUX_SENSOR_SCL_PIN = board.SCL
LUX_SENSOR_SDA_PIN = board.SDA
LUX_LOW_THRESHOLD = 100

CAMERA_ROTATION = 180
CAMERA_BUTTON_GPIO = 23
CAMERA_CAPTURE_DIR = "./camera_captures"

EXPORTER_PORT = 8000

LOG_FILE = "./plant_monitoring_system.log"
