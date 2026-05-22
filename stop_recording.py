import obsws_python as obs
client = obs.ReqClient(host="localhost", port=4455, password="cocobaby@130306")
client.stop_record()
print("✅ Recording stopped successfully.")

