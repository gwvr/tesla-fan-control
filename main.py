import os
import time
import numpy as np
from subprocess import check_output

# Set the threshold temperatures (in Celsius)
min_temp = 50  # Temperature at which fan runs at minimum speed
max_temp = 65  # Temperature at which fan runs at maximum speed

# Set the PWM values
min_pwm = 85   # PWM value at min_temp
max_pwm = 255  # PWM value at max_temp

def calculate_fan_pwm(temp):
    """Calculate fan PWM value linearly based on temperature using NumPy."""
    # np.interp performs linear interpolation
    # np.clip ensures temp stays within bounds for interpolation
    return int(np.interp(
        np.clip(temp, min_temp, max_temp),  # Clipped temperature value
        [min_temp, max_temp],               # Temperature range
        [min_pwm, max_pwm]                  # Corresponding PWM range
    ))

while True:
    # Get the current temperature of the Tesla card using nvidia-smi
    output = check_output(['nvidia-smi', '--query-gpu=temperature.gpu', '--format=csv,noheader,nounits'])
    temp = float(output.decode('utf-8').strip())
    print(f"GPU Temperature: {temp}°C")

    # Calculate PWM value based on current temperature
    pwm_value = calculate_fan_pwm(temp)
    
    # Set the fan speed
    os.system(f'echo "{pwm_value}" > /sys/class/hwmon/hwmon2/pwm5')
    print(f"Setting fan PWM to: {pwm_value}")

    time.sleep(5)  # Check temperature every 5 seconds