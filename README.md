# Nvidia Tesla add-on fan speed controller

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

Content of `/etc/systemd/system/tesla_fan_control.service`:

```systemd
[Unit]
Description=Fan control service
After=fancontrol.service

[Service]
ExecStart=/usr/bin/python /root/tesla_fan_control.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```sh
systemctl status tesla_fan_control
```
