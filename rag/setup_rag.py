"""
One-time setup script to load knowledge base into vector store
Run this after creating knowledge base documents
"""
from rag.document_loader import DocumentLoader
from rag.vector_store import VectorStore

def setup_rag():
    print("=" * 60)
    print("ASSISTLY RAG SETUP")
    print("=" * 60)
    
    # Load documents
    print("\n📖 Loading documents from knowledge_base/...")
    loader = DocumentLoader()
    documents = loader.load_all_documents()
    
    if not documents:
        print("❌ No documents found! Make sure knowledge_base/ has .txt files")
        return
    
    # Initialize vector store
    print("\n🔧 Initializing vector store...")
    vector_store = VectorStore()
    
    # Clear existing data (optional, comment out if you want to keep old data)
    # vector_store.clear_collection()
    
    # Add documents to vector store
    print("\n💾 Adding documents to vector store...")
    texts = [doc['content'] for doc in documents]
    metadatas = [doc['metadata'] for doc in documents]
    ids = [f"{doc['metadata']['source']}_{doc['metadata']['chunk_id']}" for doc in documents]
    
    vector_store.add_documents(texts, metadatas, ids)
    
    # Verify
    count = vector_store.get_collection_count()
    print(f"\n✅ RAG Setup Complete!")
    print(f"📊 Total documents in vector store: {count}")
    
    # Test search
    print("\n🧪 Testing search...")
    test_query = "What is the refund policy?"
    results = vector_store.search(test_query, n_results=2)
    print(f"\nQuery: '{test_query}'")
    print(f"Found {len(results)} results:")
    for i, result in enumerate(results, 1):
        print(f"\n  Result {i}:")
        print(f"  Source: {result['metadata']['source']}")
        print(f"  Content: {result['content'][:100]}...")

if __name__ == "__main__":
    setup_rag()