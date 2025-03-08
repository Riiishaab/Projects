# Importing Imp Libraries.
import streamlit as st
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

# CSS Code-This creates a cohesive dark theme with cyberpunk-inspired accents (#00FFAA), improved contrast, and better visual separation between different UI elements.
# CyberPunk UI Style
st.markdown("""
    <style>
    /* Core Cyberpunk Theme */
    .stApp {
        background: radial-gradient(circle at center, #0A0D12 0%, #000000 100%);
        color: #00FFAA !important;
        font-family: 'Courier New', monospace !important;
        background-image: 
            linear-gradient(to bottom, rgba(0, 255, 170, 0.05) 1px, transparent 1px),
            linear-gradient(to right, rgba(0, 255, 170, 0.05) 1px, transparent 1px);
        background-size: 20px 20px;
    }

    /* Animated Elements */
    .cyber-bot {
        position: fixed;
        bottom: 20px;
        right: 30px;
        width: 220px;
        height: 300px;
        z-index: 9999;
        pointer-events: none;
    }

    .bot-with-book {
        animation: cyberFloat 3s ease-in-out infinite;
        background: url('https://i.ibb.co/4d3qWzR/cyberbot-book-sprite.png') 0 0 no-repeat;
        width: 220px;
        height: 300px;
        filter: drop-shadow(0 0 15px #00FFAA) hue-rotate(90deg);
    }

    @keyframes cyberFloat {
        0%, 100% { 
            transform: translateY(0) rotate(-1deg) scaleX(-1);
            background-position: 0 0;
        }
        50% { 
            transform: translateY(-20px) rotate(2deg) scaleX(-1);
            background-position: -440px 0;
        }
    }

    .hologram-glow {
        position: absolute;
        width: 80px;
        height: 100px;
        background: rgba(0, 255, 170, 0.1);
        border-radius: 5px;
        animation: hologramPulse 2s ease-in-out infinite;
        filter: blur(15px);
    }

    @keyframes hologramPulse {
        0%, 100% { opacity: 0.3; transform: scale(0.95); }
        50% { opacity: 0.6; transform: scale(1.05); }
    }

    /* Matrix Rain Overlay */
    .matrix-rain {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        opacity: 0.1;
        z-index: -1;
        background: url('https://i.ibb.co/6BCct0K/matrix-rain.gif');
    }

    /* Chat Interface Enhancements */
    .stChatInput input {
        background: #001212 !important;
        border: 2px solid #00FFAA !important;
        color: #00FFAA !important;
        border-radius: 5px !important;
        font-family: 'Courier New' !important;
    }

    .stChatMessage {
        border-left: 3px solid #00FFAA !important;
        margin: 15px 0 !important;
        padding: 15px !important;
        background: linear-gradient(to right, #001515, #000000) !important;
        box-shadow: 0 0 10px rgba(0, 255, 170, 0.2) !important;
    }

    /* Neon Effects */
    h1, h2, h3 {
        text-shadow: 0 0 10px #00FFAA;
        animation: headerGlow 2s ease-in-out infinite;
    }

    @keyframes headerGlow {
        0%, 100% { text-shadow: 0 0 10px #00FFAA; }
        50% { text-shadow: 0 0 20px #00FFAA, 0 0 30px #00FFAA; }
    }

    /* Terminal Selection Glow */
    .main ::selection {
        background: #00FFAA;
        color: #000000;
    }
    </style>
""", unsafe_allow_html=True)
# You write Prompts here
PROMPT_TEMPLATE = """
[Expert Summarizer]
[Specialization: Technical paper analysis]
[Summarize a document and don't miss important points.Also keep the wording simple and easy to understand.]
[Always give point wise summarization unless asked otherwise.]

Query: {user_query} 
Context: {document_context} 

[Input structure: Query + Context]
Answer:
"""
PDF_STORAGE_PATH = 'document_store/pdfs/'   # Local Storage Isolation
EMBEDDING_MODEL = OllamaEmbeddings(model="llama2:7b")   # 7B Param Technical Encoder
DOCUMENT_VECTOR_DB = InMemoryVectorStore(EMBEDDING_MODEL)  # RAM-based Index
LANGUAGE_MODEL = OllamaLLM(model="llama2:7b")

import os
from pathlib import Path
def save_uploaded_file(uploaded_file):      # Directs files to D:\document_store\pdfs
    # Use absolute path for D: drive storage
    save_dir = r"D:\document_store\pdfs"  # Raw string for Windows
    Path(save_dir).mkdir(parents=True, exist_ok=True)  # Auto-create directories- Auto-directory Creation: Creates nested folders if missing
                                                        # Basic Sanitization:
                                                         # Replaces spaces with underscores
                                                          # Removes parentheses
                                                           # Binary Write: Ensures proper PDF handling
    
    # Sanitize filename (remove spaces/parentheses)
    safe_name = uploaded_file.name.replace(" ", "_").replace("(", "").replace(")", "")
    file_path = os.path.join(save_dir, safe_name)
    
    # Debugging check (remove in production)
    print(f"Target path: {file_path}")  
    
    with open(file_path, "wb") as file:
        file.write(uploaded_file.getbuffer())
    return file_path

def load_pdf_documents(file_path):  #PDFPlumberLoader Characteristics:
                                    #Text extraction with layout preservation, Table data recognition, Page-by-page content parsing
                                  #Metadata retention
    document_loader = PDFPlumberLoader(file_path)
    return document_loader.load()

def chunk_documents(raw_documents):   # Cuts Big Documents into Smaller Pieces.
    text_processor = RecursiveCharacterTextSplitter(
        chunk_size=1000,   # Size of eaach chunk.
        chunk_overlap=200,  # Overlap allowed, to create sence between 2 chunks.
        add_start_index=True  
    )
    return text_processor.split_documents(raw_documents)

def index_documents(document_chunks):  # Takes these small chunks and store them into searchable databases.(Like putting books in shelves)
    DOCUMENT_VECTOR_DB.add_documents(document_chunks)

def find_related_documents(query):  # When you ask questions, it searches database for similar questions.
    return DOCUMENT_VECTOR_DB.similarity_search(query)

def generate_answer(user_query, context_documents):   # Generates ans
    context_text = "\n\n".join([doc.page_content for doc in context_documents])  # Combines found text pieces.
    conversation_prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    response_chain = conversation_prompt | LANGUAGE_MODEL
    return response_chain.invoke({"user_query": user_query, "document_context": context_text})


# UI Configuration


st.title("📘 Summarizer AI")
st.markdown("### Your Intelligent Summarization Assistant")
st.markdown("---")

# File Upload Section
uploaded_pdf = st.file_uploader(
    "Upload Research Document (PDF)",
    type="pdf",
    help="Select a PDF document for analysis",
    accept_multiple_files=False

)

if uploaded_pdf:
    saved_path = save_uploaded_file(uploaded_pdf)
    raw_docs = load_pdf_documents(saved_path)
    processed_chunks = chunk_documents(raw_docs)
    index_documents(processed_chunks)
    
    st.success("✅ Document processed successfully! Summarizing it now...")

    with st.spinner("Summarizing the document..."):
        summary = generate_answer("Summarize this document.", processed_chunks)

    with st.chat_message("assistant", avatar="🤖"):
        st.write("### 📄 Document Summary:")
        st.write(summary)

    user_input = st.chat_input("Ask a question about the document...")
    
    if user_input:
        with st.chat_message("user"):
            st.write(user_input)
        
        with st.spinner("Analyzing document..."):
            relevant_docs = find_related_documents(user_input)
            ai_response = generate_answer(user_input, relevant_docs)
            
        with st.chat_message("assistant", avatar="🤖"):
            st.write(ai_response)
