import obsws_python as obs
import time
import schedule   

client = obs.ReqClient(host="localhost", port=4455, password="cocobaby@130306")

def start_recording():
    client.start_record()
    print("🎬 Recording started")

def stop_recording():
    client.stop_record()
    print("🛑 Recording stopped")

# Example: start at 9:00 AM, stop at 9:30 AM
schedule.every().day.at("09:00").do(start_recording)
schedule.every().day.at("09:30").do(stop_recording)

print("🕒 Waiting for scheduled tasks...")
while True:
    schedule.run_pending()
    time.sleep(1)
