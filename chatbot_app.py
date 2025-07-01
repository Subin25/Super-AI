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

st.title("🧠 Trợ lý AI tổng hợp")
menu = st.sidebar.radio("Chức năng", [
    "Tải lên tài liệu",
    "Tìm kiếm trên mạng",
    "So sánh hai mô hình AI"
])

if menu == "Tải lên tài liệu":
    st.header("📄 Tải lên tài liệu (PDF, DOCX, TXT)")
    uploaded_file = st.file_uploader("Chọn tệp", type=["pdf", "docx", "txt"])
    if uploaded_file:
        st.success(f"Đã tải lên: {uploaded_file.name}")
    else:
        st.info("Chưa có tệp nào được tải lên.")

elif menu == "Tìm kiếm trên mạng":
    st.header("🔍 Tìm kiếm thông tin qua Google")
    query = st.text_input("Nhập nội dung cần tìm")
    if query:
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
        st.info("(Ví dụ mô phỏng - cần tích hợp API thật)")
        st.subheader("🔷 ChatGPT:")
        st.write("Trả lời từ ChatGPT: ...")
        st.subheader("🟡 Gemini:")
        st.write("Trả lời từ Gemini: ...")
