import streamlit as st
import requests
import re
from chatbot.bot import get_rag_chain
import os
os.environ["STREAMLIT_WATCHER_IGNORE_MODULES"] = "torch"

# Initialize RAG chain
qa_chain = get_rag_chain()
API = "http://localhost:8000"

st.set_page_config(page_title="Complaint Chatbot", page_icon="🤖")
st.title("🤖 Complaint Chatbot Assistant")

# Session state for conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Define function to interact with backend
def file_complaint(name, phone, email, details):
    payload = {
        "name": name,
        "phone_number": phone,
        "email": email,
        "complaint_details": details
    }
    try:
        res = requests.post(f"{API}/complaints", json=payload)
        if res.status_code == 200:
            return res.json()
        else:
            return {"error": res.text}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def fetch_complaint(complaint_id):
    try:
        res = requests.get(f"{API}/complaints/{complaint_id}")
        if res.status_code == 200:
            return res.json()
        else:
            return {"error": "Complaint not found."}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# Sidebar for Filing / Fetching Complaint
with st.sidebar:
    st.header("📋 File a Complaint")
    with st.form("file_form"):
        name = st.text_input("Name")
        phone = st.text_input("Phone")
        email = st.text_input("Email")
        details = st.text_area("Complaint Details")
        submitted = st.form_submit_button("Submit Complaint")
        if submitted:
            result = file_complaint(name, phone, email, details)
            if "error" in result:
                st.error(result["error"])
            else:
                st.success(f"Complaint filed! ID: {result['complaint_id']}")

    st.markdown("---")

    st.header("🔍 Fetch Complaint")
    comp_id = st.text_input("Enter Complaint ID")
    if st.button("Fetch"):
        result = fetch_complaint(comp_id.upper())
        if "error" in result:
            st.error(result["error"])
        else:
            st.success("Complaint found:")
            st.json(result)

# Main Chat Interface
st.subheader("💬 Chat with the Assistant")

user_input = st.chat_input("Type your question here...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Process input
    if re.fullmatch(r"[A-Z0-9]{8}", user_input.upper()):
        result = fetch_complaint(user_input.upper())
        response = str(result)
    elif user_input.lower().startswith("fetch"):
        parts = user_input.split(" ")
        if len(parts) >= 2:
            result = fetch_complaint(parts[1].strip().upper())
            response = str(result)
        else:
            response = "Please provide a valid complaint ID. Usage: fetch <complaint_id>"
    else:
        try:
            result = qa_chain.invoke({"query": user_input})
            response = result.get("result", "No response.")
        except Exception as e:
            response = f"Error from RAG assistant: {e}"

    st.session_state.messages.append({"role": "assistant", "content": response})

# Display message history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
