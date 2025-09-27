# 🧠 Memory 2.0 — Dual-LLM Long-Term Memory

Memory 2.0 is a ready-to-use blueprint for giving large-language-model (LLM) agents **persistent, evolving memory**.  
It combines **two cooperating LLM roles**:

* **Worker LLM** – Handles real-time reasoning and conversation.
* **Memory LLM (Archivist)** – Continuously summarizes, organizes, and retrieves long-term context.

This allows your agent to *remember* facts, preferences, and tasks across weeks or months without re-sending the entire history.

---

## 🌟 Highlights
- 🔎 Retrieval-Augmented Generation (RAG) for precise recall  (In-Progress)
- 📝 Automatic summarization into concise “knowledge cards”  
- 🧩 Works with GPT-4o, Claude, Llama-3 or any API-compatible model  
- 🔒 Optional encryption and retention policies

---

## 🏗️ Architecture

```
User ─▶ API (FastAPI/Express)
       ├─▶ Worker LLM  — real-time responses
       └─▶ Memory LLM ─▶ Vector DB (e.g. Postgres+pgvector, Pinecone)
```

**Flow**
1. **Write** – Worker flags key info → Memory LLM condenses → stores in Vector DB.
2. **Retrieve** – On a new query, Memory LLM finds relevant memories → Worker replies with full context.

---

## 🚀 Quick Start

### 1️⃣ Install
```bash
git clone https://github.com/yourname/memory-2.0.git
cd memory-2.0
pip install fastapi uvicorn openai psycopg2-binary pgvector
```

### 2️⃣ Configure
Create a `.env` file:
```
OPENAI_API_KEY=your_api_key
DATABASE_URL=postgresql://user:pass@localhost:5432/memory
```

### 3️⃣ Run
```bash
uvicorn main:app --reload
```

### 4️⃣ Test
```bash
curl -X POST http://localhost:8000/chat      -H "Content-Type: application/json"      -d '{"message":"Remember that I like robotics."}'
```

---

## 📂 Suggested Structure
```
memory-2.0/
│  README.md
│  main.py            # FastAPI entry point
│  worker_agent.py    # real-time reasoning
│  memory_agent.py    # summarization + retrieval
│  database.py        # vector DB integration
```


## ⚙️ Configuration Ideas
- Choose your **Worker** and **Memory** models independently (e.g. GPT-4o for reasoning, GPT-4-mini for summarization).
- Plug in any **Vector Store** (Pinecone, Weaviate, pgvector).
- Define **Retention** (e.g. summarize or prune after N days).

---

## 💡 Use Cases
- Persistent personal AI assistants
- Research and project-planning agents
- Game NPCs with life-long memories
- Knowledge management for teams

---

## 🛡️ Security
- Encrypt data at rest (e.g. AES-256)
- Redact or hash sensitive content before storage
- Support user-initiated memory deletion

---

## 🤝 Contributing
Pull requests and new ideas—alternative DBs, better summarizers, dashboards—are welcome!

---

## 📜 License
MIT License © 2025 Your Name
