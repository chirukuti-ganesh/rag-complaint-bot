# 🤖 RAG Complaint Bot

A **Retrieval-Augmented Generation (RAG)** powered chatbot for **filing** and **retrieving customer complaints** through natural language.

This intelligent assistant integrates:
- 🧠 LangChain for RAG
- 💬 GROQ API for LLM responses
- 📄 HuggingFace + FAISS for document search
- ⚙️ FastAPI backend
- 🌐 Streamlit frontend (form + chat modes)
- 💾 SQLite database for storage

---

## 🚀 Features

- 📝 File new complaints (name, phone, email, description)
- 🔎 Retrieve complaints using complaint ID
- 🤖 RAG-based chatbot with PDF knowledge base
- 🌐 Streamlit UI and 💻 Terminal CLI
- 🗃️ Complaint data stored in SQLite

---

## 📁 Project Structure

```bash
rag-complaint_bot/
├── api/                        # FastAPI backend
│   ├── main.py                 # FastAPI app (API endpoints, DB logic)
│   ├── complaints.db           # SQLite database (should be in .gitignore)
│   └── __pycache__/            # Python cache (should be in .gitignore)
│
├── chatbot/                    # Chatbot logic and knowledge base
│   ├── bot.py                  # RAG pipeline (LangChain, embeddings, etc.)
│   ├── knowledge_base.pdf      # PDF knowledge base
│   └── __pycache__/            # Python cache (should be in .gitignore)
│
├── frontend/                   # Streamlit web frontend
│   └── streamlit_app.py        # Main Streamlit app (file/fetch UI)
│
├── chat_cli.py                 # Terminal-based chatbot CLI
├── streamlit_chatCli.py        # Streamlit-based chatbot CLI
├── requirements.txt            # Python dependencies
├── postman_collection.json     # Postman API test collection (optional)
├── .env                        # Environment variables (should be in .gitignore)
├── .gitignore                  # Git ignore file
└── README.md                   # Project documentation
````

---

## ⚙️ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/chirukuti-ganesh/rag-complaint-bot.git
cd rag-complaint-bot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Environment Variables

Create a `.env` file in the root directory:

```
GROQ_API_KEY=your_groq_api_key
```

---

## 🚦 Running the App

### 🔧 Step 1: Start FastAPI Backend (Required for All Interfaces)

```bash
cd api
uvicorn main:app --reload
```

---

### 💻 Option 1: Terminal Chatbot CLI (Chat + File/Fetch)

Use this for full interaction in the terminal — chat with bot, file new complaints, and retrieve by ID.

```bash
cd ..
python chat_cli.py
```

---

### 🌐 Option 2: Streamlit Complaint UI (File/Fetch Only)

Use this to file or fetch complaints through a simple web form.

```bash
cd frontend
streamlit run streamlit_app.py --server.port 8503
```

Then open: [http://localhost:8503](http://localhost:8503)

---

### 💬 Option 3: Streamlit Chat UI (Chat + File/Fetch)

This interface supports chatting with the RAG assistant, filing complaints, and retrieving complaints by ID — all in one place.

```bash
cd ..
streamlit run streamlit_chatCli.py --server.port 8503
```

Then open: [http://localhost:8503](http://localhost:8503)

> ✅ Ensure the backend is running before using any interface!

---

## 🤖 Main Logic Flow

### `chat_cli.py` (Terminal)

* Accepts commands like:

  * `file`, `register a complaint`: Prompts for user info and files a complaint.
  * `fetch <id>` or 8-character complaint ID: Fetches complaint by ID.
  * Other queries are sent to the RAG chatbot.

### `streamlit_chatCli.py` (Streamlit Chat UI)

* Single text input for:

  * Filing complaints (using keywords like “register complaint”)
  * Fetching by ID
  * Asking questions from the knowledge base

### `streamlit_app.py` (Form UI)

* Form interface for filing complaints and retrieving by ID
* Backend interaction only (no chatbot)

---

## 📄 .gitignore

Recommended entries:

```gitignore
__pycache__/
*.pyc
*.db
*.sqlite
.env
faiss_index/
```

## 👨‍💻 Author

**Chirukuti Ganesh**
🔗 [GitHub](https://github.com/chirukuti-ganesh)
✉️ [chirukuti.ganesh@gmail.com](mailto:chirukuti.ganesh@gmail.com)


