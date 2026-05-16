import streamlit as st
from groq import Groq

# 1. Setup the Web Page Layout and Title
st.set_page_config(page_title="Treasure", page_icon="💎", layout="centered")
st.title("💎 Treasure")
st.write("Welcome! I am Treasure, your fast, cloud-powered AI assistant.")

# 2. Securely get the Groq API key from your secrets.toml file
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=GROQ_API_KEY)
except Exception:
    st.error("Missing Groq API Key. Please configure it in your secrets file.")
    st.stop()

# 3. Define Treasure's Persona
system_prompt = (
    "Your name is Treasure. You are a brilliant, adaptive AI collaborator. "
    "Your goal is to address the user's true intent with insightful, clear, and highly scannable responses. "
    "Do not restrict your length if a deep explanation is needed to touch every corner of a topic, but avoid fluff. "
    "Structure your answers beautifully using bold headers, horizontal rules, and bullet points. "
    "Be direct, authentic, and efficient. Once the question is fully answered, stop generating text."
)

# 4. Initialize Conversation History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! What's up? What can I help you with today?"}
    ]

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Handle User Input
if user_input := st.chat_input("Ask Treasure anything..."):
    # Append and display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate Treasure's response using Groq Cloud
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            # Build history payload including the system prompt at the top
            formatted_messages = [{"role": "system", "content": system_prompt}] + [
                {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
            ]
            
            # Send to Groq using their fast, free model
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=formatted_messages,
                temperature=0.3,
            )
            
            treasure_reply = completion.choices[0].message.content
            
            # Show the reply on screen and save it to history
            message_placeholder.markdown(treasure_reply)
            st.session_state.messages.append({"role": "assistant", "content": treasure_reply})
            
        except Exception as e:
            message_placeholder.markdown(f"⚠️ Error connecting to Treasure engine: {e}")
