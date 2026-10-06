from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.orm import Session
from .config import settings
from .database import Base, engine, get_db
from .models import Chat, Document, DocumentChunk
from .rag import answer_question, retrieve
from .schemas import ChatOut, ChatRequest, DocumentCreate, DocumentOut, SourceOut

app = FastAPI(title="CodeRAG API", version="1.0.0", description="Developer Documentation Assistant API")
app.add_middleware(CORSMiddleware, allow_origins=[x.strip() for x in settings.cors_origins.split(",")], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.on_event("startup")
def startup():
    Base.metadata.create_all(engine)

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "coderag-api"}

@app.get("/api/documents", response_model=list[DocumentOut])
def documents(db: Session = Depends(get_db)):
    return db.scalars(select(Document).order_by(Document.created_at.desc())).all()

@app.get("/api/documents/{document_id}", response_model=DocumentOut)
def document(document_id: int, db: Session = Depends(get_db)):
    item = db.get(Document, document_id)
    if not item:
        raise HTTPException(404, "Document not found")
    return item

@app.post("/api/documents", response_model=DocumentOut, status_code=201)
def create_document(payload: DocumentCreate, db: Session = Depends(get_db)):
    doc = Document(**payload.model_dump())
    db.add(doc)
    db.flush()
    words = payload.content.split()
    current, length = [], 0
    for i, word in enumerate(words):
        current.append(word)
        length += len(word) + 1
        if length >= 520 or i == len(words) - 1:
            db.add(DocumentChunk(document_id=doc.id, chunk_index=i, text=" ".join(current)))
            current, length = [], 0
    db.commit()
    db.refresh(doc)
    return doc

@app.post("/api/chat", response_model=ChatOut)
def chat(payload: ChatRequest, db: Session = Depends(get_db)):
    retrieved = retrieve(db, payload.question)
    answer = answer_question(payload.question, retrieved)
    item = Chat(title=payload.question[:70], question=payload.question, answer=answer)
    db.add(item)
    db.commit()
    db.refresh(item)
    sources = [SourceOut(document_id=d.id, title=d.title, category=d.category, source_url=d.source_url, snippet=c.text[:300], score=float(score)) for score, c, d in retrieved]
    return ChatOut(id=item.id, title=item.title, question=item.question, answer=item.answer, favorite=item.favorite, created_at=item.created_at, sources=sources)

@app.get("/api/chats", response_model=list[ChatOut])
def chats(db: Session = Depends(get_db)):
    rows = db.scalars(select(Chat).order_by(Chat.created_at.desc()).limit(30)).all()
    return [ChatOut(id=x.id, title=x.title, question=x.question, answer=x.answer, favorite=x.favorite, created_at=x.created_at, sources=[]) for x in rows]

@app.get("/api/chats/{chat_id}", response_model=ChatOut)
def get_chat(chat_id: int, db: Session = Depends(get_db)):
    item = db.get(Chat, chat_id)
    if not item:
        raise HTTPException(404, "Chat not found")
    retrieved = retrieve(db, item.question)
    sources = [SourceOut(document_id=d.id, title=d.title, category=d.category, source_url=d.source_url, snippet=c.text[:300], score=float(score)) for score, c, d in retrieved]
    return ChatOut(id=item.id, title=item.title, question=item.question, answer=item.answer, favorite=item.favorite, created_at=item.created_at, sources=sources)

@app.post("/api/chats/{chat_id}/favorite", response_model=ChatOut)
def favorite_chat(chat_id: int, db: Session = Depends(get_db)):
    item = db.get(Chat, chat_id)
    if not item:
        raise HTTPException(404, "Chat not found")
    item.favorite = not item.favorite
    db.commit()
    db.refresh(item)
    return ChatOut(id=item.id, title=item.title, question=item.question, answer=item.answer, favorite=item.favorite, created_at=item.created_at, sources=[])
