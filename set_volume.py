import obsws_python as obs

client = obs.ReqClient(host="localhost", port=4455, password="cocobaby@130306")

source_name = "Mic/Aux"
volume = 0.5   # range: 0.0 to 1.0
client.set_input_volume(source_name, volume)

print(f"🔊 Volume for {source_name} set to {volume}")