import obsws_python as obs

client = obs.ReqClient(host="localhost", port=4455, password="cocobaby@130306")

sources = client.get_input_list()
print("🎙️ Available sources:")
for s in sources.inputs:
    print(" -", s['inputName'], "(", s['inputKind'], ")")