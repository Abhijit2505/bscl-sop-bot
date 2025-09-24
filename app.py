# smart_city_sop_bot.py
import streamlit as st
import requests

# Config
BASE_URL = "https://hghyoy4izpvczlipi7u5el2z.agents.do-ai.run"
API_KEY = "_0KdZR7Da0ucvgNG267gWbp-O5o5vMqZ"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def chat_completion(messages):
    """Send the entire conversation history for context"""
    url = f"{BASE_URL}/api/v1/chat/completions"
    payload = {
        "messages": messages,
        "temperature": 0.4,
        "max_tokens": 3000,   # 🔥 increased max tokens
        "stream": False,
        "retrieval_method": "rewrite",
        "provide_citations": False
    }
    resp = requests.post(url, headers=headers, json=payload)
    if resp.status_code == 200:
        return resp.json()["choices"][0]["message"]["content"]
    else:
        return f"Error {resp.status_code}: {resp.text}"

# Streamlit UI
st.set_page_config(page_title="Smart City SOP AI Bot", page_icon="🏙️", layout="centered")

st.markdown("<h2 style='text-align:center; color:#2c3e50;'>🏙️ Smart City SOP AI Bot</h2>", unsafe_allow_html=True)
st.write("Your AI-powered assistant for **Smart City Standard Operating Procedures**. Ask me anything!")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are the Smart City SOP AI Bot. Provide detailed, complete answers."}]

# Input
user_input = st.chat_input("Type your question here...")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Get bot response
    response = chat_completion(st.session_state.messages)
    
    # Add assistant message
    st.session_state.messages.append({"role": "assistant", "content": response})

# Display chat history in WhatsApp style
for i, msg in enumerate(st.session_state.messages):
    if msg["role"] == "user":
        st.markdown(
            f"<div style='text-align:right; background-color:#dcf8c6; display:inline-block; padding:10px; border-radius:12px; margin:5px 0; max-width:70%; float:right; clear:both;'>"
            f"<b>You:</b><br>{msg['content']}</div><div style='clear:both;'></div>",
            unsafe_allow_html=True
        )
    elif msg["role"] == "assistant":
        st.markdown(
            f"<div style='text-align:left; background-color:#f1f0f0; display:inline-block; padding:10px; border-radius:12px; margin:5px 0; max-width:70%; float:left; clear:both;'>"
            f"<b>SOP AI Bot:</b><br>{msg['content']}</div><div style='clear:both;'></div>",
            unsafe_allow_html=True
        )
