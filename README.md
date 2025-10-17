# imperial-court-of-the-port

An agentic AI system to manage port incidents

## Setup

1. Create a virtualenv and install dependencies:

```bash
python -m venv .venv
. .venv/Scripts/activate  # Windows PowerShell: .venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
```

2. Environment variables (create `.env` or export):

```bash
# Required for embeddings
OPENAI_API_KEY=sk-...
# Qdrant Cloud (free tier): create a serverless cluster
QDRANT_URL=https://YOUR-CLUSTER-URL
QDRANT_API_KEY=YOUR_QDRANT_API_KEY  # optional for public endpoints
QDRANT_COLLECTION=imperial_court_kb
# Optional
EMBED_MODEL=text-embedding-3-small
MOCK_MODE=true
```

3. Run the server:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## API

- GET `/health` → `{ "status": "ok" }`
- POST `/incident/run` with body:

```json
{ "incident_type": "network_outage", "severity": "high", "payload": {} }
```

- POST `/rag/ingest` → reads `data/Knowledge Base.docx`, chunks and pushes into Qdrant
- POST `/rag/search` with body:

```json
{ "query": "What is the response to a crane failure?", "top_k": 5 }
```

## RAG Details

- Chunking: tokenizer-aware, ~400 tokens per chunk with ~60-token overlap.
- Vector DB: Qdrant Cloud (free tier). 1536-d vectors (OpenAI embeddings).
- Files:
  - `app/rag_chunking.py` – chunker
  - `app/rag_embeddings.py` – embeddings
  - `app/rag_qdrant.py` – Qdrant wrapper
  - `app/rag_ingest.py` – ingestion from DOCX
  - `app/router_rag.py` – endpoints

Follow `message (1).txt` for imperial naming; RAG serves ministries for contextual grounding.
