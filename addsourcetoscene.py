import obsws_python as obs

client = obs.ReqClient(host="localhost", port=4455, password="cocobaby@130306")

scene_name = "Scene 2"
source_name = "My_Camera"
source_kind = "av_capture_input"   # Correct for Mac

# To see available devices on Mac:
# client.get_input_properties("av_capture_input") or use OBS device dropdown

settings = {
    "device_id": 0,      # Usually 0 for default webcam
    "resolution": "1920x1080",  # Optional
    "fps": 30                 # Optional
}

client.create_input(scene_name, source_name, source_kind, settings, True)

print(f"✅ Added source '{source_name}' to scene '{scene_name}'")
