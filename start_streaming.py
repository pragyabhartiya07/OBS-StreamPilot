import obsws_python as obs

client = obs.ReqClient(host="localhost", port=4455, password="cocobaby@130306")
client.start_stream()
print("📡 Streaming started")