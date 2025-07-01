import streamlit as st
from dotenv import load_dotenv
import os
import base64
from serpapi import GoogleSearch
from PIL import Image

load_dotenv()

st.set_page_config(page_title="Trợ lý AI tổng hợp", layout="wide")

# Sidebar chức năng
st.sidebar.title("🔧 Tính năng")
menu = st.sidebar.radio("Chọn chức năng", [
    "🗂 Tải lên tài liệu",
    "🖼 Ảnh từ clipboard",
    "🔍 Tìm kiếm trên mạng",
    "🤖 So sánh AI",
    "💾 Lưu phiên trò chuyện"
])

# Khởi tạo session lưu chat
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

# 🗂 Tải nhiều tài liệu
if menu == "🗂 Tải lên tài liệu":
    st.title("📄 Tải lên tài liệu (PDF, DOCX, TXT)")
    uploaded_files = st.file_uploader("Kéo thả hoặc chọn nhiều tệp", type=["pdf", "docx", "txt"], accept_multiple_files=True)
    if uploaded_files:
        for file in uploaded_files:
            st.success(f"✅ Đã tải lên: {file.name}")
    else:
        st.info("📂 Chưa có tệp nào được tải lên.")

# 🖼 Tải ảnh từ clipboard
elif menu == "🖼 Ảnh từ clipboard":
    st.title("🖼 Tải ảnh từ clipboard hoặc kéo thả")
    image = st.file_uploader("Dán hoặc chọn ảnh", type=["png", "jpg", "jpeg"])
    if image:
        st.image(Image.open(image), caption="Ảnh đã tải", use_column_width=True)
    else:
        st.info("📷 Chưa có ảnh nào được tải lên.")

# 🔍 Tìm kiếm qua SerpAPI
elif menu == "🔍 Tìm kiếm trên mạng":
    st.title("🔍 Tìm kiếm thông tin với SerpAPI")
    query = st.text_input("🔎 Nhập nội dung cần tìm:")
    if query:
        params = {
            "q": query,
            "api_key": os.getenv("SERPAPI_API_KEY"),
            "engine": "google"
        }
        try:
            search = GoogleSearch(params)
            results = search.get_dict()
            if "organic_results" in results:
                for r in results["organic_results"]:
                    title = r.get("title", "No title")
                    link = r.get("link", "#")
                    st.markdown(f"- [{title}]({link})")
            else:
                st.warning("❗ Không có kết quả phù hợp.")
        except Exception as e:
            st.error(f"⚠️ Lỗi khi truy vấn SerpAPI: {e}")

# 🤖 So sánh AI
elif menu == "🤖 So sánh AI":
    st.title("🤖 So sánh phản hồi giữa ChatGPT và Gemini")
    prompt = st.text_area("💬 Nhập nội dung muốn hỏi cả hai mô hình:")
    if prompt:
        st.session_state.chat_log.append(f"Bạn: {prompt}")
        st.info("(Mô phỏng - cần tích hợp API thật)")

        st.subheader("🔷 ChatGPT")
        gpt_reply = "Trả lời từ ChatGPT: [Chưa tích hợp API]"
        st.write(gpt_reply)
        st.session_state.chat_log.append(gpt_reply)

        st.subheader("🟡 Gemini")
        gemini_reply = "Trả lời từ Gemini: [Chưa tích hợp API]"
        st.write(gemini_reply)
        st.session_state.chat_log.append(gemini_reply)

# 💾 Lưu phiên chat
elif menu == "💾 Lưu phiên trò chuyện":
    st.title("💾 Lưu lại nội dung chat")
    if st.session_state.chat_log:
        chat_text = "\n\n".join(st.session_state.chat_log)
        b64 = base64.b64encode(chat_text.encode()).decode()
        href = f'<a href="data:file/txt;base64,{b64}" download="chat_log.txt">📥 Tải về lịch sử trò chuyện</a>'
        st.markdown(href, unsafe_allow_html=True)
    else:
        st.info("💬 Chưa có nội dung trò chuyện để lưu.")
