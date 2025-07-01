import streamlit as st
from dotenv import load_dotenv
import os
import requests

load_dotenv()

st.set_page_config(page_title="Trợ lý AI tổng hợp", layout="wide")

# Sidebar
st.sidebar.title("🔧 Tính năng")
menu = st.sidebar.radio("Chọn chức năng", [
    "💬 Trò chuyện với trợ lý AI",
    "🗂 Tải lên tài liệu",
    "💾 Lưu phiên trò chuyện"
])

# Session state
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

if menu == "💬 Trò chuyện với trợ lý AI":
    st.title("🤖 Trợ lý AI đa mô hình")

    ai_options = ["DeepSeek", "GPT", "Gemini"]
    selected_ais = st.multiselect("Chọn AI để xử lý tuần tự (thứ tự quan trọng):", ai_options, default=["DeepSeek", "GPT", "Gemini"])
    user_input = st.text_input("Hỏi gì đó bên dưới để bắt đầu…")

    if user_input:
        response_text = user_input

        for ai in selected_ais:
            if ai == "DeepSeek":
                try:
                    deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
                    res = requests.post(
                        "https://api.deepseek.com/chat/completions",
                        headers={"Authorization": f"Bearer {deepseek_api_key}"},
                        json={
                            "model": "deepseek-chat",
                            "messages": [{"role": "user", "content": response_text}]
                        }
                    )
                    response_text = res.json()["choices"][0]["message"]["content"]
                except Exception as e:
                    st.error(f"❌ DeepSeek lỗi: {e}")

            elif ai == "GPT":
                try:
                    openai_api_key = os.getenv("OPENAI_API_KEY")
                    res = requests.post(
                        "https://api.openai.com/v1/chat/completions",
                        headers={"Authorization": f"Bearer {openai_api_key}"},
                        json={
                            "model": "gpt-3.5-turbo",
                            "messages": [{"role": "user", "content": response_text}]
                        }
                    )
                    response_text = res.json()["choices"][0]["message"]["content"]
                except Exception as e:
                    st.error(f"❌ GPT lỗi: {e}")

            elif ai == "Gemini":
                try:
                    gemini_api_key = os.getenv("GEMINI_API_KEY")
                    res = requests.post(
                        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={gemini_api_key}",
                        json={"contents": [{"parts": [{"text": response_text}]}]}
                    )
                    response_text = res.json()["candidates"][0]["content"]["parts"][0]["text"]
                except Exception as e:
                    st.error(f"❌ Gemini lỗi: {e}")

        st.subheader("💡 Phản hồi tổng hợp")
        st.write(response_text)
        st.session_state.chat_log.append(f"🧑‍💻 {user_input}\n🤖 {response_text}")

elif menu == "🗂 Tải lên tài liệu":
    st.title("📄 Tải lên tài liệu")
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
