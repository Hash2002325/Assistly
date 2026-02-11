"""
Document loader for knowledge base files
Loads and chunks documents from knowledge_base/ folder
"""
import os
from typing import List, Dict
from langchain_text_splitters import RecursiveCharacterTextSplitter

class DocumentLoader:
    def __init__(self, knowledge_base_path: str = "knowledge_base"):
        self.knowledge_base_path = knowledge_base_path
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,  # Characters per chunk
            chunk_overlap=50,  # Overlap between chunks
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    def load_text_file(self, filepath: str) -> str:
        """Load a single text file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    
    def load_all_documents(self) -> List[Dict]:
        """Load all .txt files from knowledge_base folder"""
        documents = []
        
        if not os.path.exists(self.knowledge_base_path):
            print(f"❌ Knowledge base folder not found: {self.knowledge_base_path}")
            return documents
        
        for filename in os.listdir(self.knowledge_base_path):
            if filename.endswith('.txt'):
                filepath = os.path.join(self.knowledge_base_path, filename)
                content = self.load_text_file(filepath)
                
                # Split into chunks
                chunks = self.text_splitter.split_text(content)
                
                # Add each chunk with metadata
                for i, chunk in enumerate(chunks):
                    documents.append({
                        'content': chunk,
                        'metadata': {
                            'source': filename,
                            'chunk_id': i
                        }
                    })
                
                print(f"✅ Loaded {filename}: {len(chunks)} chunks")
        
        print(f"\n📚 Total documents loaded: {len(documents)}")
        return documents