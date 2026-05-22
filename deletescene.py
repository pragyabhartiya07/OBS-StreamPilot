import obsws_python as obs

client = obs.ReqClient(host="localhost", port=4455, password="cocobaby@130306")

scene_name = "palak"
client.remove_scene(scene_name)

print(f"🗑️ Scene deleted: {scene_name}")