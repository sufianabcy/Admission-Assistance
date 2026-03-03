"""
EduPilot — Configuration constants.
LLM:        Groq (llama-3.3-70b-versatile, fast & free tier)
Embeddings: all-MiniLM-L6-v2 via HuggingFace (free, local, low memory)
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ── Groq / LLM ────────────────────────────────────────────────
LLM_API_KEY     = os.environ.get("GROQ_API_KEY", "")

# ── Required environment validation ──────────────────────────
# Fail fast in production if critical secrets are missing.
_missing = [name for name in ("GROQ_API_KEY",) if not os.environ.get(name)]
if _missing:
    missing_str = ", ".join(_missing)
    raise SystemExit(
        f"Missing required environment variable(s): {missing_str}.\n"
        f"Create a .env from .env.example and set the values before starting EduPilot."
    )
LLM_MODEL       = "llama-3.3-70b-versatile"   # best quality on Groq free tier
LLM_TEMPERATURE = 0.3

# ── Embeddings (HuggingFace — cloud-friendly, free, low memory) ─────────
EMBED_MODEL     = "all-MiniLM-L6-v2"

# ── ChromaDB ──────────────────────────────────────────────────
CHROMA_PATH     = os.environ.get("CHROMA_PATH", "./chroma_db")
COLLECTION_NAME = "college_compass"

# ── Retriever ─────────────────────────────────────────────────
RETRIEVER_K     = 10   # reduced to stay under Groq free-tier 12K TPM
SCORE_THRESHOLD = 0.1

# ── Conversation memory ───────────────────────────────────────
MEMORY_K        = 4    # reduced to save tokens for response

# ── Data ──────────────────────────────────────────────────────
DATA_PATH       = os.environ.get("DATA_PATH", "./data/colleges.json")
