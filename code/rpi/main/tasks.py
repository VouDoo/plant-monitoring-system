#!/usr/bin/env python

import logging
import enum
import queue
import threading
import schedule

# internal module(s)
import config
import tasks as tasks_module
import led_strip as led_strip_module
import lux_sensor as lux_sensor_module
import camera as camera_module


class Tasks(enum.Enum):
    TURN_OFF_LED = 0
    SET_LED_FOR_PLANT = 1
    TAKE_PICTURE = 2


def led_strip_handler(
    tasks_queue: queue.Queue,
    event: threading.Event,
    led_strip: led_strip_module.LedStrip,
) -> None:
    """Handle LED strip and produce related tasks."""
    while not event.is_set():
        if led_strip.is_button_pressed():
            if led_strip.is_force_off_enabled():
                logging.info("LED button pressed, disable force off.")
                led_strip.enable_force_off(False)
            else:
                logging.info("LED button pressed, enable force off.")
                led_strip.enable_force_off(True)
                tasks_queue.put(tasks_module.Tasks.TURN_OFF_LED)
        event.wait(1)


def lux_sensor_handler(
    tasks_queue: queue.Queue,
    event: threading.Event,
    lux_sensor: lux_sensor_module.LuxSensor,
    led_strip: led_strip_module.LedStrip,
) -> None:
    """Handle Lux sensor and produce related tasks."""
    while not event.is_set():
        lux = round(lux_sensor.get_lux(), 2)
        if led_strip.is_force_off_enabled():
            pass
        elif (
            lux < config.LUX_LOW_THRESHOLD
            and led_strip.get_currmode() == led_strip_module.LedMode.OFF
        ):
            logging.info(
                f'The lux value is low ({lux}), add "Switch LED to PLANT mode" task to queue.'
            )
            tasks_queue.put(tasks_module.Tasks.SET_LED_FOR_PLANT)
        elif (
            lux >= config.LUX_LOW_THRESHOLD
            and led_strip.get_currmode() == led_strip_module.LedMode.PLANT
        ):
            logging.info(
                f'The lux value is high ({lux}), add "Turn off LED" task to queue.'
            )
            tasks_queue.put(tasks_module.Tasks.TURN_OFF_LED)
        event.wait(5)


def camera_handler(
    tasks_queue: queue.Queue,
    event: threading.Event,
    camera: camera_module.Camera,
) -> None:
    """Handle camera and produce related tasks."""

    def schedule_job():
        logging.info('Scheduled, add "Take picture" task to queue.')
        tasks_queue.put(tasks_module.Tasks.TAKE_PICTURE)

    schedule.every().hour.do(schedule_job)

    while not event.is_set():
        if camera.is_button_pressed():
            logging.info('Camera button pressed, add "Take picture" task to queue.')
            tasks_queue.put(tasks_module.Tasks.TAKE_PICTURE)
            event.wait(10)
        else:
            schedule.run_pending()
        event.wait(1)


def executor(
    tasks_queue: queue.Queue,
    event: threading.Event,
    led_strip: led_strip_module.LedStrip,
    camera: camera_module.Camera,
) -> None:
    """Consume and execute requested tasks from queue."""
    while not event.is_set():
        if not tasks_queue.empty():
            todo = tasks_queue.get(False, 10)
            if todo == Tasks.TURN_OFF_LED:
                logging.info('Execute "Turn off LED" task.')
                led_strip.set_mode(led_strip_module.LedMode.OFF)
            elif todo == Tasks.SET_LED_FOR_PLANT:
                logging.info('Execute "Switch LED to PLANT mode" task.')
                led_strip.set_mode(led_strip_module.LedMode.PLANT)
            elif todo == Tasks.TAKE_PICTURE:
                logging.info('Execute "Take picture" task.')
                if not led_strip.is_force_off_enabled():
                    led_strip.set_mode(led_strip_module.LedMode.CAMERA, False)
                camera.capture()
                if not led_strip.is_force_off_enabled():
                    led_strip.set_mode(led_strip.get_currmode())
            else:
                logging.error(f'Cannot execute task because "{todo.name}" is unknown.')
        event.wait(1)
