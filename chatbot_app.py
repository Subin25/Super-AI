import streamlit as st
from dotenv import load_dotenv
import os
import base64
import requests

load_dotenv()

st.set_page_config(page_title="Trợ lý AI tổng hợp", layout="wide")

# Sidebar
st.sidebar.title("🔧 Tính năng")
menu = st.sidebar.radio("Chọn chức năng", [
    "🧠 Trò chuyện với trợ lý AI",
    "🗂 Tải lên tài liệu",
    "💾 Lưu phiên trò chuyện"
])

# Session state
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

if menu == "🧠 Trò chuyện với trợ lý AI":
    st.title("😄 Trợ lý AI đa mô hình")

    # Chọn AI thứ tự xử lý
    selected_ais = st.multiselect("Chọn AI để xử lý (thứ tự ưu tiên):", ["DeepSeek", "GPT", "Gemini"], default=["DeepSeek", "GPT"])
    user_input = st.text_input("Hỏi gì đó bên dưới để bắt đầu…")

    ai_responses = {}
    error_messages = []
    final_response = ""

    if user_input:
        for ai in selected_ais:
            if ai == "DeepSeek":
                try:
                    deepseek_headers = {
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}"
                    }
                    deepseek_data = {
                        "model": "deepseek-chat",
                        "messages": [{"role": "user", "content": user_input}]
                    }
                    res = requests.post("https://api.deepseek.com/v1/chat/completions", json=deepseek_data, headers=deepseek_headers)
                    res.raise_for_status()
                    answer = res.json()["choices"][0]["message"]["content"]
                    ai_responses["DeepSeek"] = answer
                    final_response += answer + "\n"
                except Exception as e:
                    error_messages.append(f"❌ DeepSeek lỗi: {e}")

            elif ai == "GPT":
                try:
                    openai_headers = {
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
                    }
                    openai_data = {
                        "model": "gpt-3.5-turbo",
                        "messages": [{"role": "user", "content": user_input}]
                    }
                    res = requests.post("https://api.openai.com/v1/chat/completions", json=openai_data, headers=openai_headers)
                    res.raise_for_status()
                    answer = res.json()["choices"][0]["message"]["content"]
                    ai_responses["GPT"] = answer
                    final_response += answer + "\n"
                except Exception as e:
                    error_messages.append(f"❌ GPT lỗi: {e}")

            elif ai == "Gemini":
                try:
                    gemini_data = {
                        "contents": [{"parts": [{"text": user_input}]}]
                    }
                    headers = {
                        "Content-Type": "application/json"
                    }
                    res = requests.post(
                        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={os.getenv('GOOGLE_API_KEY')}",
                        json=gemini_data,
                        headers=headers
                    )
                    res.raise_for_status()
                    answer = res.json()["candidates"][0]["content"]["parts"][0]["text"]
                    ai_responses["Gemini"] = answer
                    final_response += answer + "\n"
                except Exception as e:
                    error_messages.append(f"❌ Gemini lỗi: {e}")

        # Hiển thị lỗi (nếu có)
        for msg in error_messages:
            st.error(msg)

        # Hiển thị phản hồi tổng hợp
        st.markdown("""
        <h4>💡 Phản hồi tổng hợp</h4>
        <div style='background-color: #f9f9f9; padding: 1rem; border-radius: 5px;'>
        <pre style='white-space: pre-wrap;'>
        {}</pre></div>
        """.format(final_response.strip()), unsafe_allow_html=True)

        # Ghi lại vào lịch sử
        st.session_state.chat_log.append(f"🧠 {user_input}\n{final_response.strip()}")

elif menu == "🗂 Tải lên tài liệu":
    st.title("📄 Tải lên tài liệu (PDF, DOCX, TXT)")
    uploaded_files = st.file_uploader("Kéo thả hoặc chọn nhiều tệp", type=["pdf", "docx", "txt"], accept_multiple_files=True)
    if uploaded_files:
        for file in uploaded_files:
            st.success(f"Đã tải lên: {file.name}")
    else:
        st.info("Chưa có tệp nào được tải lên.")

elif menu == "💾 Lưu phiên trò chuyện":
    st.title("💾 Xuất toàn bộ trò chuyện")
    if st.session_state.chat_log:
        chat_text = "\n\n".join(st.session_state.chat_log)
        b64 = base64.b64encode(chat_text.encode()).decode()
        href = f'<a href="data:file/txt;base64,{b64}" download="chat_log.txt">📥 Tải về file chat_log.txt</a>'
        st.markdown(href, unsafe_allow_html=True)
    else:
        st.info("Chưa có nội dung trò chuyện để lưu.")
