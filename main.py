import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables safely
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.error("⚠️ Missing Google API Key! Please check your .env file.")
    st.stop()

# Configure Streamlit page settings
st.set_page_config(page_title="Chat with Gemini-Pro!", page_icon="🤖", layout="centered")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-2.0-flash')

# Function to send a message and handle errors
def get_gemini_response(user_input):
    try:
        response = st.session_state.chat_session.send_message(user_input)
        return response.text
    except Exception as e:
        st.error(f"⚠️ Error sending message: {e}")
        return "Sorry, I couldn't process your request."

# Initialize chat session in Streamlit if not present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Display chatbot title
st.title("🤖 Kettavan - ChatBot")

# Show chat history
for message in st.session_state.chat_session.history:
    with st.chat_message("assistant" if message.role == "model" else message.role):
        st.markdown(message.parts[0].text)

# User input field
user_prompt = st.chat_input("Ask Gemini-Pro...")
if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    gemini_response = get_gemini_response(user_prompt)

    with st.chat_message("assistant"):
        st.markdown(gemini_response)
