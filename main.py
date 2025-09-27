from fastapi import FastAPI, Depends, status, Response, File, UploadFile
import schemas
import json
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import google.generativeai as genai
import os


genai.configure(api_key="Your API key")


app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/ingest-chat-json")
async def ingest_chat_json(file: UploadFile = File(...), db: Session = Depends(get_db)):
    raw = await file.read()
    data = json.loads(raw)

    new_chat = models.Chat(title=data.get("title", "Untitled"))
    db.add(new_chat)
    db.flush()  # so we can use new_chat.id before commit

    for msg in data["messages"]:
        db.add(
            models.ChatMessage(
                chat_id=new_chat.id, role=msg["role"], content=msg["content"]
            )
        )

    db.commit()
    db.refresh(new_chat)
    return {"chat_id": new_chat.id, "title": new_chat.title}


@app.get("/chats/{chat_id}")
def get_chat(chat_id: int, db: Session = Depends(get_db)):
    chat = db.query(models.Chat).filter(models.Chat.id == chat_id).first()
    return {
        "title": chat.title,
        "messages": [{"role": m.role, "content": m.content} for m in chat.messages],
    }


def get_chat_context(chat_id: int, db: Session) -> str:
    chat = db.query(models.Chat).filter(models.Chat.id == chat_id).first()
    messages = (
        db.query(models.ChatMessage)
        .filter_by(chat_id=chat_id)
        .order_by(models.ChatMessage.id)
        .all()
    )

    # Combine all messages into one string for the prompt
    context = f"Title: {chat.title}\n\n"
    for msg in messages:
        context += f"{msg.role.upper()}: {msg.content}\n\n"
    return context


def ask_gemini(chat_id: int, question: str, db):
    context = get_chat_context(chat_id, db)  # pull the stored conversation
    prompt = f"Here is the stored conversation:\n{context}\n\nNow answer this question: {question}"
    model = genai.GenerativeModel("models/gemini-1.5-pro")
    resp = model.generate_content(prompt)
    return resp.text


@app.get("/ask-gemini/{chat_id}")
def ask_gemini_endpoint(chat_id: int, question: str, db: Session = Depends(get_db)):
    answer = ask_gemini(chat_id, question, db)
    # store Gemini's answer as part of the chat
    db.add(models.ChatMessage(chat_id=chat_id, role="gemini", content=answer))
    db.commit()
    return {"answer": answer}
