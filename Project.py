import streamlit as st
from openai import OpenAI

# 1. Setup the Web Page Layout and Title
st.set_page_config(page_title="Treasure", page_icon="💎")
st.title("💎 Treasure")
st.write("Welcome! I am Treasure, your fast, cloud-powered AI assistant.")

# 2. Safely grab your secret OpenAI API key from the server
# Streamlit will read the key you paste into the "Secrets" box later!
API_KEY = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=API_KEY)

# 3. Define Treasure's Persona for School
system_prompt = (
    "Your name is Treasure. You are an expert school presentation assistant. "
    "Your goal is to provide highly accurate, factually correct, and clear information. "
    "Always use clean formatting like bolding, bullet points, and headers effectively to make your responses "
    "easy to read. Keep your answers brief, engaging, and perfect for school research."
)

# 4. Initialize Conversation History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 5. Handle User Input
if user_input := st.chat_input("Ask Treasure anything..."):
    # Display user's message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate Treasure's response instantly via the cloud
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
       # Look for the key safely in the environment or Streamlit settings
api_key = os.environ.get("OPENAI_API_KEY")

if not api_key and "OPENAI_API_KEY" in st.secrets:
    api_key = st.secrets["OPENAI_API_KEY"]

client = OpenAI(api_key=api_key)
                model="gpt-4o-mini", 
                messages=api_messages,
                temperature=0.3 # Low temperature forces the AI to stick strictly to real facts
            )
            
            treasure_reply = response.choices[0].message.content
            message_placeholder.markdown(treasure_reply)
            
            # Save Treasure's reply to history
            st.session_state.messages.append({"role": "assistant", "content": treasure_reply})
            
        except Exception as e:
            message_placeholder.markdown(f"⚠️ Error connecting to Treasure: {e}")