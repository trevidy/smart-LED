def web_page():
    return """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Pico LED Control</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            margin-top: 40px;
        }
        input[type=range]{
            width: 80%%;
        }
        button{
            font-size: 18px;
            padding: 10px 20px;
            margin: 10px;
        }
    </style>
</head>
<body>
    <h1>Smart LED Control</h1>

    <button onclick = "sendCmd('on')">ON</button>
    <button onclick = "sendCmd('off')">OFF</button>

    <br><br>

    <input id="slider" type ="range" min="0" max="255" value="0">

    <script>
    let ws;
    let slider = document.getElementById("slider");

    function connect() {
        ws = new WebSocket("ws://" + location.host + "/ws");

        ws.onopen = () => {
            console.log("Websocket connected");
        };

        ws.onclose = () => {
            console.log("Websocket disconnected, retrying...");
            setTimeout(connect, 1000);
        };

        ws.onerror = (err) => {
            console.log("Websocket error", err);
        };

    }

    function sendCmd(cmd){
        if (ws && ws.readyState === WebSocket.OPEN){
            ws.send(JSON.stringify({ cmd: cmd }));
        }
    }

    slider.addEventListener("input", () => {
        if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({
                cmd: "set",
                value: slider.value
            }));
        }
    });

    connect();
    </script>

</body>
</html>
"""
 
