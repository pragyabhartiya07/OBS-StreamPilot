import obsws_python as obs

client = obs.ReqClient(host="localhost", port=4455, password="cocobaby@130306")

media_source = "Video Capture Device"
client.trigger_media_input_action(media_source, "OBS_WEBSOCKET_MEDIA_INPUT_ACTION_PAUSE")

print(f"⏸️ Paused media: {media_source}")