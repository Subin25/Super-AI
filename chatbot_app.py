import streamlit as st
from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()

st.set_page_config(page_title="Trợ lý AI đa mô hình", layout="wide")

# Sidebar menu
st.sidebar.title("⚙️ Tính năng")
menu = st.sidebar.radio("Chọn chức năng", [
    "🤖 Trò chuyện với trợ lý AI",
    "📁 Tải lên tài liệu",
    "💾 Lưu phiên trò chuyện"
])

# Session state
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

if menu == "🤖 Trò chuyện với trợ lý AI":
    st.title("😎 Trợ lý AI đa mô hình")

    # Chọn AI và thứ tự xử lý
    st.subheader("Chọn AI để xử lý (thứ tự ưu tiên):")
    ai_list = st.multiselect(
        "Chọn từ 1 đến 3 AI",
        options=["DeepSeek", "GPT", "Gemini"],
        default=["DeepSeek", "GPT", "Gemini"]
    )

    user_input = st.text_input("Hỏi gì đó bên dưới để bắt đầu...")

    if user_input:
        responses = {}
        final_summary = ""

        for ai in ai_list:
            if ai == "DeepSeek":
                try:
                    headers = {
                        "Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}",
                        "Content-Type": "application/json"
                    }
                    payload = {
                        "model": "deepseek-chat",
                        "messages": [{"role": "user", "content": user_input}]
                    }
                    res = requests.post("https://api.deepseek.com/v1/chat/completions", headers=headers, json=payload)
                    res_json = res.json()
                    answer = res_json["choices"][0]["message"]["content"]
                    responses["DeepSeek"] = answer
                except Exception as e:
                    responses["DeepSeek"] = f"[DeepSeek lỗi]: {e}"

            elif ai == "GPT":
                try:
                    headers = {
                        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
                        "Content-Type": "application/json"
                    }
                    payload = {
                        "model": "gpt-3.5-turbo",
                        "messages": [{"role": "user", "content": user_input}]
                    }
                    res = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
                    res_json = res.json()
                    answer = res_json["choices"][0]["message"]["content"]
                    responses["GPT"] = answer
                except Exception as e:
                    responses["GPT"] = f"[GPT lỗi]: {e}"

            elif ai == "Gemini":
                try:
                    headers = {"Content-Type": "application/json"}
                    payload = {
                        "contents": [{"parts": [{"text": user_input}]}]
                    }
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={os.getenv('GEMINI_API_KEY')}"
                    res = requests.post(url, headers=headers, json=payload)
                    res_json = res.json()
                    answer = res_json["candidates"][0]["content"]["parts"][0]["text"]
                    responses["Gemini"] = answer
                except Exception as e:
                    responses["Gemini"] = f"[Gemini lỗi]: {e}"

        # Hiển thị phản hồi từng AI
        for ai in ai_list:
            with st.expander(f"📦 {ai} phản hồi:"):
                st.write(responses[ai])

        # Tổng hợp phản hồi
        final_summary = "\n\n".join(
            [f"➡️ {ai}: {responses[ai]}" for ai in ai_list if not responses[ai].startswith(f"[{ai} lỗi]")]
        )

        st.markdown("### 💡 Phản hồi tổng hợp")
        if final_summary:
            st.success(final_summary)
            st.session_state.chat_log.append(f"💬 {user_input}\n{final_summary}")
        else:
            st.warning("Tất cả các AI đều gặp lỗi. Vui lòng kiểm tra API key hoặc thử lại sau.")

elif menu == "📁 Tải lên tài liệu":
    st.title("📄 Tải lên tài liệu")
    uploaded_files = st.file_uploader("Kéo thả hoặc chọn tệp", type=["pdf", "docx", "txt"], accept_multiple_files=True)
    if uploaded_files:
        for f in uploaded_files:
            st.success(f"Đã tải lên: {f.name}")
    else:
        st.info("Chưa có tệp nào được tải lên.")

elif menu == "💾 Lưu phiên trò chuyện":
    st.title("💾 Xuất toàn bộ trò chuyện")
    if st.session_state.chat_log:
        chat_text = "\n\n".join(st.session_state.chat_log)
        b64 = base64.b64encode(chat_text.encode()).decode()
        href = f'<a href="data:file/txt;base64,{b64}" download="chat_log.txt">📥 Tải file trò chuyện</a>'
        st.markdown(href, unsafe_allow_html=True)
    else:
        st.info("Không có nội dung nào để lưu.")
