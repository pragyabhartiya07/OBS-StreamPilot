import customtkinter as ctk
from tkinter import messagebox
import obsws_python as obs

# ==============================
# 🌐 Connect to OBS WebSocket
# ==============================
try:
    client = obs.ReqClient(host="localhost", port=4455, password="cocobaby@130306")
    obs_connected = True
except Exception as e:
    obs_connected = False
    print("⚠️ Could not connect to OBS:", e)

# ==============================
# 🎨 App Setup
# ==============================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")  # Try: "blue", "dark-blue", "green"

app = ctk.CTk()
app.title("🎥 OBS StreamPilot - The Futuristic Controller")
app.geometry("880x580")

# ==============================
# 🌈 Background Styling (Gradient)
# ==============================
background = ctk.CTkFrame(app, fg_color=("gray10", "gray10"), corner_radius=0)
background.pack(fill="both", expand=True)

# ==============================
# 🎬 Title and Status
# ==============================
title_label = ctk.CTkLabel(
    background,
    text="🚀 OBS StreamPilot",
    font=ctk.CTkFont(size=32, weight="bold"),
    text_color="#00FFF5"
)
title_label.pack(pady=(25, 10))

status_color = "#00FF00" if obs_connected else "#FF4C4C"
status_text = "🟢 Connected to OBS" if obs_connected else "🔴 Not Connected"

status_label = ctk.CTkLabel(
    background,
    text=status_text,
    font=ctk.CTkFont(size=16, weight="bold"),
    text_color=status_color
)
status_label.pack(pady=(0, 20))

# ==============================
# 🔤 Input Fields (Scene + Source)
# ==============================
frame_inputs = ctk.CTkFrame(background, fg_color="#1A1A1A", corner_radius=15)
frame_inputs.pack(padx=40, pady=10, fill="x")

scene_entry = ctk.CTkEntry(frame_inputs, placeholder_text="Enter Scene Name")
scene_entry.pack(side="left", padx=20, pady=15, expand=True)

source_entry = ctk.CTkEntry(frame_inputs, placeholder_text="Enter Source Name")
source_entry.pack(side="left", padx=20, pady=15, expand=True)

# ==============================
# ⚙️ Helper Functions
# ==============================
def notify(msg, title="OBS StreamPilot"):
    messagebox.showinfo(title, msg)

def start_recording():
    try:
        client.start_record()
        notify("✅ Recording started successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"❌ {e}")

def stop_recording():
    try:
        client.stop_record()
        notify("🛑 Recording stopped.")
    except Exception as e:
        messagebox.showerror("Error", f"❌ {e}")

def create_scene():
    scene = scene_entry.get().strip()
    if not scene:
        messagebox.showwarning("Input Missing", "Please enter a scene name.")
        return
    try:
        client.create_scene(scene)
        notify(f"✅ Scene '{scene}' created.")
        scene_entry.delete(0, "end")
    except Exception as e:
        messagebox.showerror("Error", f"❌ {e}")

def switch_scene():
    scene = scene_entry.get().strip()
    if not scene:
        messagebox.showwarning("Input Missing", "Please enter a scene name.")
        return
    try:
        client.set_current_program_scene(scene)
        notify(f"🎬 Switched to scene '{scene}'")
    except Exception as e:
        messagebox.showerror("Error", f"❌ {e}")

def toggle_source(show=True):
    scene = scene_entry.get().strip()
    source = source_entry.get().strip()
    if not scene or not source:
        messagebox.showwarning("Input Missing", "Enter both scene and source names.")
        return
    try:
        scene_items = client.get_scene_item_list(scene).scene_items
        scene_item_id = next((item.scene_item_id for item in scene_items if item.source_name == source), None)
        if scene_item_id:
            client.set_scene_item_enabled(scene, scene_item_id, show)
            action = "👁️ shown" if show else "🙈 hidden"
            notify(f"✅ Source '{source}' {action} in '{scene}'.")
        else:
            messagebox.showerror("Error", "Source not found in scene.")
    except Exception as e:
        messagebox.showerror("Error", f"❌ {e}")

# ==============================
# 🧭 Button Panel
# ==============================
frame_buttons = ctk.CTkFrame(background, fg_color="#0F2027", corner_radius=20)
frame_buttons.pack(padx=60, pady=25, fill="both", expand=True)

buttons = [
    ("🎬 Start Recording", start_recording, "#00ADB5"),
    ("⏹ Stop Recording", stop_recording, "#FF4C4C"),
    ("➕ Create Scene", create_scene, "#39FF14"),
    ("🔄 Switch Scene", switch_scene, "#6C63FF"),
    ("🙈 Hide Source", lambda: toggle_source(False), "#F15BB5"),
    ("👁️ Show Source", lambda: toggle_source(True), "#00FFAB")
]

for text, cmd, color in buttons:
    btn = ctk.CTkButton(
        frame_buttons,
        text=text,
        command=cmd,
        fg_color=color,
        hover_color="#121212",
        height=45,
        corner_radius=15,
        font=ctk.CTkFont(size=16, weight="bold")
    )
    btn.pack(pady=10, padx=60, fill="x")

# ==============================
# 🧠 Footer
# ==============================
footer = ctk.CTkLabel(
    background,
    text="💡 Developed by Manasvi, Pragya, Palak | OBS StreamPilot 2025",
    font=ctk.CTkFont(size=12, weight="normal"),
    text_color="#999999"
)
footer.pack(side="bottom", pady=15)

# ==============================
# 🚀 Run the App
# ==============================
app.mainloop()
