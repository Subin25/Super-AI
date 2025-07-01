import streamlit as st
import openai
import google.generativeai as genai
import requests
import json
import os
import datetime
import fitz  # PyMuPDF
import docx  # python-docx
from serpapi import GoogleSearch
from langchain_community.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader
from dotenv import load_dotenv

# === Load environment variables ===
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
serpapi_key = os.getenv("SERPAPI_KEY")

# === DeepSeek Call ===
def deepseek_response(prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {deepseek_api_key}"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "Bạn là trợ lý AI."},
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }
    response = requests.post("https://api.deepseek.com/chat/completions", headers=headers, json=payload)
    result = response.json()
    return result['choices'][0]['message']['content']

# === Gemini Call ===
def gemini_response(prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text

# === GPT Call ===
def gpt_refine(text_from_gemini):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Bạn là trợ lý thông minh, hãy viết lại nội dung sau rõ ràng, hấp dẫn và mạch lạc hơn."},
            {"role": "user", "content": text_from_gemini}
        ]
    )
    return response.choices[0].message["content"]

# === Web Search ===
def web_search(query):
    search = GoogleSearch({"q": query, "api_key": serpapi_key})
    results = search.get_dict()
    output = ""
    for idx, r in enumerate(results.get("organic_results", [])[:5], 1):
        title = r.get("title", "")
        link = r.get("link", "")
        snippet = r.get("snippet", "")
        output += f"{idx}. [{title}]({link})\n{snippet}\n\n"
    return output or "Không tìm thấy kết quả phù hợp."

# === File Reader ===
def extract_text(file):
    if file.name.endswith(".pdf"):
        with fitz.open(stream=file.read(), filetype="pdf") as doc:
            return "\n".join([page.get_text() for page in doc])
    elif file.name.endswith(".docx"):
        document = docx.Document(file)
        return "\n".join([para.text for para in document.paragraphs])
    else:
        return file.read().decode("utf-8")

# === Streamlit App UI ===
st.title("🤖 Trợ lý AI tổng hợp")
user_input = st.chat_input("Nhập câu hỏi hoặc nội dung bạn muốn...")

uploaded_files = st.file_uploader("Tải lên tài liệu (PDF, DOCX, TXT)", accept_multiple_files=True)
doc_text = ""
if uploaded_files:
    for file in uploaded_files:
        doc_text += extract_text(file)

col1, col2 = st.columns(2)
use_web = col1.checkbox("🔎 Tìm kiếm web", value=False)
compare_mode = col2.checkbox("📊 So sánh các AI", value=False)

if user_input:
    final_prompt = doc_text + "\n\n" + user_input
    with st.spinner("Đang xử lý với DeepSeek..."):
        deep_out = deepseek_response(final_prompt)

    with st.spinner("Phân tích với Gemini..."):
        gemini_out = gemini_response(deep_out)

    with st.spinner("Tối ưu với GPT-4o..."):
        gpt_out = gpt_refine(gemini_out)

    if use_web:
        with st.spinner("Tìm kiếm trên Google..."):
            web_result = web_search(user_input)
            st.markdown("### 🌐 Kết quả tìm kiếm từ Google:")
            st.markdown(web_result)

    if compare_mode:
        st.markdown("## 🤖 So sánh kết quả giữa các AI")
        st.chat_message("deepseek").markdown(deep_out)
        st.chat_message("gemini").markdown(gemini_out)
        st.chat_message("gpt").markdown(gpt_out)
    else:
        st.chat_message("assistant").markdown(gpt_out)
