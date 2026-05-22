import obsws_python as obs
import time

client = obs.ReqClient(host="localhost", port=4455, password="YOUR_PASSWORD")

scenes = client.get_scene_list().scenes
scene_names = [s["sceneName"] for s in scenes]

print("🎬 Scenes available:", scene_names)

delay = 5  # seconds between switches

while True:
    for scene in scene_names:
        client.set_current_program_scene(scene)
        print(f"🔄 Switched to scene: {scene}")
        time.sleep(delay)