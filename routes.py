from machine import Pin, PWM
from constants import MAX_BRIGHTNESS, MIN_BRIGHTNESS
import led
import ujson
    
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
    
def handle_ws_message(msg, ws): 
    # three jobs:
    # 1) decode the message
    # 2) execute a command
    # 3) respond with current state

    """
    Handle a WebSocket message (JSON string)
    """
    try:
        data = ujson.loads(msg) # 'msg' arrives as a string. this converts JSON -> python dictionary.
    except ValueError:
        print("invalid JSON")
        return  # ignore invalid JSON

    cmd = data.get("cmd")

    if cmd == "on":
        led.set_brightness(MAX_BRIGHTNESS)

    elif cmd == "off":
        led.set_brightness(MIN_BRIGHTNESS)

    elif cmd == "set":
        try:
            value = int(data.get("value", 0))
            value = max(0, min(255, value))
            led.set_brightness(int(value * MAX_BRIGHTNESS / 255))
        except:
            pass

    # Send current state back to client
    ws.send(ujson.dumps({
        "brightness": led.get_brightness()
    }))