import streamlit as st
from serpapi import GoogleSearch
from PyPDF2 import PdfReader
import os
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="Trợ lý AI tổng hợp", layout="wide")

def search_google(query):
    params = {
        "engine": "google",
        "q": query,
        "api_key": os.getenv("SERPAPI_API_KEY")
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    return results.get("organic_results", [])

def handle_file_upload(uploaded_file):
    if uploaded_file.type == "application/pdf":
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    return "Unsupported file type."

with st.sidebar:
    menu = st.radio("📚 Chọn chức năng", ["🌐 Chatbot", "📅 Thư viện", "🛠 Công cụ"], label_visibility="collapsed")

st.title("🧠 Trợ lý AI tổng hợp")

if menu == "🌐 Chatbot":
    st.subheader("💬 Tương tác AI")
    use_web = st.checkbox("🔎 Tìm kiếm web")
    user_input = st.text_input("Nhập câu hỏi hoặc nội dung bạn muốn...", "")
    if st.button("Gửi") and user_input:
        if use_web:
            results = search_google(user_input)
            for result in results[:3]:
                st.write(f"[{result['title']}]({result['link']})")
                st.write(result.get("snippet", ""))
        else:
            st.write("💡 AI đang xử lý câu hỏi...")

elif menu == "📅 Thư viện":
    st.subheader("📄 Phân tích tài liệu")
    uploaded_file = st.file_uploader("Tải lên tài liệu (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])
    if uploaded_file:
        content = handle_file_upload(uploaded_file)
        st.text_area("📖 Nội dung tài liệu", value=content, height=300)

elif menu == "🛠 Công cụ":
    st.subheader("⚙️ Tùy chọn nâng cao")
    st.write("Chức năng sẽ sớm ra mắt.")
