# Install generic camera on Raspberry Pi

Documentation for the Raspberry Pi camera module: [camera on raspberrypi.com](https://www.raspberrypi.com/documentation/accessories/camera.html).

## Python module

The `python3-picamera` package provides the `picamera` Python module

To install the package, run the command:

```sh
sudo apt-get update && sudo apt-get install -y python3-picamera
```

Documentation for the Python module: [picamera on readthedocs.org](https://picamera.readthedocs.io/en/latest/index.html).

## Disable camera LED at bootup

Edit `/boot/config.txt` and add these lines:

```ini
# Disable LED on camera
disable_camera_led=1
```
