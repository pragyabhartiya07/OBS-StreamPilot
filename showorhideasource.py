import obsws_python as obs

# Connect to OBS WebSocket
client = obs.ReqClient(host="localhost", port=4455, password="cocobaby@130306")

scene_name = "Scene 2"
source_name = "camera"

# Function to get numeric sceneItemId from source name
def get_scene_item_id(scene_name, source_name):
    scene_items_data = client.get_scene_item_list(scene_name)
    # Access the sceneItems attribute
    for item in scene_items_data.sceneItems:
        if item.sourceName == source_name:
            return item.sceneItemId
    raise ValueError(f"Source '{source_name}' not found in scene '{scene_name}'")

# Get the sceneItemId
scene_item_id = get_scene_item_id(scene_name, source_name)

# Hide the source
client.set_scene_item_enabled(scene_name, scene_item_id, False)
print(f"🙈 Hidden source '{source_name}'")

# Show the source
client.set_scene_item_enabled(scene_name, scene_item_id, True)
print(f"👁️ Shown source '{source_name}'")
