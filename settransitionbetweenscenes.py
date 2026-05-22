import obsws_python as obs

client = obs.ReqClient(host="localhost", port=4455, password="cocobaby@130306")

transition_name = "Fade"   # or "Cut", "Swipe", "Slide"
duration = 500  # ms

client.set_current_scene_transition(transition_name)
client.set_current_scene_transition_duration(duration)

print(f"🔄 Transition set: {transition_name} ({duration} ms)")