import sys
import os
import streamlit as st
import requests

# Ensure chatbot module is found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Ignore torch warning for hot-reloading
os.environ["STREAMLIT_WATCHER_IGNORE_MODULES"] = "torch"

# Import RAG chatbot
from chatbot.bot import get_rag_chain

# Title
st.set_page_config(page_title="RAG Complaint Assistant")
st.title("🧠 RAG Complaint Assistant")
st.caption("File or retrieve complaints using natural language.")

# Constants
API_BASE = "http://localhost:8000"
qa_chain = get_rag_chain()

# Tabs: File & Retrieve
tab1, tab2 = st.tabs(["📩 File Complaint", "🔍 Retrieve Complaint"])

# Store complaint history
if "history" not in st.session_state:
    st.session_state.history = []

# Helper: Ask RAG bot (optional extension)
def ask_bot(user_input):
    return qa_chain.run(user_input)

# Complaint Creation
with tab1:
    st.header("Submit a New Complaint")
    with st.form("complaint_form"):
        name = st.text_input("Your Name", max_chars=50)
        phone = st.text_input("Phone Number", max_chars=15)
        email = st.text_input("Email")
        details = st.text_area("Complaint Details", height=150)

        submit = st.form_submit_button("Submit Complaint")

    if submit:
        if not name or not phone or not email or not details:
            st.warning("🚨 Please fill all fields.")
        else:
            payload = {
                "name": name.strip(),
                "phone_number": phone.strip(),
                "email": email.strip(),
                "complaint_details": details.strip()
            }
            try:
                res = requests.post(f"{API_BASE}/complaints", json=payload)
                data = res.json()
                if 'complaint_id' in data:
                    st.success(f"✅ Complaint Registered! ID: `{data['complaint_id']}`")
                    st.session_state.last_complaint_id = data["complaint_id"]
                else:
                    st.error(f"❌ Missing `complaint_id` in backend response.\n\nResponse: {data}")
            except Exception as e:
                st.error(f"❌ Error submitting complaint: {e}")

# Complaint Retrieval
with tab2:
    st.header("Retrieve Complaint by ID")
    comp_id = st.text_input("Enter Complaint ID", value=st.session_state.get("last_complaint_id", ""))

    if st.button("Fetch Complaint"):
        if not comp_id.strip():
            st.warning("⚠️ Please enter a complaint ID.")
        else:
            try:
                res = requests.get(f"{API_BASE}/complaints/{comp_id.strip()}")
                if res.status_code == 200:
                    st.success("🎉 Complaint found:")
                    st.json(res.json())
                else:
                    st.error(f"❌ Complaint not found.\nStatus code: {res.status_code}\nResponse: {res.text}")
            except Exception as e:
                st.error(f"❌ Error fetching complaint: {e}")
