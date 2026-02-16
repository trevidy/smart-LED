from machine import Pin, PWM
from constants import MAX_BRIGHTNESS, MIN_BRIGHTNESS, LED_PIN, LED_FREQ

led = PWM(Pin(LED_PIN))
led.freq(LED_FREQ)
brightness = 0
led.duty_u16(brightness)

def get_brightness():
    global brightness
    return brightness

def set_brightness(value):
    global brightness
    brightness = value
    led.duty_u16(brightness)
