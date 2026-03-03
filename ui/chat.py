"""
EduPilot — Chat UI helpers.
Premium, centered AI assistant experience with spring-physics animations.
"""

import streamlit as st
from langchain_core.messages import AIMessage


# ── Chat Bubbles & Scroll Logic Styling ─────────────────────────
def inject_chat_css():
    st.markdown("""
    <style>
        /* ── Force Black Text Globally (fixes invisible text) ────────── */
        .stMarkdown, .stMarkdown p, .stMarkdown li, .stMarkdown h1,
        .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown span,
        [data-testid="stChatMessage"] p,
        [data-testid="stChatMessage"] li,
        [data-testid="stChatMessage"] span,
        [data-testid="stChatMessage"] td,
        [data-testid="stChatMessage"] th,
        [data-testid="stChatMessage"] strong,
        [data-testid="stChatMessage"] em,
        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] li,
        [data-testid="stMarkdownContainer"] span {
            color: #111111 !important;
        }

        /* ── Root Layout ──────────────────────────────────────────── */
        .chat-view-root {
            max-width: 860px;
            margin: 0 auto;
            padding-top: 20px;
            padding-bottom: 40px;
        }

        /* ── Message Animations ────────────────────────────────────── */
        @keyframes chatFadeInSlideUp {
            from { opacity: 0; transform: translateY(18px); }
            to   { opacity: 1; transform: translateY(0);    }
        }

        [data-testid="stChatMessage"] {
            border: none !important;
            background-color: transparent !important;
            margin-bottom: 2rem !important;
            animation: chatFadeInSlideUp 0.45s cubic-bezier(0.16, 1, 0.3, 1) forwards !important;
        }

        /* ── User Bubble (Right-aligned) ───────────────────────────── */
        div[data-testid="stChatMessage"]:has(span[aria-label="👤"]) {
            display: flex;
            flex-direction: row-reverse;
            text-align: right;
        }
        div[data-testid="stChatMessage"]:has(span[aria-label="👤"]) .stMarkdown {
            background: linear-gradient(135deg, #111 0%, #222 100%) !important;
            color: #fff !important;
            padding: 14px 22px !important;
            border-radius: 20px 20px 4px 20px !important;
            max-width: 75%;
            font-size: 15px;
            line-height: 1.55;
            box-shadow: 0 8px 24px rgba(0,0,0,0.14);
        }
        div[data-testid="stChatMessage"]:has(span[aria-label="👤"]) .stMarkdown p {
            color: white !important;
        }

        /* ── Assistant Bubble (Left-aligned) ──────────────────────── */
        div[data-testid="stChatMessage"]:has(span[aria-label="🎓"]) {
            display: flex;
            flex-direction: row;
            text-align: left;
        }
        div[data-testid="stChatMessage"]:has(span[aria-label="🎓"]) .stMarkdown {
            background: rgba(255, 255, 255, 0.82) !important;
            backdrop-filter: blur(12px) !important;
            color: #1a1a1a !important;
            padding: 18px 24px !important;
            border-radius: 20px 20px 20px 4px !important;
            max-width: 85%;
            border: 1px solid rgba(0,0,0,0.06);
            font-size: 15px;
            line-height: 1.65;
            box-shadow: 0 4px 16px rgba(0,0,0,0.04);
        }

        /* ── Chat Input ────────────────────────────────────────────── */
        [data-testid="stChatInput"] {
            position: relative !important;
            bottom: auto !important;
            left: auto !important;
            transform: none !important;
            max-width: 100% !important;
            margin: 36px 0 !important;
            padding: 0 !important;
            z-index: 100;
        }
        [data-testid="stChatInput"] > div {
            border: 1.5px solid rgba(0,0,0,0.08) !important;
            border-radius: 18px !important;
            background: rgba(255,255,255,0.88) !important;
            backdrop-filter: blur(12px) !important;
            box-shadow: 0 4px 24px rgba(0,0,0,0.05) !important;
            transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        }
        [data-testid="stChatInput"]:focus-within > div {
            border-color: #222 !important;
            box-shadow: 0 14px 36px rgba(0,0,0,0.11) !important;
            transform: translateY(-2px);
            background: rgba(255,255,255,1) !important;
        }
        [data-testid="stChatInput"] textarea {
            font-size: 16px !important;
            padding: 18px 20px !important;
            line-height: 1.5 !important;
        }

        /* Hide avatars for minimal look */
        [data-testid="stChatMessageAvatar"] {
            display: none !important;
        }

        /* ── Welcome Screen ────────────────────────────────────────── */
        @keyframes welcomeFadeUp {
            from { opacity: 0; transform: translateY(24px); }
            to   { opacity: 1; transform: translateY(0);    }
        }
        .chat-hero-title {
            font-size: 40px;
            font-weight: 800;
            letter-spacing: -0.025em;
            background: linear-gradient(135deg, #111 0%, #555 50%, #111 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 12px;
            animation: welcomeFadeUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }
        .chat-hero-subtitle {
            color: #666;
            font-size: 17px;
            animation: welcomeFadeUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.15s forwards;
            opacity: 0;
        }

        /* ── Chips ─────────────────────────────────────────────────── */
        div[data-testid="stButton"] button {
            border-radius: 10px !important;
            border: 1px solid #e5e5e5 !important;
            background: rgba(255,255,255,0.75) !important;
            color: #333 !important;
            font-size: 14px !important;
            font-weight: 500 !important;
            padding: 10px 16px !important;
            transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
        }
        div[data-testid="stButton"] button:hover {
            background: rgba(255,255,255,1) !important;
            border-color: #ccc !important;
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(0,0,0,0.06) !important;
        }

        @media (max-width: 768px) {
            .chat-hero-title { font-size: 28px; }
            div[data-testid="stChatMessage"]:has(span[aria-label="👤"]) .stMarkdown,
            div[data-testid="stChatMessage"]:has(span[aria-label="🎓"]) .stMarkdown {
                max-width: 92%;
            }
        }
    </style>
    """, unsafe_allow_html=True)


def render_welcome(filters: dict = None) -> None:
    inject_chat_css()
    st.markdown('<div class="chat-view-root">', unsafe_allow_html=True)
    st.markdown("""
        <div style="text-align: center; margin: 60px 0 46px 0;">
            <h2 class="chat-hero-title">How can I help you today?</h2>
            <p class="chat-hero-subtitle">Personalised college guidance powered by local AI.</p>
        </div>
    """, unsafe_allow_html=True)

    chips = [
        "Best NITs for Computer Science?",
        "JoSAA registration guide 2025",
        "IIT Delhi vs IIT Bombay for EE",
        "Colleges with low fees in North India",
        "Top BITS Pilani branches for placements",
        "VIT vs Manipal for CSE?",
    ]
    cols = st.columns(2)
    for i, q in enumerate(chips):
        with cols[i % 2]:
            if st.button(q, key=f"chip_{i}", use_container_width=True):
                st.session_state["_injected_prompt"] = q
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


def render_chat(messages: list[dict]) -> None:
    inject_chat_css()
    st.markdown('<div class="chat-view-root">', unsafe_allow_html=True)
    for msg in messages:
        avatar = "👤" if msg["role"] == "user" else "🎓"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])
    st.markdown('</div>', unsafe_allow_html=True)


def render_stream(graph, input_msg: dict, config: dict) -> str:
    """Stream LLM response token-by-token with a typing cursor."""
    st.markdown('<div class="chat-view-root">', unsafe_allow_html=True)
    response_placeholder = st.empty()
    full_response = ""

    with st.spinner("Thinking..."):
        try:
            for state in graph.stream(input_msg, config, stream_mode="values"):
                messages = state.get("messages", [])
                if not messages:
                    continue
                last_msg = messages[-1]

                if isinstance(last_msg, AIMessage):
                    content = last_msg.content
                    if isinstance(content, str) and content.strip():
                        full_response = content
                        response_placeholder.markdown(full_response + " ▌")

            if full_response:
                response_placeholder.markdown(full_response)
            else:
                full_response = "I'm having trouble generating a response. Please try again."
                response_placeholder.markdown(full_response)

        except Exception as e:
            full_response = f"⚠️ **Error:** {str(e)}"
            response_placeholder.markdown(full_response)

    st.markdown('</div>', unsafe_allow_html=True)
    return full_response
