#!/bin/bash

# ensure script is executed as root
if ! [ $(id -u) = 0 ]
then
    echo "This script must be run as root."
    exit 1
fi

# install application
mkdir -p /plant_monitoring_system
curl -SsL "https://github.com/VouDoo/plant-monitoring-system/releases/download/v0.1.0/rpi-app.tar.gz" \
    -o /tmp/rpi-app.tar.gz
tar -xf /tmp/rpi-app.tar.gz -C /plant_monitoring_system
rm /tmp/rpi-app.tar.gz
/usr/bin/python3 -m pip install -r /plant_monitoring_system/requirements.txt

# create systemd unit service
cat > /etc/systemd/system/plant_monitoring_system.service << EOF
[Unit]
Description=Plant Monitoring System
After=multi-user.target

[Service]
Type=simple

User=root
Group=root

Restart=always
RestartSec=10

WorkingDirectory=/plant_monitoring_system
ExecStart=/usr/bin/python3 __main__.py

[Install]
WantedBy=multi-user.target
EOF

# enable and start service
systemctl daemon-reload
systemctl enable --now plant_monitoring_system
