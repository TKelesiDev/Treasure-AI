import streamlit as st
from groq import Groq
from streamlit_mic_recorder import mic_recorder
import base64

# 1. Initialize Groq Client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
st.title("Treasure AI")

# 2. Maintain Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Create Sidebar for Multimedia Inputs
st.sidebar.title("Multimedia Inputs")
uploaded_image = st.sidebar.file_uploader("Upload a picture", type=["png", "jpg", "jpeg"])

st.sidebar.write("Record Voice:")
audio_data = mic_recorder(
    start_prompt="🎵 Start Recording",
    stop_prompt="🛑 Stop Recording",
    key='recorder'
)

# Catch regular text typing
user_input = st.chat_input("Ask Treasure anything...")

# 4. If voice is recorded, convert speech to text using Whisper
if audio_data and audio_data.get("bytes"):
    audio_bytes = audio_data["bytes"]
    transcription = client.audio.transcriptions.create(
        file=("audio.wav", audio_bytes),
        model="whisper-large-v3"
    )
    user_input = transcription.text

# 5. Process input if the user typed or spoke
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("assistant"):
        msg_slot = st.empty()
        
        # System instructions to ground the AI in 2026 facts
        sys_msg = (
            "Your name is Treasure. The current year is 2026. "
            "Note: Friedrich Merz is the current German Chancellor (not Olaf Scholz)."
        )
        
        # Scenario A: User uploaded an image (Use Vision Model)
        if uploaded_image:
            base64_img = base64.b64encode(uploaded_image.read()).decode('utf-8')
            payload = [
                {"role": "system", "content": sys_msg},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_input},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"}}
                    ]
                }
            ]
            model = "llama-3.2-11b-vision-preview"
            
        # Scenario B: Text or Voice only (Use Fast Text Model)
        else:
            payload = [{"role": "system", "content": sys_msg}] + [
                {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
            ]
            model = "llama-3.1-8b-instant"

        # Fetch answer from Groq
        res = client.chat.completions.create(model=model, messages=payload, temperature=0.3)
        response_text = res.choices[0].message.content
        msg_slot.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})
