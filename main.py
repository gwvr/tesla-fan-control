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

def get_gpu_temperature():
    """Get the current GPU temperature from nvidia-smi."""
    try:
        output = check_output(['nvidia-smi', '--query-gpu=temperature.gpu', '--format=csv,noheader,nounits'])
        return float(output.decode('utf-8').strip())
    except Exception as e:
        logger.error(f"Error getting GPU temperature: {str(e)}")
        raise

def set_fan_speed(pwm_value):
    """Set the fan speed using the provided PWM value."""
    try:
        os.system(f'echo "{pwm_value}" > /sys/class/hwmon/hwmon2/pwm5')
    except Exception as e:
        logger.error(f"Error setting fan speed: {str(e)}")
        raise

logger.info("GPU fan control script starting")

# Logging control variables
log_interval = 10  # Log once per minute (in seconds)
log_counter = 0    # Counter to track elapsed time
last_pwm = None    # Track last PWM value to log changes

try:
    # Log initial temperature and PWM value
    try:
        temp = get_gpu_temperature()
        pwm_value = calculate_fan_pwm(temp)
        last_pwm = pwm_value  # Set initial last_pwm
        
        # Set the fan speed
        set_fan_speed(pwm_value)
        
        # Always log the initial value
        logger.info(f"Initial GPU Temperature: {temp}°C, Fan PWM: {pwm_value}")
    except Exception as e:
        logger.error(f"Error initializing: {str(e)}")
        last_pwm = None  # Reset last_pwm if initial reading fails
    
    while True:
        try:
            # Get the current temperature and calculate PWM
            temp = get_gpu_temperature()
            pwm_value = calculate_fan_pwm(temp)
            
            # Set the fan speed
            set_fan_speed(pwm_value)
            
            # Log when PWM value changes, respecting log interval
            if last_pwm != pwm_value:
                if log_counter >= log_interval:
                    logger.info(f"GPU Temperature: {temp}°C, Fan PWM: {pwm_value}")
                    log_counter = 0
                last_pwm = pwm_value
                      
        except Exception as e:
            logger.error(f"Error in temperature monitoring loop: {str(e)}")
            
        # Increment counter and sleep
        log_counter += 1
        time.sleep(1)  # Check temperature every 1 seconds
        
except KeyboardInterrupt:
    logger.info("Script terminated by user")
except Exception as e:
    logger.error(f"Unexpected error: {str(e)}")
    raise
