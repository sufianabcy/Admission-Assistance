"""
EduPilot — Production-Ready SaaS Admissions Assistant.
Clean, optimized, single-file app router with premium UI.
"""

import uuid
import streamlit as st
import hashlib
from pathlib import Path
from langchain_core.messages import HumanMessage
from agent.config import DATA_PATH

# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title="EduPilot | Premium Admissions Assistant",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Session State Initialisation ─────────────────────────────
_defaults = {
    "page": "home",
    "session_id": str(uuid.uuid4()),
    "messages": [],
    "filters": {},
    "logged_in": False,
    "username": "Aditya Kumar",
    "user_email": "aditya@example.com",
    "saved_colleges": ["IIT Bombay", "NIT Trichy", "BITS Pilani"],
    "jee_rank": None,
    "category": "General",
}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Global CSS ────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    /* ── Animations ───────────────────────────────────────────── */
    @keyframes gradientBG {
        0%   { background-position: 0% 50%;   }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%;   }
    }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(28px); }
        to   { opacity: 1; transform: translateY(0);    }
    }

    /* ── Global Styles ────────────────────────────────────────── */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background: linear-gradient(-45deg, #fdfbfb, #ebedee, #fdfcfb, #e8e4f0);
        background-size: 400% 400%;
        animation: gradientBG 18s ease infinite;
        color: #111;
    }
    [data-testid="stHeader"] { display: none !important; }
    .st-emotion-cache-18ni77z { padding-top: 0 !important; }

    /* ── Fixed Glassmorphism Header ──────────────────────────── */
    .header-anchor {
        position: fixed;
        top: 0; left: 0;
        width: 100%;
        height: 72px;
        background: rgba(255, 255, 255, 0.78);
        backdrop-filter: blur(22px) saturate(200%);
        border-bottom: 1px solid rgba(0,0,0,0.05);
        z-index: 999999;
        display: flex;
        align-items: center;
        padding: 0 5%;
        box-shadow: 0 2px 24px rgba(0,0,0,0.04);
    }
    .main .block-container {
        padding-top: 90px !important;
        padding-bottom: 40px !important;
    }

    /* ── Nav Buttons ─────────────────────────────────────────── */
    div[data-testid="stColumn"] button[kind="secondary"] {
        background: transparent !important;
        border: none !important;
        color: #555 !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        padding: 8px 16px !important;
        border-radius: 10px !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    div[data-testid="stColumn"] button[kind="secondary"]:hover {
        color: #000 !important;
        background: rgba(0,0,0,0.05) !important;
        transform: translateY(-1px);
    }
    div[data-testid="stColumn"] button[kind="primary"] {
        background: linear-gradient(135deg, #111 0%, #333 100%) !important;
        color: #fff !important;
        border-radius: 22px !important;
        padding: 8px 26px !important;
        font-weight: 600 !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.18) !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    div[data-testid="stColumn"] button[kind="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 28px rgba(0,0,0,0.22) !important;
    }

    /* ── Hero Typography ─────────────────────────────────────── */
    .hero-title {
        font-size: 64px;
        font-weight: 800;
        letter-spacing: -0.03em;
        background: linear-gradient(135deg, #111 0%, #444 50%, #111 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: fadeInUp 0.9s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        opacity: 0;
        margin-bottom: 12px;
        line-height: 1.1;
    }
    .hero-subtitle {
        color: #555;
        font-size: 20px;
        margin-bottom: 52px;
        animation: fadeInUp 0.9s cubic-bezier(0.16, 1, 0.3, 1) 0.15s forwards;
        opacity: 0;
    }

    /* ── Search Bar ──────────────────────────────────────────── */
    .home-search-wrap {
        max-width: 60% !important;
        margin: 0 auto !important;
        animation: fadeInUp 0.9s cubic-bezier(0.16, 1, 0.3, 1) 0.3s forwards;
        opacity: 0;
    }
    [data-testid="stTextInput"] input {
        height: 60px !important;
        border-radius: 18px !important;
        border: 2px solid transparent !important;
        background: rgba(255, 255, 255, 0.82) !important;
        backdrop-filter: blur(14px) !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.07) !important;
        padding-left: 26px !important;
        font-size: 17px !important;
        font-weight: 500 !important;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    [data-testid="stTextInput"] input:focus {
        border-color: #222 !important;
        box-shadow: 0 16px 48px rgba(0,0,0,0.13) !important;
        transform: translateY(-2px);
        background: rgba(255,255,255,1) !important;
    }

    /* ── Hero Image ──────────────────────────────────────────── */
    .hero-image {
        height: 480px;
        width: 100%;
        max-width: 90%;
        margin: 80px auto;
        background-image: url('https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=1600&q=80');
        background-size: cover;
        background-position: center top;
        border-radius: 28px;
        box-shadow: 0 32px 64px rgba(0,0,0,0.16);
        animation: fadeInUp 1.1s cubic-bezier(0.16, 1, 0.3, 1) 0.45s forwards;
        opacity: 0;
        transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .hero-image:hover { transform: scale(1.015); }

    /* ── Vision Section ──────────────────────────────────────── */
    .vision-section {
        padding: 64px 0;
        text-align: center;
        max-width: 700px;
        margin: 0 auto;
        animation: fadeInUp 1.1s cubic-bezier(0.16, 1, 0.3, 1) 0.6s forwards;
        opacity: 0;
    }

    /* ── Feature Cards ─────────────────────────────────────── */
    .feature-card {
        background: rgba(255,255,255,0.75);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0,0,0,0.06);
        border-radius: 20px;
        padding: 28px 24px;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        box-shadow: 0 4px 16px rgba(0,0,0,0.04);
    }
    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 16px 40px rgba(0,0,0,0.1);
    }
    .feature-card .icon { font-size: 36px; margin-bottom: 12px; }
    .feature-card h4 { font-weight: 700; font-size: 17px; margin: 0 0 8px 0; }
    .feature-card p  { color: #666; font-size: 14px; line-height: 1.5; margin: 0; }

    /* ── Dashboard Cards ──────────────────────────────────────── */
    .dash-stat-card {
        background: rgba(255,255,255,0.82);
        border: 1px solid rgba(0,0,0,0.06);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 16px rgba(0,0,0,0.04);
    }
    .dash-stat-num  { font-size: 32px; font-weight: 800; color: #111; }
    .dash-stat-label{ font-size: 13px; color: #777; margin-top: 4px; }

    /* ── Profile Card ─────────────────────────────────────────── */
    .profile-card {
        background: rgba(255,255,255,0.85);
        border: 1px solid rgba(0,0,0,0.06);
        border-radius: 18px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.04);
    }

    /* ── Footer ──────────────────────────────────────────────── */
    .premium-footer {
        background-color: #0f0f0f;
        color: #888;
        padding: 52px 5%;
        border-top: 1px solid #1e1e1e;
        margin-top: 100px;
        width: 100%;
        font-size: 14px;
        box-shadow: inset 0 24px 48px rgba(0,0,0,0.25);
    }
    .footer-content {
        display: flex;
        justify-content: space-between;
        align-items: center;
        max-width: 1200px;
        margin: 0 auto;
    }
    .footer-left  { display: flex; flex-direction: column; gap: 8px; }
    .footer-right { display: flex; gap: 30px; align-items: center; }
    .footer-logo  { color: #fff; font-weight: 800; font-size: 20px; letter-spacing: -0.01em; }
    .footer-tagline { color: #666; font-size: 13px; }
    .footer-links { display: flex; gap: 24px; list-style: none; padding: 0; margin: 0; }
    .footer-links a {
        color: #888;
        text-decoration: none;
        transition: color 0.3s ease;
        font-weight: 500;
    }
    .footer-links a:hover { color: #fff; }

    /* ── Responsive ──────────────────────────────────────────── */
    @media (max-width: 768px) {
        .hero-title     { font-size: 40px; }
        .hero-image     { height: 280px; border-radius: 18px; }
        .home-search-wrap { max-width: 95% !important; }
        .footer-content { flex-direction: column; text-align: center; gap: 30px; }
        .footer-right   { flex-direction: column; gap: 15px; }
        .footer-links   { justify-content: center; }
    }
</style>
""", unsafe_allow_html=True)


# ── Navigation Router ─────────────────────────────────────────
def go_to(page: str):
    st.session_state.page = page
    st.rerun()


# ── Sticky Header ─────────────────────────────────────────────
st.markdown('<div class="header-anchor"></div>', unsafe_allow_html=True)
with st.container():
    h_logo, h_nav, h_auth = st.columns([1.5, 3, 1.5])
    with h_logo:
        st.markdown(
            '<div style="padding-top:10px; font-weight:800; font-size:22px; '
            'letter-spacing:-0.01em;">✦ EduPilot</div>',
            unsafe_allow_html=True,
        )
        if st.button(" ", key="logo_home_btn", help="Go to Home"):
            go_to("home")
    with h_nav:
        n1, n2, n3 = st.columns(3)
        with n1:
            if st.button("Home", key="l_home"):
                go_to("home")
        with n2:
            if st.button("Agent", key="l_agent"):
                go_to("agent")
        with n3:
            if st.button("Dashboard", key="l_dash"):
                go_to("dashboard")
    with h_auth:
        if not st.session_state.logged_in:
            if st.button("Login / Sign Up", key="h_auth", type="primary"):
                st.session_state.logged_in = True
                st.rerun()
        else:
            if st.button("Logout", key="h_logout", type="secondary"):
                st.session_state.logged_in = False
                go_to("home")


# ── Agent initialisation ──────────────────────────────────────
from agent.ingest import ensure_ingested
from agent.graph import GRAPH
from ui.sidebar import render_sidebar
from ui.chat import render_chat, render_stream, render_welcome


@st.cache_resource
def init_db(data_hash: str):
    ensure_ingested()
    return True


def get_data_hash() -> str:
    p = Path(DATA_PATH)
    return hashlib.md5(p.read_bytes()).hexdigest() if p.exists() else "none"


# ── Home Page ─────────────────────────────────────────────────
def render_home_page():
    st.markdown('<div style="text-align: center; margin-top: 80px;">', unsafe_allow_html=True)
    st.markdown('<h1 class="hero-title">Elevate Your Future.</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="hero-subtitle">Personalised admissions guidance powered by AI.</p>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="home-search-wrap">', unsafe_allow_html=True)
    search_input = st.text_input(
        "Search colleges...",
        placeholder="Find colleges by name, city, branch, or rank...",
        label_visibility="collapsed",
        key="search_h",
    )
    if search_input:
        st.session_state["_injected_prompt"] = f"Tell me about colleges related to: {search_input}"
        go_to("agent")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="hero-image"></div>', unsafe_allow_html=True)

    # ── Feature highlights ────────────────────────────────────
    st.markdown(
        '<h2 style="text-align:center; font-weight:800; font-size:30px; margin-bottom:28px;">Why EduPilot?</h2>',
        unsafe_allow_html=True,
    )
    fc1, fc2, fc3 = st.columns(3)
    features = [
        ("🔍", "Smart Search", "Filter by rank, budget, branch, and state to find your perfect match."),
        ("🤖", "AI Counsellor", "Real-time answers from our RAG-powered agent trained on college data."),
        ("🔒", "100% Private", "All inference runs locally. Your data is never sent to any server."),
    ]
    for col, (icon, title, desc) in zip([fc1, fc2, fc3], features):
        with col:
            st.markdown(
                f'<div class="feature-card">'
                f'<div class="icon">{icon}</div>'
                f'<h4>{title}</h4>'
                f'<p>{desc}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown('<div class="vision-section">', unsafe_allow_html=True)
    st.markdown(
        '<h2 style="font-weight:800; font-size:30px; margin-bottom:18px;">Our Vision</h2>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p style="color:#444; line-height:1.75; font-size:17px;">'
        "Helping students make smarter college decisions through transparent, "
        "AI-powered insights while keeping data 100% private."
        "</p>",
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)


# ── Agent Page ────────────────────────────────────────────────
def render_agent_page():
    filters = render_sidebar()
    st.session_state.filters = filters

    if not st.session_state.messages:
        render_welcome(filters=filters)

    if "_injected_prompt" in st.session_state:
        injected = st.session_state.pop("_injected_prompt")
        st.session_state.messages.append({"role": "user", "content": injected})

    render_chat(st.session_state.messages)

    if prompt := st.chat_input("Ask about ranks, fees, cutoffs, or specific colleges..."):
        f = st.session_state.filters

        # Build enriched prompt with profile context
        filter_parts = []
        for k, v in f.items():
            if not v or k in ("budget_max", "rank"):
                continue
            filter_parts.append(f"{k}: {v}")
        if f.get("budget_max"):
            filter_parts.append(f"Budget: ₹{f['budget_max']:,}/yr")
        if f.get("rank"):
            filter_parts.append(f"JEE Rank: {f['rank']:,}")

        enriched_prompt = (
            f"{prompt}\n\n[Student Profile: {' | '.join(filter_parts)}]"
            if filter_parts else prompt
        )

        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

        config = {"configurable": {"thread_id": st.session_state.session_id}}
        input_msg = {
            "messages": [HumanMessage(content=enriched_prompt)],
            "filters": f,
            "context": "",
        }
        with st.chat_message("assistant", avatar="🎓"):
            response = render_stream(GRAPH, input_msg, config)

        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()


# ── Dashboard Page ─────────────────────────────────────────────
def render_dashboard_page():
    if not st.session_state.logged_in:
        st.warning("⚠️ Please log in to access your Dashboard.")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Log In Now", type="primary"):
            st.session_state.logged_in = True
            st.rerun()
        return

    st.markdown(
        f'<h2 style="font-weight:800; font-size:28px; margin-bottom:24px;">'
        f'👋 Welcome back, {st.session_state.username.split()[0]}!</h2>',
        unsafe_allow_html=True,
    )

    # ── Stats row ───────────────────────────────────────────
    s1, s2, s3, s4 = st.columns(4)
    stats = [
        (str(len(st.session_state.saved_colleges)), "Shortlisted"),
        (str(len(st.session_state.messages) // 2), "Questions Asked"),
        ("2025", "Admission Year"),
        (st.session_state.filters.get("category") or "General", "Category"),
    ]
    for col, (num, label) in zip([s1, s2, s3, s4], stats):
        with col:
            st.markdown(
                f'<div class="dash-stat-card">'
                f'<div class="dash-stat-num">{num}</div>'
                f'<div class="dash-stat-label">{label}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Two-column layout ───────────────────────────────────
    col_left, col_right = st.columns([2, 1])

    with col_left:
        # Profile card
        f = st.session_state.filters
        rank_text = f"JEE Rank: **{f['rank']:,}**" if f.get("rank") else "JEE Rank: *Not set*"
        budget_text = f"₹{f.get('budget_max', 500000):,}/yr"
        st.markdown(
            f'<div class="profile-card">'
            f'<h3 style="margin:0 0 16px 0; font-weight:800;">👤 Profile</h3>'
            f'<p style="margin:0; line-height:2; color:#333;">'
            f'<strong>Name:</strong> {st.session_state.username}<br>'
            f'<strong>Email:</strong> {st.session_state.user_email}<br>'
            f'{rank_text}<br>'
            f'<strong>Exam:</strong> {f.get("exam") or "Not set"}<br>'
            f'<strong>Branch:</strong> {f.get("branch") or "Not set"}<br>'
            f'<strong>Max Budget:</strong> {budget_text}<br>'
            f'<strong>State:</strong> {f.get("state") or "All India"}'
            f'</p></div>',
            unsafe_allow_html=True,
        )

        # Shortlist
        st.markdown("### 🔖 My Shortlist")
        if not st.session_state.saved_colleges:
            st.info("Your shortlist is empty. Ask the AI agent to recommend colleges!")
        else:
            for i, clg in enumerate(list(st.session_state.saved_colleges)):
                r1, r2 = st.columns([5, 1])
                with r1:
                    st.markdown(
                        f'<div style="background:rgba(255,255,255,0.85); border:1px solid #eee; '
                        f'border-radius:12px; padding:12px 18px; margin-bottom:8px; '
                        f'font-weight:600; font-size:15px;">🎓 {clg}</div>',
                        unsafe_allow_html=True,
                    )
                with r2:
                    if st.button("✕", key=f"rm_{i}_{clg}"):
                        st.session_state.saved_colleges.remove(clg)
                        st.rerun()

    with col_right:
        # Quick navigation
        st.markdown("### 🚀 Quick Actions")
        if st.button("💬 Open AI Agent", use_container_width=True):
            go_to("agent")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🏠 Back to Home", use_container_width=True):
            go_to("home")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 📊 Recent Activity")
        msg_count = len(st.session_state.messages)
        if msg_count == 0:
            st.caption("No conversations yet. Start chatting with the AI Agent!")
        else:
            # Show last 3 user messages
            user_msgs = [m for m in st.session_state.messages if m["role"] == "user"][-3:]
            for m in reversed(user_msgs):
                st.markdown(
                    f'<div style="background:rgba(255,255,255,0.7); border-radius:10px; '
                    f'padding:10px 14px; margin-bottom:8px; font-size:13px; color:#444; '
                    f'border:1px solid #eee;">💬 {m["content"][:80]}{"..." if len(m["content"]) > 80 else ""}</div>',
                    unsafe_allow_html=True,
                )


# ── Footer ────────────────────────────────────────────────────
def render_footer():
    st.markdown("""
    <div class="premium-footer">
        <div class="footer-content">
            <div class="footer-left">
                <div class="footer-logo">✦ EduPilot</div>
                <div class="footer-tagline">100% Local AI. 0% Data Shared.</div>
            </div>
            <div class="footer-right">
                <ul class="footer-links">
                    <li><a href="#">Privacy Policy</a></li>
                    <li><a href="#">Terms of Use</a></li>
                    <li><a href="#">Contact</a></li>
                    <li><a href="#">GitHub</a></li>
                </ul>
                <div style="color:#555;">© 2025 EduPilot</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── Main ──────────────────────────────────────────────────────
def main():
    init_db(get_data_hash())

    page = st.session_state.page
    if page == "home":
        render_home_page()
    elif page == "agent":
        render_agent_page()
    elif page == "dashboard":
        render_dashboard_page()

    render_footer()


if __name__ == "__main__":
    main()
