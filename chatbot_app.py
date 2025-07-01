import streamlit as st
from dotenv import load_dotenv
import os
import base64
from PIL import Image
from serpapi import GoogleSearch

load_dotenv()

st.set_page_config(page_title="Trợ lý AI tổng hợp", layout="wide")

# Sidebar
st.sidebar.title("🔧 Tính năng")
menu = st.sidebar.radio("Chọn chức năng", [
    "🗂 Tải lên tài liệu",
    "🔍 Tìm kiếm trên mạng",
    "🤖 So sánh AI",
    "💾 Lưu phiên trò chuyện"
])

# Session state
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

# Tải tài liệu
if menu == "🗂 Tải lên tài liệu":
    st.title("📄 Tải lên tài liệu (PDF, DOCX, TXT, Hình ảnh)")
    uploaded_files = st.file_uploader(
        "📤 Kéo thả hoặc chọn nhiều tệp", 
        type=["pdf", "docx", "txt", "png", "jpg", "jpeg"], 
        accept_multiple_files=True
    )
    if uploaded_files:
        for file in uploaded_files:
            st.success(f"Đã tải lên: {file.name}")
            if file.type.startswith("image/"):
                img = Image.open(file)
                st.image(img, caption=file.name)
    else:
        st.info("Chưa có tệp nào được tải lên.")

# Tìm kiếm SerpAPI
elif menu == "🔍 Tìm kiếm trên mạng":
    st.title("🔍 Tìm kiếm thông tin với SerpAPI")
    query = st.text_input("🔎 Nhập nội dung cần tìm kiếm:")
    if query:
        params = {
            "q": query,
            "api_key": os.getenv("SERPAPI_API_KEY")
        }
        try:
            search = GoogleSearch(params)
            results = search.get_dict()
            if "organic_results" in results:
                for r in results["organic_results"]:
                    st.markdown(f"🔗 [{r['title']}]({r['link']})")
            else:
                st.warning("Không có kết quả.")
        except Exception as e:
            st.error(f"Lỗi khi truy vấn SerpAPI: {e}")

# So sánh AI
elif menu == "🤖 So sánh AI":
    st.title("🤖 So sánh phản hồi giữa ChatGPT và Gemini")
    prompt = st.text_area("💬 Nhập nội dung bạn muốn hỏi cả hai mô hình:")
    if prompt:
        st.session_state.chat_log.append(f"Bạn: {prompt}")
        st.info("(Đây là bản mô phỏng - cần tích hợp API thật)")
        st.subheader("🔷 ChatGPT")
        st.write("Trả lời từ ChatGPT: ...")
        st.subheader("🟡 Gemini")
        st.write("Trả lời từ Gemini: ...")
        st.session_state.chat_log.append("ChatGPT: ...\nGemini: ...")

# Lưu trò chuyện
elif menu == "💾 Lưu phiên trò chuyện":
    st.title("💾 Xuất toàn bộ trò chuyện")
    if st.session_state.chat_log:
        chat_text = "\n\n".join(st.session_state.chat_log)
        b64 =
