# Adafruit VEML7700 lux sensor

Documentation for this sensor: [VEML7700](https://learn.adafruit.com/adafruit-veml7700/python-circuitpython).

## Installation

### I2C interface

This sensor uses I2C interfaces to send data.

To allow communications on I2C interfaces, you need to enable the automatic loading of I2C kernel module.

To do so, run this command to configure the Raspberry Pi:

```sh
sudo raspi-config
```

Select "3 Interface Options", then "I5 I2C" and finally, select "Yes" to enable it.

## Python module

The required module to drive the sensor is `adafruit-circuitpython-veml7700`.

Install it with `pip`:

```sh
sudo pip3 install adafruit-circuitpython-veml7700
```

## Troubleshooting

### I2C protocol

`i2c-tools` packages provides a bench of tools to analyse I2C buses.
