#!/usr/bin/env python

import logging
import queue
import threading
import concurrent.futures

# internal module(s)
import config
import gpio
import tasks
import led_strip
import lux_sensor
import camera
import exporter


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%dT%H:%M:%S",
        encoding="utf-8",
        filename=config.LOG_FILE,
    )

    gpio.init()

    tasks_queue = queue.Queue(maxsize=3)
    event = threading.Event()

    led_strip = led_strip.LedStrip()
    lux_sensor = lux_sensor.LuxSensor()
    camera = camera.Camera()

    logging.info("Starting Plant Monitoring System.")

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.submit(tasks.executor, tasks_queue, event, led_strip, camera)
        executor.submit(tasks.led_strip_handler, tasks_queue, event, led_strip)
        executor.submit(tasks.lux_sensor_handler, tasks_queue, event, lux_sensor, led_strip)
        executor.submit(tasks.camera_handler, tasks_queue, event, camera)
        executor.submit(exporter.serve, event, led_strip, lux_sensor)
