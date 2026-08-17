# Gemini Chat Assistant

A lightweight Streamlit chatbot powered by Google's Gemini API.

## Features

- Conversational memory
- Streaming responses
- System prompts
- Model selection
- Response length control
- Clear chat
- Error handling

## Tech Stack

- Python
- Streamlit
- Google Gemini API
- python-dotenv

## Architecture

User
 ↓
Streamlit
 ↓
Session State
 ↓
Gemini API
 ↓
Streaming Response
 ↓
Streamlit UI

## Setup

1. Clone the repository
2. Create virtual environment
3. Install dependencies
4. Add Gemini API key
5. Run Streamlit

## Environment Variables

GEMINI_API_KEY=your_api_key

## Run

streamlit run app.py