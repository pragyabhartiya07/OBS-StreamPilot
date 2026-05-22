import obsws_python as obs

client = obs.ReqClient(host="localhost", port=4455, password="cocobaby@130306")

source_name = "My_Camera"
filter_name = "Grayscale_Filter"
filter_kind = "color_filter"   # OBS filter type
settings = {"hue_shift": 0, "saturation": 0}  # Example: grayscale

client.create_source_filter(source_name, filter_name, filter_kind, settings)
print(f"🎨 Added filter '{filter_name}' to source '{source_name}'")