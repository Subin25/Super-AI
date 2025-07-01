import streamlit as st
from dotenv import load_dotenv
import os
import base64
import requests

load_dotenv()

# API Keys
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

st.set_page_config(page_title="Trợ lý AI tổng hợp", layout="wide")

# Sidebar
st.sidebar.title("🔧 Tính năng")
menu = st.sidebar.radio("Chọn chức năng", [
    "🤖 Trò chuyện với trợ lý AI",
    "🗂 Tải lên tài liệu",
    "💾 Lưu phiên trò chuyện"
])

# Session state
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

# === Các hàm gọi API ===
def get_deepseek_response(prompt):
    try:
        headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
        data = {"model": "deepseek-chat", "messages": [{"role": "user", "content": prompt}]}
        response = requests.post("https://api.deepseek.com/v1/chat/completions", headers=headers, json=data)
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[DeepSeek lỗi]: {e}"

def get_gpt_response(prompt):
    try:
        headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
        data = {"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": prompt}]}
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[GPT lỗi]: {e}"

def get_gemini_response(prompt):
    try:
        headers = {"Content-Type": "application/json"}
        data = {"contents": [{"parts": [{"text": prompt}]}]}
        response = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}",
            headers=headers, json=data
        )
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"[Gemini lỗi]: {e}"

# === Giao diện từng tab ===
if menu == "🤖 Trò chuyện với trợ lý AI":
    st.title("😄 Trợ lý AI đa mô hình")
    selected_models = st.multiselect("Chọn AI để xử lý (thứ tự ưu tiên):", ["DeepSeek", "GPT", "Gemini"], default=["DeepSeek", "GPT", "Gemini"])
    prompt = st.text_input("Hỏi gì đó bên dưới để bắt đầu...")

    if prompt and selected_models:
        ai_results = {}
        final_answer = None

        for model in selected_models:
            if model == "DeepSeek":
                result = get_deepseek_response(prompt)
            elif model == "GPT":
                result = get_gpt_response(prompt)
            elif model == "Gemini":
                result = get_gemini_response(prompt)

            ai_results[model] = result

            if not result.startswith("[") and "lỗi" not in result.lower():
                final_answer = result  # Ghi nhận phản hồi thành công cuối cùng

        for model, result in ai_results.items():
            if result.startswith("["):
                st.error(f"❌ {model} lỗi: {result}")
            else:
                st.success(f"✅ {model} phản hồi thành công.")

        st.markdown("### 💡 Phản hồi tổng hợp")
        if final_answer:
            st.write(final_answer)
            st.session_state.chat_log.append(f"Bạn: {prompt}\nAI: {final_answer}")
        else:
            st.warning("Tất cả các AI đều gặp lỗi. Vui lòng kiểm tra API key hoặc thử lại sau.")

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
