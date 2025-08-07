# Nvidia Tesla add-on fan speed controller

This script provides temperature-based fan speed control for Nvidia Tesla GPUs with an add-on pwm cooling fan. It adjusts fan speed based on GPU temperature for optimal cooling and noise levels.

This script was developed and tested with a Tesla P4 card, installed in a Micro-ATX desktop PC and running Debian 12. The P4 was designed for passive cooling, relying on airflow through a rackmount server to cool it. In a desktop PC, a custom fan and duct is required to keep temperatures at an acceptable level. The test installation uses this [3D print](https://www.thingiverse.com/thing:5984640) and an Arctic
S4028-6K 40mm fan.

Temperature thresholds, min and max fan PWM values, PWM control settings and logging interval are all configured within the `tesla_fan_control.py` script.

## Installation

### System Dependencies

```sh
sudo apt install nvidia-smi python3-numpy
```

### Install Python script

```sh
sudo cp tesla_fan_control.py /usr/local/bin/tesla_fan_control.py
sudo chmod +x /usr/local/bin/tesla_fan_control.py
```

### Configure SystemD unit

```sh
sudo cp tesla-fan-control.service /etc/systemd/system/tesla-fan-control.service
sudo systemctl daemon-reload
sudo systemctl enable tesla-fan-control
sudo systemctl start tesla-fan-control
sudo systemctl status tesla-fan-control
```
