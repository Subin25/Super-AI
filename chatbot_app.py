import streamlit as st
from dotenv import load_dotenv
import os

# Xử lý lỗi khi không có serpapi
try:
    from serpapi import GoogleSearch
except ImportError:
    GoogleSearch = None

load_dotenv()

st.set_page_config(page_title="Trợ lý AI tổng hợp", layout="wide")

# Khởi tạo bộ nhớ lưu chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("🧠 Trợ lý AI tổng hợp")
menu = st.sidebar.radio("Chức năng", [
    "Tải lên tài liệu",
    "Tải ảnh từ máy",
    "Tìm kiếm trên mạng",
    "So sánh hai mô hình AI",
    "Xem lịch sử trò chuyện"
])

if menu == "Tải lên tài liệu":
    st.header("📄 Tải lên tài liệu (PDF, DOCX, TXT)")
    uploaded_files = st.file_uploader("Chọn tệp", type=["pdf", "docx", "txt"], accept_multiple_files=True)
    if uploaded_files:
        for file in uploaded_files:
            st.success(f"Đã tải lên: {file.name}")
    else:
        st.info("Chưa có tệp nào được tải lên.")

elif menu == "Tải ảnh từ máy":
    st.header("🖼️ Tải ảnh từ thiết bị (PNG, JPG)")
    image_files = st.file_uploader("Chọn ảnh", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    if image_files:
        for img in image_files:
            st.image(img, caption=img.name, use_column_width=True)
    else:
        st.info("Chưa có ảnh nào được tải lên.")

elif menu == "Tìm kiếm trên mạng":
    st.header("🔍 Tìm kiếm thông tin qua Google")
    query = st.text_input("Nhập nội dung cần tìm")
    if query:
        st.session_state.chat_history.append(("🔍 Tìm kiếm", query))
        if GoogleSearch:
            params = {
                "q": query,
                "api_key": os.getenv("SERPAPI_API_KEY")
            }
            search = GoogleSearch(params)
            results = search.get_dict()
            if "organic_results" in results:
                for r in results["organic_results"]:
                    st.markdown(f"[{r['title']}]({r['link']})")
            else:
                st.warning("Không có kết quả.")
        else:
            st.error("Chưa cài đặt thư viện serpapi.")

elif menu == "So sánh hai mô hình AI":
    st.header("🤖 So sánh mô hình ChatGPT và Gemini")
    prompt = st.text_area("Nhập nội dung cần hỏi:")
    if prompt:
        st.session_state.chat_history.append(("⚖️ So sánh AI", prompt))
        st.info("(Ví dụ mô phỏng - cần tích hợp API thật)")
        st.subheader("🔷 ChatGPT:")
        st.write("Trả lời từ ChatGPT: ...")
        st.subheader("🟡 Gemini:")
        st.write("Trả lời từ Gemini: ...")

elif menu == "Xem lịch sử trò chuyện":
    st.header("🕒 Lịch sử trò chuyện")
    if st.session_state.chat_history:
        for i, (func, content) in enumerate(st.session_state.chat_history[::-1], 1):
            st.markdown(f"**{i}. {func}:** {content}")
    else:
        st.info("Chưa có lịch sử trò chuyện nào.")
