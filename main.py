import os
# import psutil
import time
import numpy as np
from subprocess import check_output

# Set the threshold temperatures (in Celsius)
min_temp = 45
max_temp = 50

while True:
    # Get the current temperature of the Tesla card using nvidia-smi
    output = check_output(['nvidia-smi', '--query-gpu=temperature.gpu', '--format=csv,noheader,nounits'])
    temp = float(output.decode('utf-8').strip())
    print(temp)


    if temp > max_temp:
        # Turn on the fan at maximum speed
        os.system('echo "255" > /sys/class/hwmon/hwmon2/pwm5')
    elif temp < min_temp:
        # Turn down the fan
        os.system('echo "85" > /sys/class/hwmon/hwmon2/pwm5')

    time.sleep(10)  # Check temperature every 10 seconds