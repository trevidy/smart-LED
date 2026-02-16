import led
def web_page():
    return f"""
<!DOCTYPE html>
<html>
<head>
    <title>Pico LED</title>
</head>
<body>
    <h1>Smart LED Control</h1>
    <p>Brightness: {led.get_brightness()}</p>

    <button onclick = "fetch('/on')">ON</button>
    <button onclick = "fetch('/off')">OFF</button>

    <br><br>

    <input type="range" min="0" max="255" value="0"
        oninput="fetch('/set?value=' + this.value)">
</body>
</html>
"""
