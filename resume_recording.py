import obsws_python as obs

client = obs.ReqClient(host="localhost", port=4455, password="manasvi@123")
client.resume_record()
print("▶️ Recording resumed")