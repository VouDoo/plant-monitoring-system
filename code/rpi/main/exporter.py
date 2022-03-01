#!/usr/bin/env python

import logging
import threading
import prometheus_client

# internal module(s)
import config
import lux_sensor as lux_sensor_module
import led_strip as led_strip_module


def serve(
    event: threading.Event,
    led_strip: led_strip_module.LedStrip,
    lux_sensor: lux_sensor_module.LuxSensor,
) -> None:
    led_strip_mode_enum = prometheus_client.Enum(
        "led_strip_mode",
        "Current mode set for the LED strip",
        states=[e.name for e in led_strip_module.LedMode],
    )
    lux_quantity_gauge = prometheus_client.Gauge(
        "lux_quantity", "Quantity of Lux from the sensor"
    )
    light_quantity_gauge = prometheus_client.Gauge(
        "light_quantity", "Quantity of light from the sensor"
    )

    prometheus_client.start_http_server(config.EXPORTER_PORT)
    logging.info(f"Prometheus metrics exposed on port {config.EXPORTER_PORT}.")

    while not event.is_set():
        led_strip_mode_enum.state(led_strip.get_currmode().name)
        lux_quantity_gauge.set(lux_sensor.get_lux())
        light_quantity_gauge.set(lux_sensor.get_light())
        event.wait(1)
