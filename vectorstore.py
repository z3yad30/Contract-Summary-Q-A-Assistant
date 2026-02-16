from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import os

PERSIST_DIR = "./data/chroma_db"

def get_embeddings():
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def get_vectorstore():
    embeddings = get_embeddings()
    if os.path.exists(PERSIST_DIR):
        return Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)
    return Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)