import obsws_python as obs

client = obs.ReqClient(host="localhost", port=4455, password="cocobaby@130306")

source_name = "Video Capture Device"

# Play
client.trigger_media_input_action(source_name, "OBS_WEBSOCKET_MEDIA_INPUT_ACTION_PLAY")
print("▶️ Media playing")

# Pause
client.trigger_media_input_action(source_name, "OBS_WEBSOCKET_MEDIA_INPUT_ACTION_PAUSE")
print("⏸️ Media paused")

# Stop
client.trigger_media_input_action(source_name, "OBS_WEBSOCKET_MEDIA_INPUT_ACTION_STOP")
print("⏹️ Media stopped")