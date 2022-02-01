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

`i2c-tools` package provides a bench of tools to analyse I2C buses.

To detect I2C chips, run this command:

```sh
ic2detect -y 1
```

To read the lux sensor I2C chip, run this command:

_`0x10` is the address used by the chip._

```sh
i2cget -y 1 0x10
# if no error, it should return "0x00", else "Error: Read failed"
```
