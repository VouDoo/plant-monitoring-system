#!/usr/bin/env python

import os
import logging
import queue
import threading
from concurrent.futures import ThreadPoolExecutor

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

    logging.info("Starting Plant Monitoring System.")

    gpio.init()

    tasks_queue = queue.Queue(maxsize=3)
    event = threading.Event()

    led_strip = led_strip.LedStrip()
    lux_sensor = lux_sensor.LuxSensor()
    camera = camera.Camera()

    futures = {}

    with ThreadPoolExecutor() as executor:
        futures["tasks_executor"] = executor.submit(
            tasks.executor, tasks_queue, event, led_strip, camera
        )
        futures["tasks_led_strip_handler"] = executor.submit(
            tasks.led_strip_handler, tasks_queue, event, led_strip
        )
        futures["tasks_lux_sensor_handler"] = executor.submit(
            tasks.lux_sensor_handler, tasks_queue, event, lux_sensor, led_strip
        )
        futures["tasks_camera_handler"] = executor.submit(
            tasks.camera_handler, tasks_queue, event, camera
        )
        futures["exporter_serve"] = executor.submit(
            exporter.serve, event, led_strip, lux_sensor
        )

        while not event.is_set():
            event.wait(1)
            for name, call in futures.items():
                if not call.running():
                    logging.error(f'Thread "{name}" has stopped: {call.exception()}.')
                    event.set()
                    executor.shutdown(wait=True, cancel_futures=True)
                    os._exit(1)
