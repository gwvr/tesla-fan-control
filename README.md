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
sudo cp tesla_fan_control.py /usr/local/bin/tesla_fan_control.py
sudo chmod +x /usr/local/bin/tesla_fan_control.py
```

## Configure SystemD unit

```sh
sudo cp tesla-fan-control.service /etc/systemd/system/tesla-fan-control.service
systemctl daemon-reload
systemctl enable tesla-fan-control
systemctl start tesla-fan-control
systemctl status tesla-fan-control
```
