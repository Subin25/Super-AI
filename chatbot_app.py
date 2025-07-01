import streamlit as st
from dotenv import load_dotenv
import os
import base64
import requests
from PIL import Image

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

# 🗂 Tải lên tài liệu
if menu == "🗂 Tải lên tài liệu":
    st.title("📄 Tải lên tài liệu (PDF, DOCX, TXT, PNG, JPG)")
    uploaded_files = st.file_uploader("Kéo thả hoặc chọn nhiều tệp", 
                                      type=["pdf", "docx", "txt", "png", "jpg", "jpeg"], 
                                      accept_multiple_files=True)
    if uploaded_files:
        for file in uploaded_files:
            st.success(f"Đã tải lên: {file.name}")
            # Hiển thị ảnh nếu là hình ảnh
            if file.type.startswith("image/"):
                img = Image.open(file)
                st.image(img, caption=file.name)
    else:
        st.info("Chưa có tệp nào được tải lên.")

# 🔍 Tìm kiếm trên mạng
elif menu == "🔍 Tìm kiếm trên mạng":
    st.title("🔍 Tìm kiếm thông tin với SerpAPI")
    query = st.text_input("Nhập nội dung cần tìm kiếm:")
    if query:
        params = {
            "q": query,
            "api_key": os.getenv("SERPAPI_API_KEY"),
            "engine": "google"
        }
        try:
            response = requests.get("https://serpapi.com/search", params=params)
            results = response.json()
            if "organic_results" in results:
                for r in results["organic_results"]:
                    st.markdown(f"[{r.get('title', 'Không có tiêu đề')}]({r.get('link', '#')})")
            else:
