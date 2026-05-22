import obsws_python as obs

client = obs.ReqClient(host="localhost", port=4455, password="cocobaby@130306")

source_name = "Mic/Aux"   # change to your actual audio source
client.toggle_input_mute(source_name)

print(f"🔇 Toggled mute for {source_name}")