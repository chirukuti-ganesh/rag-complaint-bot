import os
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

# Prevent hot-reload issues with PyTorch in Streamlit
os.environ["STREAMLIT_WATCHER_IGNORE_MODULES"] = "torch"
os.environ["PYTORCH_NO_OP"] = "1"

# Load .env variables
load_dotenv()

# Constants
PDF_PATH = os.path.join(os.path.dirname(__file__), "knowledge_base.pdf")
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
GROQ_MODEL = "llama3-8b-8192"  

def load_vector_store():
    # Load and split the PDF
    if not os.path.exists(PDF_PATH):
        raise FileNotFoundError(f"Knowledge base PDF not found at: {PDF_PATH}")
    
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)

    # Generate embeddings
    embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)
    db = FAISS.from_documents(docs, embeddings)
    return db.as_retriever()

def get_rag_chain():
    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key:
        raise ValueError(" GROQ_API_KEY is not set in your environment variables.")
    
    retriever = load_vector_store()
    llm = ChatGroq(
        model_name=GROQ_MODEL,
        groq_api_key=groq_key
    )

    # Return RAG pipeline
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=False
    )
