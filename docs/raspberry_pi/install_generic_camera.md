# Install generic camera on Raspberry Pi

## Links

- [The official documentation to use a Raspberry Pi camera module.](https://www.raspberrypi.com/documentation/accessories/camera.html)

## Disable camera LED

Edit `/boot/config.txt` and add the following lines:

```ini
# Disable LED on camera
disable_camera_led=1
```
