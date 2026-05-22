import obsws_python as obs

client = obs.ReqClient(host="localhost", port=4455, password="cocobaby@130306")

scene_name = "manasvi"
source_name = "v1"
file_path = "/Users/manasvisharma/Videos/intro.mp4"  


client.create_input(
    scene_name,                     
    source_name,                    
    "ffmpeg_source",               
    {"local_file": file_path, "looping": False, "is_local_file": True},  # Input settings
    True                            
)

print(f"🎵 Media source '{source_name}' added to scene '{scene_name}'")
