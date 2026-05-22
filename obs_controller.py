from obswebsocket import obsws, requests
import sqlite3
from datetime import datetime

# OBS WebSocket connection
host = "localhost"
port = 4455
password = "cocobaby@130306"
ws = obsws(host, port, password)
ws.connect()
print("✅ Connected to OBS")

# Start Recording
def start_recording():
    ws.call(requests.StartRecord())
    print("🎥 Recording Started")

# Stop Recording + Save to DB
def stop_recording():
    response = ws.call(requests.StopRecord())
    filepath = response.getOutputPath()

    # Save in SQLite DB
    conn = sqlite3.connect("recordings.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS recordings
                 (filename TEXT, date TEXT)''')
    c.execute("INSERT INTO recordings VALUES (?, ?)",
              (filepath, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    print(f"🛑 Recording Stopped | File saved at: {filepath}")

# Example usage
start_recording()
input("Press Enter to stop...")
stop_recording()

ws.disconnect()
