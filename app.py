import streamlit as st
import os
import time
import subprocess
from backend.rag import retrieve_context
from backend.mistral_model import generate_answer

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Enterprise RAG Assistant",
    page_icon="💼",
    layout="wide"
)

# ---------------- CUSTOM PREMIUM CSS ----------------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
}
.header-title {
    font-size: 36px;
    font-weight: 700;
    background: linear-gradient(90deg, #38bdf8, #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.status-badge {
    background-color: #16a34a;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 14px;
    font-weight: 600;
}
.glass-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    padding: 20px;
    border-radius: 16px;
    margin-bottom: 20px;
}
.chat-user {
    background: linear-gradient(90deg, #2563eb, #3b82f6);
    padding: 12px;
    border-radius: 12px;
    margin-bottom: 10px;
    text-align: right;
}
.chat-bot {
    background: rgba(255, 255, 255, 0.08);
    padding: 12px;
    border-radius: 12px;
    margin-bottom: 20px;
}
.stButton>button {
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    color: white;
    border-radius: 10px;
    height: 45px;
    font-weight: 600;
    border: none;
}
.stButton>button:hover {
    background: linear-gradient(90deg, #4f46e5, #7c3aed);
}
.stTextInput>div>div>input {
    background-color: #1e293b;
    color: white;
    border-radius: 10px;
    border: 1px solid #334155;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
col1, col2 = st.columns([6, 2])

with col1:
    st.markdown('<div class="header-title">Finance & Hospitality RAG Assistant</div>', unsafe_allow_html=True)
    st.caption("Enterprise AI • Local Deployment • CPU Optimized")

with col2:
    st.markdown('<div class="status-badge">🟢 Local Model Running</div>', unsafe_allow_html=True)

st.markdown("---")

# ---------------- SESSION STATE ----------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ---------------- MAIN LAYOUT ----------------
left, right = st.columns([1, 4])

# ---------------- DOCUMENT PANEL ----------------
with left:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Document Management")

    uploaded_files = st.file_uploader(
        "Upload Documents",
        type=["pdf", "docx", "txt", "csv"],
        accept_multiple_files=True
    )

    if uploaded_files:

        # Clear old uploads
        # for old_file in os.listdir(UPLOAD_DIR):
        #     os.remove(os.path.join(UPLOAD_DIR, old_file))

        for file in uploaded_files:
            file_path = os.path.join(UPLOAD_DIR, file.name)
            with open(file_path, "wb") as f:
                f.write(file.getbuffer())

        st.success("Documents uploaded successfully.")

        if st.button("Re-index Documents"):
            with st.spinner("Rebuilding vector index..."):

                if os.path.exists("index.faiss"):
                    os.remove("index.faiss")

                if os.path.exists("docs.pkl"):
                    os.remove("docs.pkl")

                subprocess.run(["python", "backend/ingest.py"])

            st.success("Indexing completed successfully.")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- CHAT PANEL ----------------
with right:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Intelligent Assistant")

    question = st.text_input("Ask your question")

    if st.button("Send"):
        if question.strip() != "":
            start = time.time()

            # 🔍 Step 1 – Retrieval Spinner
            with st.spinner("Retrieving relevant documents..."):
                context, sources = retrieve_context(question)

            # 🤖 Step 2 – Generating Animation
            generate_placeholder = st.empty()

            for i in range(3):
                generate_placeholder.markdown(
                    f" **Generating response{'.' * (i+1)}**"
                )
                time.sleep(0.4)

            if not context.strip():
                answer = "No relevant information found in uploaded documents."
                sources = []
            else:
                try:                #this one to
                    answer = generate_answer(context, question)
                except Exception as e:
                    st.error(f"Run time error: {str(e)}")
                    answer = None       #tto this


            generate_placeholder.empty()

            end = time.time()
            response_time = round(end - start, 2)
        if answer:
            st.session_state.chat_history.append(
                (question, answer, response_time, sources)
            )
        else:
            st.warning("Please try again....")

    # Display Chat History
    for q, a, t, src in reversed(st.session_state.chat_history):
        st.markdown(f'<div class="chat-user"><b>You:</b><br>{q}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="chat-bot"><b>Assistant:</b><br>{a}<br><br>⏱ Response Time: {t}s</div>', unsafe_allow_html=True)

        with st.expander("Source Reference"):
            if src:
                for s in src:
                    st.write(f"{s}")
            else:
                st.write("No source available.")

    if st.button("Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
