"""
EduPilot — LangGraph StateGraph.
LLM:  Groq (primary: llama-3.3-70b-versatile, fallback: llama-3.1-8b-instant)
RAG:  Context retrieved from ChromaDB and injected into system prompt.

Two-node graph: retrieve → agent → END
"""

import logging
import time
from dotenv import load_dotenv
from typing import Annotated

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict

from agent.config import LLM_API_KEY, LLM_MODEL, LLM_TEMPERATURE, MEMORY_K
from agent.prompts import SYSTEM_PROMPT
from agent.retriever import get_retriever

load_dotenv()
log = logging.getLogger(__name__)

# Groq fallback models — all confirmed active on Groq as of 2025
FALLBACK_MODELS = [
    "llama-3.1-8b-instant",
    "llama3-70b-8192",
    "llama3-8b-8192",
]


# ── State ─────────────────────────────────────────────────────
class AgentState(TypedDict):
    messages:      Annotated[list[BaseMessage], add_messages]
    filters:       dict
    context:       str
    college_count: int


# ── LLM call ─────────────────────────────────────────────────
def _call_llm(model: str, system: str, history: list[BaseMessage]) -> str:
    """Call Groq with the given model and message history."""
    llm = ChatGroq(
        model=model,
        api_key=LLM_API_KEY,
        temperature=LLM_TEMPERATURE,
        max_tokens=1024,   # cap output to keep total within free-tier TPM
    )
    messages = [SystemMessage(content=system)] + history
    response = llm.invoke(messages)
    return response.content


# ── RAG retrieval ─────────────────────────────────────────────
def _retrieve_context(query: str, filters: dict) -> tuple[str, int]:
    """Retrieve relevant college docs from ChromaDB and format as context."""
    try:
        retriever = get_retriever(
            state=filters.get("state"),
            exam=filters.get("exam"),
            budget_max=filters.get("budget_max"),
            branch=filters.get("branch"),
        )
        docs = retriever.invoke(query)
        if not docs:
            return "No specific college data found for this query.", 0

        docs = sorted(docs, key=lambda x: x.metadata.get("nirf_rank", 999))
        ctx = "\n\n---\n\n".join(
            f"**{doc.metadata.get('name', 'College')}**\n{doc.page_content}"
            for doc in docs
        )
        return ctx, len(docs)
    except Exception as e:
        log.warning("[EduPilot] Retrieval failed: %s", e)
        return "", 0


# ── Graph builder ─────────────────────────────────────────────
def build_graph():

    def retrieve(state: AgentState) -> dict:
        messages = state["messages"]
        filters  = state.get("filters", {})
        query = next(
            (m.content for m in reversed(messages) if isinstance(m, HumanMessage)),
            "",
        )
        context, count = _retrieve_context(query, filters)
        return {"context": context, "college_count": count}

    def call_model(state: AgentState) -> dict:
        messages = state["messages"]
        context  = state.get("context", "")
        filters  = state.get("filters", {})
        count    = state.get("college_count", 0)

        trimmed = messages[-(MEMORY_K * 2):] if len(messages) > MEMORY_K * 2 else messages

        # Build system prompt
        filter_info = ""
        if any(filters.values()):
            parts = [f"{k}={v}" for k, v in filters.items() if v and k not in ("budget_max", "rank")]
            if filters.get("budget_max"):
                parts.append(f"budget=₹{filters['budget_max']:,}")
            if filters.get("rank"):
                parts.append(f"JEE_rank={filters['rank']:,}")
            filter_info = f"\nStudent profile: {', '.join(parts)}"

        system = SYSTEM_PROMPT + filter_info
        if count > 0:
            system += f"\n\nTotal matching colleges found: {count}."
            system += (
                f"\n=== Retrieved College Data ===\n{context}\n=== End of Data ===\n\n"
                f"Strictly list ALL {count} matching colleges. "
                "DO NOT TRUNCATE or say 'some of the colleges'."
            )
        else:
            system += (
                "\n\nNo matching colleges found for this student profile and query. "
                "State that clearly and suggest adjusting filters."
            )

        history = list(trimmed)
        if not history:
            return {"messages": [AIMessage(content="Please ask a question about Indian college admissions.")]}

        models_to_try = [LLM_MODEL] + [m for m in FALLBACK_MODELS if m != LLM_MODEL]
        last_err = ""

        for model in models_to_try:
            try:
                content = _call_llm(model, system, history)
                return {"messages": [AIMessage(content=content)]}
            except Exception as e:
                last_err = str(e)
                log.warning("[EduPilot] Model %s failed: %s", model, e)
                if "429" in str(e) or "rate_limit" in str(e).lower():
                    time.sleep(2)
                continue

        return {"messages": [AIMessage(content=_error_msg(last_err))]}

    graph = StateGraph(AgentState)
    graph.add_node("retrieve", retrieve)
    graph.add_node("agent", call_model)
    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "agent")
    graph.add_edge("agent", END)
    return graph.compile(checkpointer=MemorySaver())


def _error_msg(err: str) -> str:
    e = err.lower()
    if "401" in e or "invalid api key" in e or "authentication" in e:
        return "⚠️ **Invalid API key.** Check your `.env` file for `GROQ_API_KEY`."
    if "429" in e or "rate_limit" in e:
        return "⚠️ **Rate limit hit.** Please wait a moment and try again."
    if "connection" in e or "timeout" in e:
        return "⚠️ **Connection error.** Check your internet connection and try again."
    return f"⚠️ LLM temporarily unavailable. Please try again.\n\n`{err[:200]}`"


# ── Singleton ─────────────────────────────────────────────────
GRAPH = build_graph()
