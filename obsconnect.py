# obs_connect.py
import obsws_python as obs

def connect():
    try:
        client = obs.ReqClient(host="localhost", port=4455, password="cocobaby@130306")
        print("✅ Connected to OBS successfully!")
        return client
    except Exception as e:
        print("❌ Connection failed:", e)
        return None
