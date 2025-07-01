import streamlit as st
import os
from dotenv import load_dotenv
import requests

load_dotenv()
st.set_page_config(page_title="Trợ lý AI Đa mô hình", layout="wide")

# Tạo session state để lưu hội thoại
if "messages" not in st.session_state:
    st.session_state.messages = []

if "ai_chain" not in st.session_state:
    st.session_state.ai_chain = []

# Sidebar - chọn AI theo thứ tự
st.sidebar.title("⚙️ Chọn AI sử dụng")
ai_options = st.sidebar.multiselect(
    "Thứ tự AI bạn muốn dùng:",
    ["DeepSeek", "GPT", "Gemini"],
    default=["DeepSeek", "GPT", "Gemini"]
)

# Hiển thị đoạn chat trước đó
st.title("💬 Trò chuyện với Trợ lý AI")
st.markdown("Hỏi gì đó bên dưới để bắt đầu...")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Nhập prompt
prompt = st.chat_input("Hỏi bất kỳ điều gì")

if prompt and ai_options:
    st.session_state.messages.append({"role": "user", "content": prompt})
    current_input = prompt

    for ai in ai_options:
        try:
            if ai == "DeepSeek":
                res = requests.post(
                    "https://api.deepseek.com/chat",
                    json={"prompt": current_input},
                    headers={"Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}"}
                )
                reply = res.json().get("response", "❌ DeepSeek không phản hồi.")
            elif ai == "GPT":
                res = requests.post(
                    "https://api.openai.com/v1/chat/completions",
                    json={
                        "model": "gpt-3.5-turbo",
                        "messages": [{"role": "user", "content": current_input}]
                    },
                    headers={
                        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
                        "Content-Type": "application/json"
                    }
                )
                reply = res.json()["choices"][0]["message"]["content"]
            elif ai == "Gemini":
                res = requests.post(
                    "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
                    params={"key": os.getenv("GEMINI_API_KEY")},
                    json={"contents": [{"parts": [{"text": current_input}]}]}
                )
                reply = res.json()["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            reply = f"❌ Lỗi khi truy vấn {ai}: {e}"

        # Hiển thị & lưu phản hồi AI
        with st.chat_message("assistant"):
            st.markdown(f"**{ai} trả lời:**\n\n{reply}")
        st.session_state.messages.append({"role": "assistant", "content": f"**{ai}**: {reply}"})
        current_input = reply
