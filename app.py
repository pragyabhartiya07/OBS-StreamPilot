import streamlit as st
import obsws_python as obs
from obsws_python.error import OBSSDKRequestError
import time
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader


#--- here starts the whole CSS color gradient thingy---
st.markdown("""
<style>

/* SOLID CREAM BACKGROUND */
.stApp {
    background: #FFF9E5 !important;          /* Cream background */
}

/* SIDEBAR */
section[data-testid="stSidebar"] > div {
    background-color: #5B3734 !important;    /* Maroon-Brown, not harsh */
    border-right: none;
}
section[data-testid="stSidebar"] * {
    color: #FFF9E5 !important;               /* Cream text in sidebar */
}

/* HEADINGS */
h1, h2, h3 {
    color: #882A2A !important;               /* Accent maroon headings */
    font-weight: 700;
}

/* BUTTONS */
div.stButton > button {
    background-color: #882A2A !important;    /* Accent maroon */
    color: #FFF9E5 !important;               /* Cream text */
    border-radius: 8px;
    border: none;
    padding: 0.5rem 1.2rem;
    font-size: 16px;
    font-weight: 600;
    transition: background 0.2s;
}
div.stButton > button:hover {
    background-color: #5B3734 !important;    /* Slightly darker on hover */
    color: #FFF9E5 !important;
}

/* CARDS + DASHBOARD PANELS */
.card, [data-testid="stHorizontalBlock"] {
    background: #F8F5ED;
    border-radius: 16px;
    border: 1.5px solid #E7DACC;
    box-shadow: 0 2px 6px rgba(88,42,42,0.04);
    margin-bottom: 18px;
}

/* INPUTS */
input, textarea {
    background-color: #F8F5ED !important;
    border: 2px solid #A85C5C !important;
    color: #31201E !important;
}

/* ALERT / STATUS BOXES */
.stAlert {
    background-color: #E7DACC !important;
    border-left: 5px solid #A85C5C !important;
    color: #31201E !important;
}

</style>
""", unsafe_allow_html=True)


#-- yaha CSS khatam--


#--COMMAND FUNCTIONS--
def start_recording(client):
    client.start_record()

def stop_recording(client):
    client.stop_record()

def pause_recording(client):
    client.pause_record()

def resume_recording(client):
    client.resume_record()

def create_scene(client, scene_name: str):
    scene_name = scene_name.strip()
    if scene_name :
        try:
            client.create_scene(scene_name)
        except Exception as e:
            st.error(f"Failed to create scene: {e}")

def delete_scene(client, scene_name: str):
    scene_name = scene_name.strip()
    if scene_name:
        client.remove_scene(scene_name)

def switch_scene(client, scene_name: str):
    scene_name = scene_name.strip()
    if scene_name:
        client.set_current_program_scene(scene_name)
#--ENDING OF COMMAND FUNCTIONS--

#page title
st.set_page_config(
    page_title = "OBS StreamPilot",
    page_icon = "✈️"
)

#now, we check if the connection is already stored
if 'obs_client' not in st.session_state:
    st.session_state.obs_client = None

if 'view' not in st.session_state:
    st.session_state.view = 'welcome'

if 'is_streaming' not in st.session_state:
    st.session_state.is_streaming = False

#now we will set up the user authentication vali cheez
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

if not st.session_state.get('authentication_status'):
    #WELCOME PAGE
    if st.session_state.view == 'welcome':
        st.title("Welcome to OBS StreamPilot")
        st.write("Please Login or Create an account to continue.")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Login", use_container_width=True):
                st.session_state.view= 'login'
                st.rerun()
        
        with col2:
            if st.button("Sign up", use_container_width=True):
                st.session_state.view = 'signup'
                st.rerun()
    
    #--LOGIN PAGE--
    elif st.session_state.view == 'login':

        authenticator.login('main')   # only displays form

        auth_status = st.session_state.get("authentication_status")
        username = st.session_state.get("username")
        name = st.session_state.get("name")

        if auth_status == False:
            st.error("Incorrect username or password.")

        if auth_status == None:
            st.warning("Please enter username and password.")

        if auth_status:
            # Store role in session
            st.session_state['role'] = config['credentials']['usernames'][username]['role']
            st.session_state['name'] = name
            st.session_state.obs_client = None
            st.session_state.view = "connected"
            st.rerun()

        if st.button("Back"):
            st.session_state.view = 'welcome'
            st.rerun()


    #--SIGN UP--
    elif st.session_state.view == 'signup':
        try:
            if authenticator.register_user('main'):
                new_username = st.session_state['username']
                config['credentials']['usernames'][new_username]['role'] = "user"

                with open('config.yaml', 'w') as file:
                    yaml.dump(config, file)

                st.success("User registered successfully. You are a 'user' by default.")
                st.info("Go back and login now.")
        except Exception as e:
            st.error(e)

        if st.button("Back to Welcome"):
            st.session_state.view = 'welcome'
            st.rerun()



#if the user is logged in
elif st.session_state.get('authentication_status'):
    #login screen which is the first screen
    if st.session_state.obs_client is None:
        st.title(f"Welcome, *{st.session_state.name}*!")
        
        st.info(f"Logged in as: {st.session_state['role'].upper()}")
        #--- dahsboard ka code is here---
        st.markdown("""
            <div style="
                background:#fff5e4;
                padding: 25px;
                border-radius: 18px;
                border: 1px solid #ffc4c4;
                margin-top: 10px;
                margin-bottom: 25px;
            ">
                <h1 style="color:#850e35; margin-bottom:5px;">OBS StreamPilot Dashboard</h1>
                <p style="color:#850e35; font-size:16px; margin-top:0;">
                    Control your OBS Studio with a clean, elegant interface.
                </p>
            </div>
        """, unsafe_allow_html=True)

        st.header("Connect to OBS")
        st.markdown("Enter your OBS Websocket details below.")

        #now, we create the forms vali cheez
        host = st.text_input("Host (IP Address)", "localhost")
        port = st.number_input("Port", 1, 65535, 4455)
        password = st.text_input("Password", type="password")

        #create the connect button
        if st.button("Connect", use_container_width=True):
            st.info("Connecting to OBS..")

            try:
                client = obs.ReqClient(
                    host = host,
                    port = int(port),
                    password = password
                )
                
                st.success("Connection successful")
                st.session_state.obs_client = client
                st.session_state['obs_password'] = password
                time.sleep(1)
                st.rerun()

            except Exception as e:
                st.error(f"An unknown error occurred: {e}")
        
    #this else runs only if the connection is found
    else:
        client = st.session_state.obs_client

        # ----------------------- SIDEBAR DESIGN -----------------------
        with st.sidebar:
            st.markdown("""
            <div style="
                background-color:#fff5e4; 
                padding:20px; 
                border-radius:15px;
                border:1px solid #ffc4c4;
                text-align:center;
            ">
                <h3 style="color:#850e35;">🌸 StreamPilot</h3>
                <p style="color:#850e35; font-size:14px;">Welcome, Pragya!</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("### 🧭 Navigation")
            st.markdown("- Dashboard")
            st.markdown("- Scenes")
            st.markdown("- Recording")
            st.markdown("- Settings")
            st.markdown("---")

            st.markdown("### 🔌 Connection")
            authenticator.logout('Logout')

            if st.button("Disconnect from OBS"):
                client.disconnect()
                st.session_state.obs_client = None
                st.rerun()

            #----- voice assistant aa gya ishar ab-----
            import subprocess

            st.markdown("### 🎙 Voice Assistant")

            # --- START VOICE ASSISTANT ---
            if st.button("Start Voice Assistant"):
                obs_pass = st.session_state.get('obs_password', "")
                st.session_state['va_process'] = subprocess.Popen([
                    r"D:\College\5th semester\OBS StreamPilot\venv\Scripts\python.exe",
                    "voice_assistant.py",
                    st.session_state['obs_password']
                ])
                st.success("Voice Assistant started! Say 'Hi Nadia' to wake her.")


            # --- STOP VOICE ASSISTANT ---
            if st.button("Stop Voice Assistant"):
                if 'va_process' in st.session_state:
                    st.session_state['va_process'].terminate()
                    st.session_state['va_process'] = None
                    st.success("Voice Assistant stopped.")
                else:
                    st.warning("Voice Assistant is not running.")


        # ----------------------- RECORDING CARD -----------------------
        st.markdown("""
        <div style="
            background:#fff5e4;
            padding:20px;
            border-radius:18px;
            border:1px solid #ffc4c4;
            margin-bottom:25px;
        ">
            <h2 style="color:#850e35; margin-top:0;">🎥 Recording Controls</h2>
        </div>
        """, unsafe_allow_html=True)

        rec1, rec2, rec3, rec4 = st.columns(4)
        with rec1:
            if st.button("Start Recording"):
                start_recording(client)
                st.success("Recording started.")
        with rec2:
            if st.button("Stop Recording"):
                stop_recording(client)
                st.success("Recording stopped.")
        with rec3:
            if st.button("Pause Recording"):
                pause_recording(client)
                st.info("Recording paused.")
        with rec4:
            if st.button("Resume Recording"):
                resume_recording(client)
                st.success("Recording resumed.")

        # ----------------------- STREAMING CARD (SIMULATED) -----------------------
        st.markdown("""
        <div style="
            background:#fff5e4;
            padding:20px;
            border-radius:18px;
            border:1px solid #ffc4c4;
            margin-bottom:25px;
        ">
            <h2 style="color:#850e35; margin-top:0;">📡 Streaming Controls</h2>
        </div>
        """, unsafe_allow_html=True)

        col_s1, col_s2 = st.columns(2)
        with col_s1:
            if st.button("Start Streaming"):
                if not st.session_state.is_streaming:
                    st.session_state.is_streaming = True
                    st.success("Streaming started (simulated).")
                else:
                    st.info("Already streaming.")
        with col_s2:
            if st.button("Stop Streaming"):
                if st.session_state.is_streaming:
                    st.session_state.is_streaming = False
                    st.warning("Streaming stopped (simulated).")
                else:
                    st.info("Not currently streaming.")

        # ----------------------- SCENE CONTROLS CARD -----------------------
        st.markdown("""
        <div style="
            background:#fff5e4;
            padding:20px;
            border-radius:18px;
            border:1px solid #ffc4c4;
            margin-bottom:25px;
        ">
            <h2 style="color:#850e35; margin-top:0;">🎬 Scene Controls</h2>
        </div>
        """, unsafe_allow_html=True)

        scene_name = st.text_input("Scene name", key="scene_name_input")

        sc1, sc2, sc3 = st.columns(3)
        with sc1:
            if st.button("Create Scene"):
                if scene_name:
                    create_scene(client, scene_name)
                    st.success(f"Scene '{scene_name}' created.")
                else:
                    st.warning("Please enter a scene name.")
        with sc2:
            if st.button("Delete Scene"):
                if scene_name:
                    delete_scene(client, scene_name)
                    st.success(f"Scene '{scene_name}' deleted.")
                else:
                    st.warning("Please enter a scene name.")
        with sc3:
            if st.button("Switch to Scene"):
                if scene_name:
                    switch_scene(client, scene_name)
                    st.success(f"Switched to scene '{scene_name}'.")
                else:
                    st.warning("Please enter a scene name.")

        # ----------------------- ADD CAMERA SOURCE CARD -----------------------
        st.markdown("""
        <div style="
            background:#F8F5ED;
            padding:20px;
            border-radius:18px;
            border:1px solid #E7DACC;
            margin-bottom:25px;
        ">
            <h2 style="color:#850E35; margin-top:0;">🎥 Add Camera Source</h2>
            <p style="color:#31201E;">Add your webcam as a source inside any scene.</p>
        </div>
        """, unsafe_allow_html=True)

        cam_scene = st.text_input("Scene Name (where camera should be added)", key="cam_scene")
        cam_source = st.text_input("Source Name (camera input name)", key="cam_source")

        resolution = st.selectbox(
            "Resolution",
            ["640x480", "1280x720", "1920x1080"],
            index=2
        )
        fps = st.selectbox("FPS", [24, 30, 60], index=1)

        if st.button("Add Camera Source"):
            if not cam_scene or not cam_source:
                st.warning("Please enter both scene name and source name.")
            else:
                try:
                    settings = {
                        "device_id": 0,
                        "resolution": resolution,
                        "fps": fps
                    }
                    client.create_input(
                        cam_scene,
                        cam_source,
                        "av_capture_input",   # camera input kind
                        settings,
                        True
                    )
                    st.success(f"Camera '{cam_source}' added to scene '{cam_scene}'.")
                except Exception as e:
                    st.error(f"Failed to add camera: {e}")

        # ----------------------- COUNTDOWN SCENE SWITCH CARD -----------------------
        st.markdown("""
        <div style="
            background:#F8F5ED;
            padding:20px;
            border-radius:18px;
            border:1px solid #E7DACC;
            margin-bottom:25px;
        ">
            <h2 style="color:#850E35; margin-top:0;">⏳ Countdown Scene Switch</h2>
            <p style="color:#31201E;">Automatically switch to a scene after a timer.</p>
        </div>
        """, unsafe_allow_html=True)

        countdown_seconds = st.number_input(
            "Countdown Seconds",
            min_value=1,
            max_value=300,
            value=10
        )
        countdown_target_scene = st.text_input("Target Scene Name", key="countdown_scene")

        if st.button("Start Countdown"):
            if not countdown_target_scene:
                st.warning("Please enter a target scene name.")
            else:
                st.info(f"⏳ Countdown started: switching in {countdown_seconds} seconds…")
                with st.spinner("Countdown running…"):
                    time.sleep(countdown_seconds)
                try:
                    client.set_current_program_scene(countdown_target_scene)
                    st.success(f"✅ Scene switched to '{countdown_target_scene}'.")
                except Exception as e:
                    st.error(f"Failed to switch scene: {e}")
