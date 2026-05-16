import streamlit as st
from groq import Groq
import base64

# 1. Initialize Groq Client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("Treasure AI")

# 2. System Prompt
system_prompt = (
    "Your name is Treasure. You are a brilliant, adaptive AI collaborator. "
    "The current year is 2026. Always ensure your answers reflect this time context accurately. "
    "Structure your answers beautifully using bold headers, horizontal rules, and bullet points."
)

# 3. Initialize Session State for Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Sidebar Image Uploader
st.sidebar.title("Multimedia Settings")
uploaded_image = st.sidebar.file_uploader("Upload an image for Treasure to see", type=["png", "jpg", "jpeg"])

# Display the uploaded image in the sidebar if present
if uploaded_image:
    st.sidebar.image(uploaded_image, caption="Uploaded Image", use_container_width=True)

# Helper function to convert image to Base64 string for Groq Vision API
def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# 5. Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Chat Input
if user_input := st.chat_input("Ask Treasure anything..."):
    # Append user message to display chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate Response from Groq
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            # Dynamically select model and format payload based on image upload
            if uploaded_image:
                model_to_use = "llama-3.2-11b-vision-preview"
                base64_image = encode_image(uploaded_image)
                
                # Vision structure payload
                formatted_messages = [
                    {"role": "system", "content": system_prompt},
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": user_input},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ]
            else:
                model_to_use = "llama-3.1-8b-instant"
                # Standard text-only history payload
                formatted_messages = [{"role": "system", "content": system_prompt}] + [
                    {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
                ]

            # Send request to Groq Cloud
            completion = client.chat.completions.create(
                model=model_to_use,
                messages=formatted_messages,
                temperature=0.3,
            )
            
            response_text = completion.choices[0].message.content
            message_placeholder.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})

        except Exception as e:
            message_placeholder.markdown(f"An error occurred: {e}")
