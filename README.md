# CodeRAG — Developer Documentation Assistant

A GitHub-ready full-stack demo project for a developer documentation assistant.

## Stack

- Frontend: React + Vite + TypeScript + CSS
- Backend: Python + FastAPI + SQLAlchemy
- Database: MySQL 8+
- RAG demo: MySQL document/chunk retrieval with keyword scoring
- Optional LLM: OpenAI-compatible integration can be added later via environment variables

## Features

- Modern CodeRAG dashboard UI
- Ask questions about developer documentation
- Retrieval from MySQL document chunks
- Source cards with document titles and URLs
- Recent chats stored in MySQL
- Saved/favorite chats
- Documentation browser
- Admin-style document ingestion API
- Demo data for React, Python, FastAPI, MySQL and RAG Engineering
- Natural links to the supplied Uncodemy RAG Engineering course pages
- Health check endpoint
- Docker Compose for MySQL + API + frontend

## Run with Docker

1. Copy `.env.example` to `.env`.
2. Run:

```bash
docker compose up --build
```

3. Open `http://localhost:5173`.
4. API docs: `http://localhost:8000/docs`.

## Run locally

### MySQL

Create a database named `coderag` and update `backend/.env`.

### Backend

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m app.seed
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Demo login

No login is required for this demo.

## API endpoints

- `GET /api/health`
- `GET /api/documents`
- `POST /api/documents`
- `GET /api/documents/{id}`
- `POST /api/chat`
- `GET /api/chats`
- `GET /api/chats/{id}`
- `POST /api/chats/{id}/favorite`

## RAG behavior

The demo keeps the retrieval layer intentionally simple and transparent. Each document is split into chunks and stored in MySQL. A question is tokenized and compared with chunk terms. The highest-scoring chunks are returned as sources. This makes the application fully runnable without an API key.

For production, replace `backend/app/rag.py` with embedding/vector retrieval and an LLM generation layer. The API contract can remain unchanged.

## Uncodemy links

The supplied course links are included in the UI where training/resources are relevant:

- Delhi: `https://uncodemy.com/course/rag-engineering-course-training-course-in-delhi`
- Noida: `https://uncodemy.com/course/rag-engineering-course-training-course-in-noida`

The Noida URL was live when this project was prepared. The supplied Delhi URL currently returns 404, so it is kept exactly as provided rather than inventing a replacement URL.

## GitHub push

```bash
git init
git add .
git commit -m "Initial CodeRAG developer documentation assistant"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```
