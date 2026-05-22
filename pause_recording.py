import obsws_python as obs

client = obs.ReqClient(host="localhost", port=4455, password="YOUR_PASSWORD")
client.pause_record()
print("⏸️ Recording paused")