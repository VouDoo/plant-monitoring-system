# Texas Instruments SN74AHCT125 Level-shifter

## Wiring schema

```txt
                .     _____
[1] ground      1OE -|  U  |- Vcc main +5V   [0]
[1] input 3.3V  1A  -|     |- 4OE ground     [4]
[1] ouput 5V    1Y  -|     |- 4A  input 3.3V [4]
[2] ground      2OE -|     |- 4Y  ouput 5V   [4]
[2] input 3.3V  2A  -|     |- 3OE ground     [3]
[2] ouput 5V    2Y  -|     |- 3A  input 3.3V [3]
[0] main ground GND -|_____|- 3Y  ouput 5V   [3]
```
