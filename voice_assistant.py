#OpEZfgKanMmT7JEi

import sounddevice as sd
import soundfile as sf
import numpy as np
import speech_recognition as sr
import pyttsx3
import obsws_python as obs
from obsws_python.error import OBSSDKRequestError

print(sd.query_devices())

import sys
obs_password = sys.argv[1] if len(sys.argv) > 1 else ""

# PREVENT STREAMLIT FROM RUNNING THIS SCRIPT ON IMPORT

import __main__
if hasattr(__main__, "__file__") and "streamlit" in __main__.__file__:
    # If Streamlit is importing this file, STOP execution here.
    raise SystemExit("Voice assistant loaded (import only), not running.")


# --------- CONNECT TO OBS ---------
client = obs.ReqClient(
    host="localhost",
    port=4455,
    password= obs_password
)

# --------- TEXT TO SPEECH ENGINE ---------
engine = pyttsx3.init()
engine.setProperty("rate", 170)

def speak(text):
    print("Nadia:", text)
    engine.say(text)
    engine.runAndWait()

# --------- LISTEN USING sounddevice ---------
def listen(device_index=1):
    fs = 48000          # use correct sample rate
    duration = 4.5

    print("Listening...")

    try:
        recording = sd.rec(
            int(duration * fs),
            samplerate=fs,
            channels=1,
            device=device_index   # now device_index exists
        )
        sd.wait()

        sf.write("temp.wav", recording, fs)

        recognizer = sr.Recognizer()
        with sr.AudioFile("temp.wav") as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio, language="en-IN", show_all=False)
            return text.lower()

    except Exception as e:
        print("Recognition error:", e)
        return ""

# --------- EXECUTE COMMANDS ---------
def execute_command(command):
    if "start recording" in command:
        client.start_record()
        speak("Recording started.")

    elif "stop recording" in command:
        client.stop_record()
        speak("Recording stopped.")

    elif "pause recording" in command:
        client.pause_record()
        speak("Recording paused.")

    elif "resume recording" in command:
        client.resume_record()
        speak("Recording resumed.")

    elif "start streaming" in command:
        try:
            client.start_stream()
            speak("Streaming started.")
        except OBSSDKRequestError:
            speak("Cannot start streaming. Check OBS settings.")

    elif "stop streaming" in command:
        try:
            client.stop_stream()
            speak("Streaming stopped.")
        except OBSSDKRequestError:
            speak("Streaming is not active.")

    elif "switch to" in command:
        scene = command.replace("switch to", "").strip().title()
        client.set_current_program_scene(scene)
        speak(f"Switched to scene {scene}.")

    elif "exit" in command or "goodbye" in command:
        speak("Goodbye Pragya.")
        return False

    else:
        speak("I did not understand that.")

    return True

# --------- WAKE WORD DETECTION ---------
def wait_for_wake_word():
    speak("Voice assistant ready. Say 'Hi Nadia' to activate.")
    while True:
        text = listen(device_index=9)
        if "hi nadia" in text or "hey nadia" in text:
            speak("Hello Pragya, I'm listening.")
            return
    if text.strip() == "stop nadia":
        speak("Stopping voice assistant.")
        sys.exit()


# --------- COMMAND MODE ---------
def command_mode():
    speak("You may give commands now.")
    while True:
        text = listen()
        print("Heard:", text)
        if not execute_command(text):
            break
    if text.strip() == "stop nadia":
        speak("Stopping voice assistant.")
        sys.exit()


# Disable auto-run so Streamlit doesn't import and execute this file.
# Streamlit will start the assistant ONLY when you click the button.

if __name__ == "__main__":
    wait_for_wake_word()
    command_mode()
