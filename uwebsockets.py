# uwebsocket.py
import ubinascii
import uhashlib

_GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"


class WebSocket:
    def __init__(self, sock, request):
        self.sock = sock
        self.open = False
        self._handshake(request)

    def _handshake(self, request):
        headers = request.decode().split("\r\n")
        key = None

        for h in headers:
            if h.startswith("Sec-WebSocket-Key"):
                key = h.split(": ")[1]
                break

        if not key:
            raise ValueError("WebSocket key not found")

        accept = ubinascii.b2a_base64(
            uhashlib.sha1((key + _GUID).encode()).digest()
        ).strip().decode()

        response = (
            "HTTP/1.1 101 Switching Protocols\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            "Sec-WebSocket-Accept: {}\r\n\r\n"
        ).format(accept)

        self.sock.send(response)
        self.open = True

    def recv(self):
        try:
            hdr = self.sock.recv(2)
            if not hdr:
                self.open = False
                return None

            length = hdr[1] & 0x7F

            if length == 126:
                length = int.from_bytes(self.sock.recv(2), "big")
            elif length == 127:
                length = int.from_bytes(self.sock.recv(8), "big")

            mask = self.sock.recv(4)
            data = bytearray(self.sock.recv(length))

            for i in range(length):
                data[i] ^= mask[i % 4]

            return data.decode()

        except:
            self.open = False
            return None

    def send(self, msg):
        if not self.open:
            return

        data = msg.encode()
        length = len(data)

        if length < 126:
            header = bytes([0x81, length])
        elif length < 65536:
            header = bytes([0x81, 126]) + length.to_bytes(2, "big")
        else:
            header = bytes([0x81, 127]) + length.to_bytes(8, "big")

        self.sock.send(header + data)

    def close(self):
        try:
            self.sock.send(b"\x88\x00")
        except:
            pass
        self.open = False
        self.sock.close()