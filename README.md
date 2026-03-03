# EduPilot – AI Powered College Admission Intelligence Platform

Personalised admissions guidance for Indian engineering aspirants. Students set filters (exam, rank, budget, state, branch) and chat with an AI counsellor that returns full, ranked college lists with details — not just the “top 3”.

---

## Features

- AI-based college filtering with rich metadata
- Full filtered results (no truncation to top 3)
- Smart Agent Chat (LangGraph + LangChain)
- Dashboard-like insights in a clean Streamlit UI
- Secure API integration (no keys in frontend, `.env` only)
- Simple environment variable configuration

---

## Tech Stack

- Frontend: Streamlit (Python)
- Backend: Python, LangChain, LangGraph, Groq LLM
- Database: ChromaDB (local persisted vector store)

---

## Installation

```bash
git clone git@github.com:sufianabcy/Admission-Assistance.git
cd Admission-Assistance
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

---

## Environment Setup

```bash
cp .env.example .env
```

Then set your values in `.env`:

- GROQ_API_KEY=your_groq_api_key_here  ← required
- DATA_PATH=./data/colleges.json       ← optional
- CHROMA_PATH=./chroma_db              ← optional

Generic placeholders (for portability with common hosts):

- API_KEY=your_api_key_here
- DATABASE_URL=your_database_url_here
- SECRET_KEY=your_secret_here
- PORT=5000

The app validates required variables at startup and stops if `GROQ_API_KEY` is missing.

---

## Run Locally

```bash
streamlit run app.py
```

The app opens at http://localhost:8501

---

## Production Deployment

You can deploy on any platform that supports Python web processes.

- Streamlit Community Cloud
  - Connect the GitHub repo and select `app.py`.
  - Add environment secrets (at least `GROQ_API_KEY`).

- Render / Railway
  - Build: `pip install -r requirements.txt`
  - Start: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
  - Set env vars in the dashboard (never commit `.env`).

Note: Vercel is optimized for Node runtimes; Render/Railway/Streamlit Cloud are recommended for Streamlit.

---

## Security Notice

- No API keys are committed. `.env` is ignored by Git.
- Secrets must be provided via environment variables in production.
- If you previously placed keys in code, move them to `.env` and use `os.environ.get()` access; never expose secrets in the UI.

---

## Project Structure

```
Edu-Pilot-main/
├── app.py                  # Main Streamlit app (routing/UI)
├── requirements.txt        # Python dependencies
├── .env.example            # Safe template (no secrets)
├── agent/
│   ├── config.py           # Env loading + validation
│   ├── graph.py            # LangGraph agent (RAG + chat)
│   ├── ingest.py           # JSON → ChromaDB ingestion (idempotent)
│   ├── prompts.py          # System prompt
│   └── retriever.py        # Chroma retriever with filters
├── ui/
│   ├── chat.py             # Chat components
│   └── sidebar.py          # Filter sidebar
└── data/
    ├── colleges.json       # Sample dataset (auto-generated if missing)
    └── generate_data.py    # Dataset generator
```

---

## Maintenance

- Rebuild vector store after dataset changes:

```bash
python -c "from agent.ingest import ingest; ingest()"
```

- Lint/syntax check quickly:

```bash
python -m py_compile app.py agent/*.py ui/*.py
```

---

Made with ❤️ to help students make confident college choices.
