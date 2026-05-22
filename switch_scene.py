import obsws_python as obs

client = obs.ReqClient(host="localhost", port=4455, password="cocobaby@130306")
client.set_current_program_scene("manasvi")
print("✅ Switched to scene: manasvi")