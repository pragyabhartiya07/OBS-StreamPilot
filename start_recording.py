import obsws_python as obs
client = obs.ReqClient(host="localhost", port=4455, password="manasvi@123")
client.start_record()
print("✅ Recording started")