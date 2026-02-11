"""
Vector store manager using ChromaDB
Stores and retrieves document embeddings
"""
from chromadb import Client
from chromadb.config import Settings
import chromadb
from typing import List, Dict
import os
from dotenv import load_dotenv
from rag.embeddings import EmbeddingManager

load_dotenv()

class VectorStore:
    def __init__(self, collection_name: str = "assistly_knowledge"):
        # Initialize ChromaDB with persistent storage
        persist_dir = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
        
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.embedding_manager = EmbeddingManager()
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "Assistly knowledge base"}
        )
    
    def add_documents(self, texts: List[str], metadatas: List[Dict] = None, ids: List[str] = None):
        """Add documents to vector store"""
        if not ids:
            ids = [f"doc_{i}" for i in range(len(texts))]
        
        if not metadatas:
            metadatas = [{"source": "unknown"} for _ in texts]
        
        # Generate embeddings
        embeddings = self.embedding_manager.embed_documents(texts)
        
        # Add to collection
        self.collection.add(
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
        
        print(f"✅ Added {len(texts)} documents to vector store")
    
    def search(self, query: str, n_results: int = 3) -> List[Dict]:
        """Search for similar documents"""
        query_embedding = self.embedding_manager.embed_text(query)
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        # Format results
        documents = []
        for i in range(len(results['documents'][0])):
            documents.append({
                'content': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i]
            })
        
        return documents
    
    def get_collection_count(self) -> int:
        """Get number of documents in collection"""
        return self.collection.count()
    
    def clear_collection(self):
        """Delete all documents from collection"""
        self.client.delete_collection(self.collection.name)
        print(f"✅ Cleared collection: {self.collection.name}")