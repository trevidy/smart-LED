import network
import time
from secrets import SSID, PASSWORD
TIMEOUT = 20

timeout = TIMEOUT
start = time.time()

# connect to the router
wlan = network.WLAN(network.STA_IF)

# power on the CYW43 Wi-Fi chip
wlan.active(True)
wlan.connect(SSID,PASSWORD)

while not wlan.isconnected():
    # if elapsed time is greater than TIMEOUT time, raise an error.
    if time.time() - start>timeout:
        raise RuntimeError("WiFi connection failed")
    time.sleep(0.5)

print("IP:", wlan.ifconfig()[0])
