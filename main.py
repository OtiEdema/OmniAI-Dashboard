import streamlit as st
import time
from datetime import datetime
from collections import defaultdict
import os
import random
import pandas as pd
import tempfile
from io import BytesIO
import base64
import soundfile as sf
from openai import OpenAI

# Initialise OpenAI client
client = OpenAI()

# App Configuration
st.set_page_config(page_title="OmniAI Dashboard", layout="wide")

# Apply Dark Theme CSS
st.markdown("""
    <style>
        body {
            background-color: #0e1117;
            color: #d1d5db;
        }
        .reportview-container .main .block-container{
            padding-top: 2rem;
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
        .stTextInput>div>input {
            background-color: #1c1f26;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 OmniAI: The Autonomous Company Dashboard")

# Role colours
def get_role_colors():
    return {
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

role_colors = get_role_colors()

# Expanded Agents and Departments
agents = {
    "CEO": "You are the CEO of the company. Respond with strategic insights.",
    "CTO": "You are the CTO. Answer with technical clarity.",
    "CFO": "You are the CFO. Give financial advice in professional tone.",
    "CMO": "You are the CMO. Think like a marketer.",
    "COO": "You are the COO. Streamline operational efficiency.",
    "Legal Advisor": "You are the legal advisor. Respond with legal clarity.",
    "Public Relations Officer": "You are the Publicity head. Respond diplomatically.",
    "DevOps": "You are the DevOps engineer. Explain systems and pipelines.",
    "Product Manager": "You are a product manager. Clarify scope and vision.",
    "Sales Director": "You are the Sales Director. Respond to client and market queries.",
    "QA Engineer": "You are the QA Engineer. Highlight testing methodologies.",
    "HR Manager": "You are the HR Manager. Be human-centred and policy-driven.",
    "Customer Support Agent": "You are a helpful and kind support agent."
}

# Sidebar - Language and Agent
language_map = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Chinese": "zh",
    "Arabic": "ar"
}

st.sidebar.header("🧠 Select an AI Agent")
agent_name = st.sidebar.selectbox("Agent", list(agents.keys()))
selected_language_name = st.sidebar.selectbox("🌍 Preferred Language", list(language_map.keys()))
selected_language_code = language_map[selected_language_name]

# Tabs
tab1, tab2 = st.tabs(["💬 Chat", "📊 Status"])
chat_log = []
usage_counter = defaultdict(int)

# Chat Tab
with tab1:
    st.markdown("#### 🗣️ Enter text or upload your voice below")

    user_query = ""
    uploaded_audio = st.file_uploader("📁 Upload audio (WAV/MP3/M4A)", type=["wav", "mp3", "m4a"])

    if uploaded_audio:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(uploaded_audio.read())
            tmp_path = tmp_file.name

        with st.spinner("🧠 Transcribing with Whisper..."):
            try:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=open(tmp_path, "rb"),
                    response_format="json",
                    language=selected_language_code
                )
                user_query = transcript.text
                st.success(f"📝 Transcribed ({selected_language_name}): {user_query}")
            except Exception as e:
                st.error(f"❌ Whisper error: {e}")

    if not user_query:
        user_query = st.text_input("💬 Or type your message:", placeholder="e.g. What’s our deployment success rate?")

    if user_query:
        st.markdown("---")
        system_prompt = {"role": "system", "content": agents[agent_name]}
        user_input = {"role": "user", "content": user_query}

        with st.spinner("💡 Generating response..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[system_prompt, user_input],
                    temperature=0.7
                )
                reply = response.choices[0].message.content.strip()

                # Translate back if needed
                if selected_language_code != "en":
                    translation = client.chat.completions.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": f"Translate this to {selected_language_name}:"},
                            {"role": "user", "content": reply}
                        ],
                        temperature=0.5
                    )
                    reply = translation.choices[0].message.content.strip()

                st.markdown(f"**{agent_name}**: {reply}")
                chat_log.append({"agent": agent_name, "query": user_query, "response": reply, "time": datetime.now()})
                usage_counter[agent_name] += 1

            except Exception as e:
                st.error(f"❌ Error: {e}")

# Status Page
with tab2:
    st.subheader("📊 Live Agent Usage")
    if usage_counter:
        df = pd.DataFrame(list(usage_counter.items()), columns=["Agent", "Usage Count"])
        st.bar_chart(df.set_index("Agent"))
    else:
        st.info("No agent usage yet.")

    st.subheader("📜 Chat Log")
    if chat_log:
        for item in reversed(chat_log[-5:]):
            st.markdown(f"- 🕒 {item['time'].strftime('%H:%M:%S')} | **{item['agent']}** → {item['query']}")
            st.markdown(f"  ↪️ _{item['response']}_")
    else:
        st.info("No conversations logged yet.")

# Footer
st.markdown("""
---
Made with ❤️ by Oti Edema • Powered by OpenAI & Streamlit  
GitHub: [OtiEdema/OmniAI-Dashboard](https://github.com/OtiEdema/OmniAI-Dashboard)
""")
