import socket
import web
import routes 
from uwebsocket import WebSocket


def get_path(request):
    try:
        line = request.split(b"\r\n")[0]
        return line.split()[1].decode()
    except:
        return "/"
    
def start_server():
    addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr) # attach a socket to this address
    s.listen(1) # listen for a client

    print("Listening on", addr)
    try:
        while True:
            conn, addr = s.accept() # blocking call to wait for client. this is also triggered when fetch() is called.
            try:
                # conn = private connection to client.
                print("Client connected from", addr)

                request = conn.recv(1024)

                if b"Upgrade: websocket" in request:
                    print("WebSocket requested")

                    print("creating websocket object.")
                    ws = WebSocket(conn, request) # create a websocket object

                    print("websocket created. currently waiting..")
                    while ws.open: # as long as this connection stays alive
                        print("waiting for message..")
                        msg = ws.recv() # blocks until a message arrives (for example, sendCmd(set:xx) from web.py through button press)
                        if msg is None: # if none, connection closed. (browser tab closed, client disconnected, etc.)
                            break 

                        print("messsage received. handligng...")
                        routes.handle_ws_message(msg, ws) # handle the message 

                    print("WebSocket closed")
                    ws.close()
                else:
                    path = get_path(request)
                    print("Path:", path)

                    routes.handle_request(path)

                    response = web.web_page()
                    conn.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n") # protocol version, status code(200 = "success", OK = human readable)
                    conn.send(response)
            finally:
                conn.close()
    except KeyboardInterrupt:
        print("Stopped by user")

    finally:
        # close the client and server
        s.close()
        print("Socket closed")
