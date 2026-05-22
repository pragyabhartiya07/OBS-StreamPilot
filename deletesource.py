import obsws_python as obs

client = obs.ReqClient(host="localhost", port=4455, password="cocobaby@130306")

source_name = "Video Capture Device"
client.remove_input(source_name)

print(f"🗑️ Deleted source: {source_name}")