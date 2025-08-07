import os
import time
import numpy as np
import logging
import sys
from subprocess import check_output

# Configure logging to work with systemd
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)  # Log to stdout for systemd to capture
    ]
)
logger = logging.getLogger(__name__)

# Set the threshold temperatures (in Celsius)
min_temp = 45  # Temperature at which fan runs at minimum speed
max_temp = 50  # Temperature at which fan runs at maximum speed

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

logger.info("GPU fan control script starting")

try:
    while True:
        try:
            # Get the current temperature of the Tesla card using nvidia-smi
            output = check_output(['nvidia-smi', '--query-gpu=temperature.gpu', '--format=csv,noheader,nounits'])
            temp = float(output.decode('utf-8').strip())
            
            # Calculate PWM value based on current temperature
            pwm_value = calculate_fan_pwm(temp)
            
            # Set the fan speed
            os.system(f'echo "{pwm_value}" > /sys/class/hwmon/hwmon2/pwm5')
            logger.info(f"GPU Temperature: {temp}°C, Fan PWM: {pwm_value}")
            
        except Exception as e:
            logger.error(f"Error in temperature monitoring loop: {str(e)}")
            
        time.sleep(5)  # Check temperature every 10 seconds
        
except KeyboardInterrupt:
    logger.info("Script terminated by user")
except Exception as e:
    logger.error(f"Unexpected error: {str(e)}")
    raise
