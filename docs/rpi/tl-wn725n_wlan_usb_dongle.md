# TP-Link TL-WN725N Wireless USB dongle on Raspberry Pi

Official support page for [TL-WN725N](https://www.tp-link.com/us/support/download/tl-wn725n/).

## Installation

This installation guide assumes that the Raspberry Pi runs a recent version of Raspbian.

_Do not plug the dongle until explicitly mentioned._

### Prepare the system

1. Upgrade existing packages.

    ```sh
    sudo apt-get update && sudo apt-get dist-upgrade
    ```

2. Install required packages.

    ```sh
    sudo apt-get install -y build-essential raspberrypi-kernel-headers git
    ```

### Install the driver

1. Clone the firmware repository ([stand-alone RTL8188EU driver](https://github.com/lwfinger/rtl8188eu)).

    ```sh
    cd ~
    git clone https://github.com/lwfinger/rtl8188eu.git
    ```

2. Compile and install the program.

    ```sh
    cd ~/rtl8188eu
    make all
    sudo make install
    ```

3. _(optional)_ Remove compiled file to save disk space.

    ```sh
    rm -rf ~/rtl8188eu
    ```

### Install the dongle

1. Physically power off the Raspberry Pi.
2. Plug the USB dongle.
3. Power the Raspberry Pi back on.
4. Check if the USB bus is present.

    ```sh
    lsusb | grep 'RTL8188EUS' || echo 'not found'
    ```

5. Check if the module is loaded.

    ```sh
    lsmod | grep '8188eu' || echo 'not loaded'
    ```

6. Check if the network interface is present.

    ```sh
    ip a | grep 'wlan0' || echo 'not found'
    ```

### Configure network interface

1. Create the configuration file for the `wlan0` interface.

    ```sh
    sudo tee /etc/network/interfaces.d/wlan0 <<EOF
    allow-hotplug wlan0
    iface wlan0 inet dhcp
    wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf
    iface default inet dhcp
    EOF
    ```

2. Configure the target router in the `wpa_supplicant.conf` configuration file.

    _Replace placeholders with the router's settings._

    ```sh
    sudo tee -a /etc/wpa_supplicant/wpa_supplicant.conf <<EOF
    network={
    ssid="<WIFI_NETWORK_NAME>"
    psk="<WIFI_NETWORK_PASSWORD>"
    proto=RSN
    key_mgmt=WPA-PSK
    pairwise=CCMP
    auth_alg=OPEN
    }
    EOF
    ```

3. Reboot the system to apply the configuration. Run:

    ```sh
    sudo reboot
    ```
