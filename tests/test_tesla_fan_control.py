import pytest
from tesla_fan_control import calculate_fan_pwm  # , get_gpu_temperature


@pytest.mark.parametrize("temp, pwm", [(45, 85), (50, 85), (65, 255), (70, 255)])
def test_calculate_fan_pwm_min_temp(temp, pwm):
    """Test PWM calculation at minimum temperature."""
    # When temperature is at or below min_temp (50°C), PWM should be min_pwm (85)
    assert calculate_fan_pwm(temp) == pwm
