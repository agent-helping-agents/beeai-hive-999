# Knowledge Base

Add markdown documents here to build your RAG knowledge base.

## Structure

```
docs/
├── README.md (this file)
├── langchain_guide.md
├── api_reference.md
└── troubleshooting.md
```

## Usage

After adding documents, update the FAISS index:

```bash
./scripts/update_rag.sh
```

Then query your knowledge base:

```bash
python langchain_rag.py --mode query --question "Your question here"
```
