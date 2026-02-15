import network
import socket
import time
from secrets import SSID, PASSWORD
TIMEOUT = 20


# -------- Wi-Fi ---------
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

# -------- Web Server ---------
addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr) # attach a socket to this address
s.listen(1) # listen for a client

print("Listening on", addr)
try:
    while True:
        conn, addr = s.accept() # blocking call to wait for client.
        try:
            # conn = private connection to client.
            print("Client connected from", addr)

            request = conn.recv(1024)
            print("Request:", request)

            response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html\r\n"
                "Connection: close\r\n"
                "\r\n"
                "<h1>Hello Pico</h1>"
            )

            # close the client connection
            conn.send(response)
        finally:
            conn.close()


except KeyboardInterrupt:
    print("Stopped by user")

finally:
    # close the client and server
    s.close()
    print("Socket closed")
