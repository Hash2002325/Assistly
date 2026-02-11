"""
Embedding manager using Ollama's nomic-embed-text model
"""
from langchain_ollama import OllamaEmbeddings
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

class EmbeddingManager:
    def __init__(self):
        self.embeddings = OllamaEmbeddings(
            model="nomic-embed-text",
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        )
    
    def embed_text(self, text: str) -> List[float]:
        """Convert text to embedding vector"""
        return self.embeddings.embed_query(text)
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Convert multiple texts to embedding vectors"""
        return self.embeddings.embed_documents(texts)