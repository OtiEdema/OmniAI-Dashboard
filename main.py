import streamlit as st
import time
from datetime import datetime
from collections import defaultdict
import openai
import os
import random
import pandas as pd
import tempfile
from io import BytesIO
import base64
import soundfile as sf

# Load OpenAI API Key from secrets or env
openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")

# App Configuration
st.set_page_config(page_title="OmniAI Dashboard", layout="wide")
st.title("🤖 OmniAI: The Autonomous Company Dashboard")

# CSS enhancements
st.markdown("""
    <style>
        .reportview-container {
            background-color: #0e1117;
            color: #d1d5db;
        }
        .stButton>button {
            background-color: #2563eb;
            color: white;
            font-weight: bold;
        }
        .stDownloadButton>button {
            background-color: #059669;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# Role colours
role_colors = {
    "executive": "#FFD700",
    "engineering": "#1f77b4",
    "product": "#ff7f0e",
    "marketing": "#2ca02c",
    "design": "#9467bd",
    "project-management": "#8c564b",
    "studio-operations": "#e377c2",
    "testing": "#7f7f7f",
    "sales": "#17becf",
    "finance": "#bcbd22",
    "legal": "#d62728",
    "publicity": "#17becf"
}

chat_log = []
usage_counter = defaultdict(int)

st.sidebar.header("🧠 Select an AI Agent")

language_map = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Chinese": "zh",
    "Arabic": "ar"
}

selected_language_name = st.sidebar.selectbox("🌍 Preferred Language", list(language_map.keys()))
selected_language_code = language_map[selected_language_name]

st.markdown("#### 🗣️ Enter text, record, or upload your voice below")
user_query = ""

audio_bytes = st.audio_recorder("🎤 Record your message (click to start/stop)", format="audio/wav")

uploaded_audio = st.file_uploader("📁 Or upload audio (WAV/MP3/M4A)", type=["wav", "mp3", "m4a"])

if audio_bytes or uploaded_audio:
    if audio_bytes:
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        tmp_file.write(audio_bytes)
        tmp_path = tmp_file.name
    else:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(uploaded_audio.read())
            tmp_path = tmp_file.name

    with st.spinner("🧠 Transcribing with Whisper..."):
        try:
            transcript = openai.Audio.transcribe(
                model="whisper-1",
                file=open(tmp_path, "rb"),
                response_format="json",
                language=selected_language_code
            )
            user_query = transcript["text"]
            st.success(f"📝 Transcribed ({selected_language_name}): {user_query}")
        except Exception as e:
            st.error(f"❌ Whisper error: {e}")

if not user_query:
    user_query = st.text_input("💬 Or type your message:", placeholder="e.g. What's the projected revenue this quarter?")

if user_query:
    st.markdown("---")
    agent_name = "CFO Bot"
    role_prompt = "You are a knowledgeable company CFO. Respond in concise business tone."
    system_prompt = {"role": "system", "content": role_prompt}
    user_input = {"role": "user", "content": user_query}

    with st.spinner("💡 Generating response..."):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[system_prompt, user_input],
                temperature=0.7
            )
            reply = response.choices[0].message["content"].strip()

            if selected_language_code != "en":
                translation = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": f"Translate this to {selected_language_name}:"},
                        {"role": "user", "content": reply}
                    ],
                    temperature=0.5
                )
                reply = translation.choices[0].message["content"].strip()

            st.markdown(f"**{agent_name}**: {reply}")
            chat_log.append({"agent": agent_name, "query": user_query, "response": reply, "time": datetime.now()})
            usage_counter[agent_name] += 1
        except Exception as e:
            st.error(f"❌ Error: {e}")

st.markdown("""
---
Made with ❤️ by Oti Edema • Powered by OpenAI & Streamlit  
GitHub: [OtiEdema/OmniAI-Dashboard](https://github.com/OtiEdema/OmniAI-Dashboard)
""")
