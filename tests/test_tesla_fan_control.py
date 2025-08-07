import pytest
from tesla_fan_control import calculate_fan_pwm, get_gpu_temperature


@pytest.mark.parametrize("temp, pwm", [(45, 85), (50, 85), (54, 130), (65, 255), (70, 255)])
def test_calculate_fan_pwm(temp, pwm):
    """Test PWM calculation at minimum temperature."""
    # When temperature is at or below min_temp (50°C), PWM should be min_pwm (85)
    assert calculate_fan_pwm(temp) == pwm

def test_get_gpu_temperature():
    temperature = get_gpu_temperature()
    assert type(temperature) is float
    assert 10 <= temperature <= 90

def test_hotness():
    temperature = get_gpu_temperature()
    assert temperature <= 80, print("That's hot! Suggest improving your cooling solution")
