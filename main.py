import wifi

MODE = "SERVER"

wifi.connect()

if MODE == "MQTT":
    import mqtt
    mqtt.loop_forever()

elif MODE == "SERVER":
    import server
    server.start_server()
