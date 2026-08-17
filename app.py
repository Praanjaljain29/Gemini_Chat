import os

from dotenv import load_dotenv
from google import genai
import streamlit as st
from google.genai import types


# -------------------------
# Gemini client
# -------------------------

def create_gemini_client():
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        st.error("GEMINI_API_KEY is not configured.")
        st.stop()

    return genai.Client(api_key=api_key)


# -------------------------
# Session state
# -------------------------

def initialize_session():
    if "messages" not in st.session_state:
        st.session_state.messages = []


# -------------------------
# Display chat history
# -------------------------

def display_messages():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])


# -------------------------
# Convert messages to
# Gemini format
# -------------------------

def build_contents():
    contents = []

    for message in st.session_state.messages:
        contents.append({
            "role": message["role"],
            "parts": [
                {
                    "text": message["content"]
                }
            ]
        })

    return contents


# -------------------------
# Stream Gemini response
# -------------------------

def generate_response(
    client,
    model,
    contents,
    max_tokens,
    system_prompt
):
    response_stream = client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=types.GenerateContentConfig(
            max_output_tokens=max_tokens,
            system_instruction=system_prompt
        )
    )

    for chunk in response_stream:
        if chunk.text:
            yield chunk.text


# -------------------------
# Application setup
# -------------------------

client = create_gemini_client()

initialize_session()


# -------------------------
# UI
# -------------------------

st.title("🤖 Gemini Chat")

st.sidebar.title("Settings")


model = st.sidebar.selectbox(
    "Model",
    [
        "gemini-3.6-flash",
        "gemini-3.5-flash"
    ]
)


max_tokens = st.sidebar.slider(
    "Maximum response length",
    min_value=100,
    max_value=2000,
    value=1000,
    step=100
)


system_prompt = st.sidebar.text_area(
    "System Prompt",
    value="You are a helpful AI assistant."
)


if st.sidebar.button("🧹 Clear Chat"):
    st.session_state.messages = []
    st.rerun()


# -------------------------
# Display existing history
# -------------------------

display_messages()


# -------------------------
# User input
# -------------------------

prompt = st.chat_input("Type a message...")


if prompt:

    # Store user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })


    # Display user message
    with st.chat_message("user"):
        st.write(prompt)


    # Build Gemini conversation
    contents = build_contents()


    # Generate and stream response
    try:

        with st.chat_message("assistant"):
            response_text = st.write_stream(
                generate_response(
                    client,
                    model,
                    contents,
                    max_tokens,
                    system_prompt
                )
            )

        # Store Gemini response
        st.session_state.messages.append({
            "role": "model",
            "content": response_text
        })

    except Exception:
        st.error("Sorry, I couldn't generate a response.")