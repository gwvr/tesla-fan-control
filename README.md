# Nvidia Tesla add-on fan speed controller

This script provides temperature-based fan speed control for Nvidia Tesla GPUs with add-on cooling fans. It linearly adjusts fan speed based on GPU temperature for optimal cooling and noise levels.

Installation:

1. install system dependencies
1. setup fancontrol
1. install python script
1. configure systemd unit

## System Dependencies

```sh
apt install fancontrol nvidia-smi python3-numpy
```

## Install Python script

```sh
cp main.py /root/tesla_fan_control.py
```

## Configure SystemD unit

Content of `/etc/systemd/system/tesla-fan-control.service`:

```systemd
[Unit]
Description=Fan control service
After=fancontrol.service

[Service]
Type=simple
ExecStart=/usr/bin/python /root/tesla_fan_control.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

```sh
systemctl daemon-reload
systemctl enable tesla-fan-control
systemctl start tesla-fan-control
systemctl status tesla-fan-control
```
