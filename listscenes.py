import obsws_python as obs

client = obs.ReqClient(host="localhost", port=4455, password="cocobaby@130306")

scenes = client.get_scene_list()
print("🎬 Available scenes:")
for s in scenes.scenes:
    print(" -", s['sceneName'])