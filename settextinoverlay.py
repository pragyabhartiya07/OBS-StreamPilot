import obsws_python as obs

client = obs.ReqClient(host="localhost", port=4455, password="cocobaby@130306")

source_name = "camera"
new_text = "hii"

client.set_input_settings(source_name, {"text": new_text}, overlay=True)

print(f"📝 Updated text source {camera} → {hii}")