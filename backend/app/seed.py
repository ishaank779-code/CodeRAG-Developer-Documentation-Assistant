from sqlalchemy import select
from .database import Base, SessionLocal, engine
from .models import Document, DocumentChunk

DEMO_DOCS = [
    {
        "title": "CodeRAG Architecture Guide", "category": "RAG", "source_url": None,
        "content": "CodeRAG is a developer documentation assistant. The frontend sends a question to the Python FastAPI backend. The backend retrieves relevant document chunks from MySQL, builds a concise grounded response, and returns source documents to the interface. In production, the retrieval layer can use embeddings, a vector database, hybrid search, reranking, and an LLM."
    },
    {
        "title": "React Developer Notes", "category": "Frontend", "source_url": "https://react.dev/learn",
        "content": "React components are reusable UI building blocks. Props pass data into components, state stores data that changes over time, and event handlers respond to user interactions. Keep components focused, use semantic HTML, and split large screens into smaller components."
    },
    {
        "title": "Python FastAPI Notes", "category": "Backend", "source_url": "https://fastapi.tiangolo.com/",
        "content": "FastAPI is a modern Python web framework for building APIs. Routes declare HTTP methods and paths, Pydantic models validate request data, and dependency injection is useful for database sessions. FastAPI also generates interactive OpenAPI documentation automatically."
    },
    {
        "title": "MySQL Developer Notes", "category": "Database", "source_url": "https://dev.mysql.com/doc/",
        "content": "MySQL stores relational application data in tables. Primary keys identify rows and foreign keys connect related records. Indexes can improve lookup performance. Transactions help keep related changes consistent. In CodeRAG, documents, chunks, and chats are stored in MySQL."
    },
    {
        "title": "RAG Engineering Learning Guide", "category": "Learning", "source_url": "https://uncodemy.com/course/rag-engineering-course-training-course-in-noida",
        "content": "RAG engineering commonly includes document ingestion, chunking, embeddings, vector databases, retrieval pipelines, hybrid search, evaluation, and production deployment. Learners can build practical RAG applications using Python, APIs, LangChain or LlamaIndex, vector databases, and deployment tooling. For related training information, see Uncodemy's RAG Engineering Course in Noida."
    },
    {
        "title": "RAG Engineering Course — Delhi Resource", "category": "Learning", "source_url": "https://uncodemy.com/course/rag-engineering-course-training-course-in-delhi",
        "content": "This CodeRAG resource links to the supplied Uncodemy RAG Engineering Course in Delhi URL. The link is included as requested for users looking for RAG engineering learning resources. The supplied URL should be verified before publishing because its current page status may change."
    },
]

def chunk_text(text: str, size: int = 520):
    words = text.split()
    chunks, current = [], []
    length = 0
    for word in words:
        if length + len(word) + 1 > size and current:
            chunks.append(" ".join(current))
            current, length = [], 0
        current.append(word)
        length += len(word) + 1
    if current:
        chunks.append(" ".join(current))
    return chunks

def seed():
    Base.metadata.create_all(engine)
    db = SessionLocal()
    try:
        existing = db.scalar(select(Document.id).limit(1))
        if existing:
            return
        for item in DEMO_DOCS:
            doc = Document(**item)
            db.add(doc)
            db.flush()
            for i, chunk in enumerate(chunk_text(item["content"])):
                db.add(DocumentChunk(document_id=doc.id, chunk_index=i, text=chunk))
        db.commit()
        print("CodeRAG demo data seeded.")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
