import obsws_python as obs

# Take scene name from user
scene_name = input("Enter the name of the new scene: ").strip()

# Create scene
client = obs.ReqClient(host="localhost", port=4455, password="cocobaby@130306")
client.create_scene(scene_name)
print(f"✅ Scene '{scene_name}' created successfully")



