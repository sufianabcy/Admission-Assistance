"""
EduPilot — Redesigned Sidebar.
Clean, minimal, professional filter panel with JEE rank input.
"""

import streamlit as st

# ── Dropdown options ──────────────────────────────────────────
EXAMS = ["", "JEE Main", "JEE Advanced", "BITSAT", "VITEEE", "KCET", "MHT-CET", "WBJEE", "COMEDK"]
CATEGORIES = ["", "General", "OBC", "EWS", "SC", "ST", "PwD"]
QUOTAS = ["All_India", "Home_State", "Management", "NRI"]
BRANCHES = ["", "CSE", "ECE", "Mech", "Civil", "EE", "AI/ML", "Chemical", "Biotech", "IT"]
STATES = [
    "",
    "Andhra Pradesh", "Bihar", "Chhattisgarh", "Delhi",
    "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand",
    "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra",
    "Odisha", "Punjab", "Rajasthan", "Tamil Nadu",
    "Telangana", "Uttar Pradesh", "Uttarakhand", "West Bengal",
]


def render_sidebar() -> dict:
    """Render a professional filter sidebar for students."""

    st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #fafafa 0%, #f5f5f5 100%);
            border-right: 1px solid #ececec;
        }
        [data-testid="stSidebar"] .stSelectbox label,
        [data-testid="stSidebar"] .stSlider label,
        [data-testid="stSidebar"] .stNumberInput label {
            color: #444 !important;
            font-size: 13px !important;
            font-weight: 600 !important;
            letter-spacing: 0.01em !important;
            text-transform: uppercase !important;
        }
        [data-testid="stSidebar"] .stSelectbox > div > div {
            border-radius: 10px !important;
            border-color: #e0e0e0 !important;
        }
        [data-testid="stSidebar"] .stNumberInput > div > div > input {
            border-radius: 10px !important;
        }
        .sidebar-title {
            font-size: 17px;
            font-weight: 800;
            color: #0a0a0a;
            margin-bottom: 6px;
            margin-top: 8px;
            letter-spacing: -0.01em;
        }
        .sidebar-section {
            font-size: 11px;
            font-weight: 700;
            color: #aaa;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin: 18px 0 6px 0;
        }
    </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown('<div class="sidebar-title">🎯 Your Profile</div>', unsafe_allow_html=True)
        st.caption("Set your filters to get personalised results.")

        st.markdown('<div class="sidebar-section">Entrance Exam</div>', unsafe_allow_html=True)
        exam = st.selectbox("Entrance Exam", EXAMS, label_visibility="collapsed")
        category = st.selectbox("Category", CATEGORIES)
        quota = st.selectbox("Quota", QUOTAS, index=0)

        st.divider()
        st.markdown('<div class="sidebar-section">Rank & Budget</div>', unsafe_allow_html=True)

        rank_raw = st.number_input(
            "JEE Rank (optional)",
            min_value=1,
            max_value=250_000,
            value=None,
            step=1,
            placeholder="e.g. 45000",
            help="Your JEE Main / Advanced closing rank (1 – 2,50,000)",
        )
        # Validate rank
        rank = None
        if rank_raw is not None:
            rank = int(rank_raw)

        budget_max = st.slider(
            "Max Annual Fee (₹)",
            min_value=50_000,
            max_value=2_000_000,
            value=500_000,
            step=50_000,
            format="₹%d",
        )

        st.divider()
        st.markdown('<div class="sidebar-section">Location & Branch</div>', unsafe_allow_html=True)
        state = st.selectbox("Target State", STATES)
        branch = st.selectbox("Preferred Branch", BRANCHES)

        st.divider()
        st.markdown('<div class="sidebar-section">About EduPilot</div>', unsafe_allow_html=True)
        st.caption(
            "Uses Google Gemini for chat and HuggingFace for lightning-fast local RAG retrieval."
        )
        st.code("LLM:    gemini-1.5-flash\nEmbed:  all-MiniLM-L6-v2", language="text")

        with st.expander("💡 Example questions"):
            st.markdown(
                "- Show CSE colleges under ₹2L in Tamil Nadu\n"
                "- Can I get NIT Trichy with JEE rank 45000 OBC?\n"
                "- When does VIT application close?\n"
                "- Best BITS campus for CS?\n"
                "- IIT cutoffs for SC category 2024\n"
                "- Compare IIT Delhi vs IIT Bombay for ECE"
            )

    return {
        "exam":       exam or None,
        "category":   category or None,
        "quota":      quota,
        "state":      state or None,
        "branch":     branch or None,
        "budget_max": budget_max,
        "rank":       rank,
    }
