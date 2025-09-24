# smart_city_sop_bot.py
import streamlit as st
import requests
import time

# Config
BASE_URL = "https://hghyoy4izpvczlipi7u5el2z.agents.do-ai.run"
API_KEY = "_0KdZR7Da0ucvgNG267gWbp-O5o5vMqZ"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def chat_completion(messages):
    """Send conversation history and return bot reply"""
    url = f"{BASE_URL}/api/v1/chat/completions"
    payload = {
        "messages": messages,
        "temperature": 0.4,
        "max_tokens": 3000,
        "stream": False,
        "retrieval_method": "rewrite",
        "provide_citations": False
    }
    resp = requests.post(url, headers=headers, json=payload)
    if resp.status_code == 200:
        return resp.json()["choices"][0]["message"]["content"]
    else:
        return f"Error {resp.status_code}: {resp.text}"

# Page setup
st.set_page_config(page_title="Smart City SOP AI Bot", page_icon="🏙️", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    body { background-color: #f5f5f5; }
    .chat-container { max-width: 800px; margin: auto; }
    .user-bubble {
        background-color: #dcf8c6; padding: 10px 15px; border-radius: 15px;
        margin: 8px 0; max-width: 70%; float: right; clear: both;
        font-family: Arial, sans-serif; font-size: 15px;
    }
    .bot-bubble {
        background-color: #ffffff; padding: 10px 15px; border-radius: 15px;
        margin: 8px 0; max-width: 70%; float: left; clear: both;
        font-family: Arial, sans-serif; font-size: 15px; border: 1px solid #ddd;
    }
    .typing { font-style: italic; color: #555; margin: 5px 0; float: left; clear: both; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align:center; color:#2c3e50;'>🏙️ Smart City SOP AI Bot</h2>", unsafe_allow_html=True)

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are the Smart City SOP AI Bot. Provide detailed, complete answers."}
    ]

# Input box at bottom
user_input = st.chat_input("Type your question...")

if user_input:
    # Add user message immediately
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Show messages so far (user text visible instantly)
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"<div class='user-bubble'><b>You:</b><br>{msg['content']}</div>", unsafe_allow_html=True)
        elif msg["role"] == "assistant":
            st.markdown(f"<div class='bot-bubble'><b>SOP AI Bot:</b><br>{msg['content']}</div>", unsafe_allow_html=True)

    # Typing indicator
    typing_placeholder = st.empty()
    typing_placeholder.markdown("<div class='typing'>🤖 SOP AI Bot is typing...</div>", unsafe_allow_html=True)

    # Get bot response
    response = chat_completion(st.session_state.messages)

    # Replace typing with actual reply (simulated streaming)
    bot_reply = ""
    reply_placeholder = st.empty()
    for ch in response:
        bot_reply += ch
        reply_placeholder.markdown(
            f"<div class='bot-bubble'><b>SOP AI Bot:</b><br>{bot_reply}</div>",
            unsafe_allow_html=True
        )
        time.sleep(0.01)

    typing_placeholder.empty()
    st.session_state.messages.append({"role": "assistant", "content": response})

# If no new input, just render history
else:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"<div class='user-bubble'><b>You:</b><br>{msg['content']}</div>", unsafe_allow_html=True)
        elif msg["role"] == "assistant":
            st.markdown(f"<div class='bot-bubble'><b>SOP AI Bot:</b><br>{msg['content']}</div>", unsafe_allow_html=True)
