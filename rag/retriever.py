"""
RAG Retriever - searches knowledge base and formats context for agents
"""
from rag.vector_store import VectorStore
from typing import List

class RAGRetriever:
    def __init__(self):
        self.vector_store = VectorStore()
    
    def retrieve_context(self, query: str, n_results: int = 3) -> str:
        """
        Retrieve relevant context for a query
        Returns formatted string with sources
        """
        results = self.vector_store.search(query, n_results=n_results)
        
        if not results:
            return "No relevant information found in knowledge base."
        
        # Format context
        context_parts = []
        for i, doc in enumerate(results, 1):
            source = doc['metadata'].get('source', 'unknown')
            content = doc['content']
            context_parts.append(f"[Source {i}: {source}]\n{content}\n")
        
        return "\n".join(context_parts)
    
    def retrieve_for_billing(self, query: str) -> str:
        """Specialized retrieval for billing queries"""
        return self.retrieve_context(query, n_results=3)
    
    def retrieve_for_technical(self, query: str) -> str:
        """Specialized retrieval for technical queries"""
        return self.retrieve_context(query, n_results=3)
    
    def retrieve_for_sales(self, query: str) -> str:
        """Specialized retrieval for sales/product queries"""
        return self.retrieve_context(query, n_results=3)