import obsws_python as obs
import time

client = obs.ReqClient(host="localhost", port=4455, password="cocobaby@130306")

seconds = 10
target_scene = "Intro"

print(f"⏳ Countdown {seconds}s → switch to {target_scene}")
time.sleep(seconds)

client.set_current_program_scene(target_scene)
print(f"✅ Scene switched to {target_scene}")