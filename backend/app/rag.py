import re
from sqlalchemy import select
from sqlalchemy.orm import Session
from .models import DocumentChunk, Document
from .text_utils import tokenize, term_counts

def retrieve(db: Session, question: str, limit: int = 5):
    q_tokens = term_counts(question)
    rows = db.execute(select(DocumentChunk, Document).join(Document, Document.id == DocumentChunk.document_id)).all()
    scored = []
    for chunk, doc in rows:
        text_tokens = term_counts(chunk.text)
        overlap = sum(min(q_tokens[t], text_tokens[t]) for t in q_tokens)
        phrase_bonus = 0.0
        normalized_q = " ".join(tokenize(question))
        if normalized_q and normalized_q in chunk.text.lower():
            phrase_bonus = 2.0
        score = overlap + phrase_bonus
        if score > 0:
            scored.append((score, chunk, doc))
    scored.sort(key=lambda x: (-x[0], x[1].id))
    return scored[:limit]

def answer_question(question: str, retrieved):
    if not retrieved:
        return ("I couldn't find a strong match in the indexed documentation. "
                "Try asking about React, Python, FastAPI, MySQL, RAG, embeddings, retrieval, or the CodeRAG architecture.")
    lead = retrieved[0][2].title
    bullets = []
    for _, chunk, _ in retrieved[:3]:
        clean = re.sub(r"\s+", " ", chunk.text).strip()
        bullets.append(clean[:360])
    return f"Based on the indexed documentation, the strongest match is **{lead}**.\n\n" + "\n\n".join(f"• {b}" for b in bullets) + "\n\nThis demo uses MySQL-backed retrieval. A production version can add embeddings and an LLM generation layer after retrieval."
