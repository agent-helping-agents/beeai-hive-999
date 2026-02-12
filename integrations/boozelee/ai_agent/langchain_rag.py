#!/usr/bin/env python3
"""
LangChain RAG Pipeline
----------------------
Retrieval-Augmented Generation system with FAISS:
  1. Document ingestion and embedding
  2. Vector search with FAISS
  3. Context-aware Q&A with Claude
  4. Persistent index management
"""

import os
import argparse
from pathlib import Path

try:
    from langchain_community.document_loaders import DirectoryLoader, TextLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain_community.embeddings import HuggingFaceEmbeddings
    from langchain_community.vectorstores import FAISS
    from langchain.chains import RetrievalQA
    from anthropic import Anthropic
    DEPS_AVAILABLE = True
except ImportError as e:
    print(f"Missing dependencies: {e}")
    DEPS_AVAILABLE = False


class RAGPipeline:
    """RAG pipeline with FAISS and Claude."""

    def __init__(self, index_path="data/faiss_index"):
        self.index_path = index_path
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.vector_store = None
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def ingest_docs(self, docs_dir="docs", glob_pattern="**/*.md"):
        """Ingest documents and create FAISS index."""
        print(f"\n=== INGESTING DOCUMENTS FROM {docs_dir} ===")

        # Load documents
        loader = DirectoryLoader(
            docs_dir,
            glob=glob_pattern,
            loader_cls=TextLoader,
            show_progress=True,
        )
        documents = loader.load()
        print(f"  Loaded {len(documents)} documents")

        # Split into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )
        chunks = text_splitter.split_documents(documents)
        print(f"  Created {len(chunks)} chunks")

        # Create FAISS index
        self.vector_store = FAISS.from_documents(chunks, self.embeddings)
        print("  ✓ FAISS index created")

        # Save index
        self.save_index()

    def load_index(self):
        """Load existing FAISS index."""
        if not Path(self.index_path).exists():
            print(f"  Index not found at {self.index_path}")
            return False

        self.vector_store = FAISS.load_local(
            self.index_path,
            self.embeddings,
            allow_dangerous_deserialization=True
        )
        print(f"  ✓ Loaded index from {self.index_path}")
        return True

    def save_index(self):
        """Save FAISS index to disk."""
        if not self.vector_store:
            print("  No index to save")
            return

        Path(self.index_path).parent.mkdir(parents=True, exist_ok=True)
        self.vector_store.save_local(self.index_path)
        print(f"  ✓ Saved index to {self.index_path}")

    def query(self, question, k=4):
        """Query the RAG pipeline."""
        if not self.vector_store:
            print("  No index loaded. Run ingest_docs first.")
            return None

        # Retrieve relevant chunks
        docs = self.vector_store.similarity_search(question, k=k)
        print(f"\n=== RETRIEVED {len(docs)} DOCUMENTS ===")

        # Build context
        context = "\n\n".join([doc.page_content for doc in docs])

        # Query Claude with context
        prompt = f"""Based on the following context, answer the question.

Context:
{context}

Question: {question}

Answer:"""

        response = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}]
        )

        answer = response.content[0].text
        print(f"\n=== ANSWER ===\n{answer}\n")

        return answer


def main():
    if not DEPS_AVAILABLE:
        print("Please install dependencies:")
        print("  pip install langchain langchain-community faiss-cpu sentence-transformers anthropic")
        return

    parser = argparse.ArgumentParser(description="LangChain RAG Pipeline")
    parser.add_argument("--mode", choices=["ingest", "query", "update-index"], required=True)
    parser.add_argument("--docs-dir", default="docs", help="Documents directory")
    parser.add_argument("--question", help="Question for query mode")
    parser.add_argument("--index-path", default="data/faiss_index", help="FAISS index path")

    args = parser.parse_args()

    rag = RAGPipeline(index_path=args.index_path)

    if args.mode == "ingest":
        rag.ingest_docs(docs_dir=args.docs_dir)

    elif args.mode == "update-index":
        print("\n=== UPDATING INDEX ===")
        if Path(args.docs_dir).exists():
            rag.ingest_docs(docs_dir=args.docs_dir)
        else:
            print(f"  Docs directory not found: {args.docs_dir}")

    elif args.mode == "query":
        if not args.question:
            print("Error: --question required for query mode")
            return

        if rag.load_index():
            rag.query(args.question)
        else:
            print("  Run ingest mode first to create index")


if __name__ == "__main__":
    main()
