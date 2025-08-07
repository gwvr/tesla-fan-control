import os
import time
import numpy as np
import logging
import sys
from subprocess import check_output

# Set the threshold temperatures (in Celsius)
min_temp = 50  # Temperature at which fan runs at minimum speed
max_temp = 65  # Temperature at which fan runs at maximum speed

# Set the PWM values
min_pwm = 85  # PWM value at min_temp
max_pwm = 255  # PWM value at max_temp

# Fan control parameters
FAN_HWMON_PATH = "/sys/class/hwmon/hwmon2"
FAN_PWM_FILE = "pwm5"
FAN_ENABLE_FILE = "pwm5_enable"

# Logging control variables
log_interval = 10  # Log once per 10 seconds
log_counter = 0  # Counter to track elapsed time
last_pwm = None  # Track last PWM value to log changes

# Configure logging to work with systemd
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)  # Log to stdout for systemd to capture
    ],
)
logger = logging.getLogger(__name__)


def enable_pwm_control():
    """Enable manual PWM control for the fan.

    Values for pwm*_enable:
    0: No control (fan at full speed)
    1: Manual control (control pwm value manually)
    2: Automatic control (hwmon sets pwm value automatically)
    """
    try:
        enable_file = os.path.join(FAN_HWMON_PATH, FAN_ENABLE_FILE)
        # Set to 1 for manual control
        os.system(f'echo "1" > {enable_file}')
        logger.info("Enabled manual PWM control for fan")
        return True
    except Exception as e:
        logger.error(f"Error enabling PWM control: {str(e)}")
        raise


def get_gpu_temperature():
    """Get the current GPU temperature from nvidia-smi."""
    try:
        output = check_output(
            [
                "nvidia-smi",
                "--query-gpu=temperature.gpu",
                "--format=csv,noheader,nounits",
            ]
        )
        return float(output.decode("utf-8").strip())
    except Exception as e:
        logger.error(f"Error getting GPU temperature: {str(e)}")
        raise


def calculate_fan_pwm(temp):
    """Calculate fan PWM value linearly based on temperature using NumPy."""
    # np.interp performs linear interpolation
    # np.clip ensures temp stays within bounds for interpolation
    return int(
        np.interp(
            np.clip(temp, min_temp, max_temp),  # Clipped temperature value
            [min_temp, max_temp],  # Temperature range
            [min_pwm, max_pwm],  # Corresponding PWM range
        )
    )


def set_fan_speed(pwm_value):
    """Set the fan speed using the provided PWM value."""
    try:
        pwm_file = os.path.join(FAN_HWMON_PATH, FAN_PWM_FILE)
        os.system(f'echo "{pwm_value}" > {pwm_file}')
    except Exception as e:
        logger.error(f"Error setting fan speed: {str(e)}")
        raise


logger.info("GPU fan control script starting")

if __name__ == "__main__":

    try:
        # First enable PWM control
        enable_pwm_control()

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
            time.sleep(1)  # Check temperature every 1 second

    except KeyboardInterrupt:
        logger.info("Script terminated by user")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise
