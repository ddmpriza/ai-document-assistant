# AI Document Assistant

A small, extensible backend for uploading PDF documents and asking questions
about their content.

## Current MVP

The first version includes:

- PDF upload through a FastAPI endpoint
- Page-level text extraction with `pypdf`
- Temporary in-memory document storage
- Question endpoint
- Page references in responses
- Provider interface that can later support OpenAI, Hugging Face or another LLM
- A deterministic mock provider, so the full application flow works without an API key

> The current parser supports PDFs that already contain selectable text.
> Scanned documents will require OCR in a later version.

## Project structure

```text
.
├── app/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── providers/
│   │   ├── base.py
│   │   └── mock_provider.py
│   └── services/
│       ├── document_store.py
│       └── pdf_parser.py
├── tests/
│   └── test_health.py
├── requirements.txt
└── README.md
```

## Setup

### 1. Create a virtual environment

Windows:

```bash
py -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the API

```bash
uvicorn app.main:app --reload
```

Open the interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## First test

1. Use `POST /documents` to upload a PDF.
2. Copy the returned `document_id`.
3. Use `POST /ask` with:

```json
{
  "document_id": "paste-the-id-here",
  "question": "What is this document about?"
}
```

The answer currently contains excerpts from the most relevant pages.
This proves that upload, parsing, storage, question handling and page references
work before adding an external LLM.

## Next milestones

1. Add text chunking with metadata.
2. Add embeddings and semantic retrieval.
3. Connect a real LLM provider.
4. Persist documents in a database.
5. Add a small Streamlit interface.
6. Add Docker and deployment configuration.
