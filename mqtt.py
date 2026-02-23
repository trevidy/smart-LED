import time
import ubinascii
import machine
from umqtt.simple import MQTTClient
NAMESPACE = "7f3a9c21e8b44c9d9d2a6a1b" #unique namespace to avoid collision.
DEVICE_ID = "pico01"
BASE_TOPIC = f"trevi/{NAMESPACE}/{DEVICE_ID}"

import led
from constants import MAX_BRIGHTNESS, MIN_BRIGHTNESS

#--------------- MQTT CONFIG ---------------
BROKER = "test.mosquitto.org"
PORT = 1883

CLIENT_ID = b"pico01" + ubinascii.hexlify(machine.unique_id())

TOPIC_LED_SET = f"{BASE_TOPIC}/led/set".encode()
TOPIC_LED_STATE = f"{BASE_TOPIC}/led/state".encode()

TOPIC_BRIGHTNESS_SET = f"{BASE_TOPIC}/led/brightness/set".encode()
TOPIC_BRIGHTNESS_STATE = f"{BASE_TOPIC}/led/brightness/state".encode()

TOPIC_ONLINE = f"{BASE_TOPIC}/online".encode()

#--------------- HELPERS -----------------
def clamp(val):
    return max(MIN_BRIGHTNESS, min(MAX_BRIGHTNESS, val))

#--------------- CALLBACK ----------------
def on_message(topic, msg):
    try: 
        msg = msg.decode()

        if topic == TOPIC_LED_SET:
            if msg == "ON":
                led.set_brightness(MAX_BRIGHTNESS)
                client.publish(TOPIC_LED_STATE,b"ON",retain=True)
        
            elif msg == "OFF":
                led.set_brightness(MIN_BRIGHTNESS)
                client.publish(TOPIC_LED_STATE,b"OFF",retain=True)

        elif topic == TOPIC_BRIGHTNESS_SET:
            value = int(msg)
            value = clamp(value)

            led.set_brightness(value)
            client.publish(
                TOPIC_BRIGHTNESS_STATE, 
                str(value),
                retain=True
            )
    except Exception as e:
        print("MQTT message error:", e)
                
#--------------- MAIN LOOP ---------------
def loop_forever():
    global client 

    while True:
        try:
            print("Connecting to MQTT broker...")
            client = MQTTClient(
                CLIENT_ID,
                BROKER,
                port = PORT,
                keepalive=60
            )            

            # Last Will: mark offline if we die
            client.set_last_will(
                TOPIC_ONLINE,
                b"offline",
                retain=True
            )    

            client.set_callback(on_message)
            client.connect()

            print("MQTT connected")

            # Online status
            client.publish(TOPIC_ONLINE, b"online", retain = True)

            # Subscriptions
            client.subscribe(TOPIC_LED_SET,qos=1)
            client.subscribe(TOPIC_BRIGHTNESS_SET)

            print("MQTT subscribed, entering loop")

            # Blocking loop
            while True:
                client.wait_msg()
        except Exception as e:
            print("MQTT error, reconnecting:", e)
            time.sleep(5)

            
            


