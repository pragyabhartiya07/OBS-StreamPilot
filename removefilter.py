import obsws_python as obs

client = obs.ReqClient(host="localhost", port=4455, password="cocobaby@130306")

source_name = "My_Camera"
filter_name = "Grayscale_Filter"

client.remove_source_filter(source_name, filter_name)
print(f"🗑️ Removed filter '{filter_name}' from source '{source_name}'")