from machine import Pin, PWM
from constants import MAX_BRIGHTNESS, MIN_BRIGHTNESS
import led
    
def handle_request(path):
    
    if path == "/on":
        led.set_brightness(MAX_BRIGHTNESS)

    elif path == "/off":
        led.set_brightness(MIN_BRIGHTNESS)
    
    elif path.startswith("/set"):
        try:
            value = int(path.split("value=")[1])
            value = max(0,min(255,value))
            led.set_brightness(int(value * MAX_BRIGHTNESS/255))
        except:
            pass
    
