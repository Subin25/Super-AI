import streamlit as st
import os
from dotenv import load_dotenv
import requests

load_dotenv()
st.set_page_config(page_title="So sánh AI", layout="wide")

# Khởi tạo session
if "ai_chain" not in st.session_state:
    st.session_state.ai_chain = []
if "result" not in st.session_state:
    st.session_state.result = {}

# Giao diện sidebar
st.sidebar.title("⚙️ Cài đặt")
selected_ais = st.sidebar.multiselect(
    "Chọn AI muốn sử dụng theo thứ tự:",
    ["DeepSeek", "GPT", "Gemini"],
    default=["DeepSeek", "GPT", "Gemini"]
)

# Ô nhập prompt
st.title("🤖 Trợ lý AI đa mô hình")
prompt = st.text_area("✍️ Nhập yêu cầu của bạn:")

if st.button("🚀 Gửi yêu cầu"):
    if not selected_ais or not prompt:
        st.warning("Vui lòng nhập prompt và chọn ít nhất 1 AI.")
    else:
        current_input = prompt
        st.session_state.result = {}

        for ai in selected_ais:
            if ai == "DeepSeek":
                res = requests.post(
                    "https://api.deepseek.com/chat",
                    json={"prompt": current_input},
                    headers={"Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}"}
                )
                reply = res.json().get("response", "❌ Lỗi từ DeepSeek.")
                st.session_state.result["DeepSeek"] = reply
                current_input = reply

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
                st.session_state.result["GPT"] = reply
                current_input = reply

            elif ai == "Gemini":
                res = requests.post(
                    "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
                    params={"key": os.getenv("GEMINI_API_KEY")},
                    json={"contents": [{"parts": [{"text": current_input}]}]}
                )
                reply = res.json()["candidates"][0]["content"]["parts"][0]["text"]
                st.session_state.result["Gemini"] = reply
                current_input = reply

# Hiển thị kết quả
if st.session_state.result:
    st.header("🧾 Kết quả phản hồi")
    for ai in selected_ais:
        if ai in st.session_state.result:
            st.subheader(f"🔹 {ai}")
            st.write(st.session_state.result[ai])
