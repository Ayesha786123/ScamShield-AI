import streamlit as st

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ScamShield AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── GLOBAL CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

*, html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Dark navy base */
.stApp {
    background:
        radial-gradient(ellipse at 10% 5%,  rgba(30,58,138,0.25) 0%, transparent 45%),
        radial-gradient(ellipse at 90% 10%, rgba(88,28,135,0.20) 0%, transparent 40%),
        radial-gradient(ellipse at 50% 95%, rgba(6,182,212,0.10) 0%, transparent 40%),
        #06090f;
    color: #f1f5f9;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1328 0%, #080c1a 100%);
    border-right: 1px solid rgba(56,189,248,0.10);
}
section[data-testid="stSidebar"] .stRadio > label {
    font-weight: 600;
    color: #94a3b8;
    font-size: 11px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}

/* Buttons */
.stButton > button {
    border-radius: 10px !important;
    border: none !important;
    background: linear-gradient(135deg, #1d4ed8 0%, #4f46e5 50%, #7c3aed 100%) !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    padding: 10px 20px !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 15px rgba(79,70,229,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(124,58,237,0.4) !important;
}

/* Inputs */
.stTextInput input, .stTextArea textarea {
    background: rgba(15,23,42,0.8) !important;
    color: #f1f5f9 !important;
    border: 1px solid rgba(56,189,248,0.20) !important;
    border-radius: 10px !important;
    font-size: 14px !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: rgba(99,102,241,0.6) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important;
}

/* Metrics */
[data-testid="stMetric"] {
    background: rgba(15,23,42,0.7);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 16px 20px;
    backdrop-filter: blur(8px);
}
[data-testid="stMetricValue"] {
    font-weight: 800;
    color: #38bdf8;
}

/* Expanders */
.streamlit-expanderHeader {
    background: rgba(15,23,42,0.6) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 10px !important;
    color: #cbd5e1 !important;
    font-weight: 600 !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(15,23,42,0.5);
    border-radius: 10px;
    padding: 4px;
}
.stTabs [data-baseweb="tab"] {
    color: #64748b;
    font-weight: 600;
    border-radius: 8px;
}
.stTabs [aria-selected="true"] {
    background: rgba(56,189,248,0.15);
    color: #38bdf8;
}

/* File uploader */
section[data-testid="stFileUploader"] {
    background: rgba(15,23,42,0.5);
    border: 1px dashed rgba(56,189,248,0.25);
    border-radius: 12px;
}

/* Alerts */
.stAlert {
    border-radius: 10px !important;
}

/* Divider */
hr {
    border-color: rgba(255,255,255,0.06) !important;
}

/* Download button */
.stDownloadButton > button {
    border-radius: 10px !important;
    border: 1px solid rgba(56,189,248,0.30) !important;
    background: rgba(14,165,233,0.15) !important;
    color: #38bdf8 !important;
    font-weight: 700 !important;
}
</style>
""", unsafe_allow_html=True)

# ─── SESSION STATE DEFAULTS ───────────────────────────────────────────────────
if "nav_page" not in st.session_state:
    st.session_state["nav_page"] = "Dashboard"
if "privacy_mode" not in st.session_state:
    st.session_state["privacy_mode"] = False
if "demo_mode" not in st.session_state:
    st.session_state["demo_mode"] = False

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 10px 0 20px 0;">
        <div style="font-size: 36px; filter: drop-shadow(0 0 12px rgba(56,189,248,0.5));">🛡️</div>
        <div style="font-size: 18px; font-weight: 800; color: #f8fafc; letter-spacing: 0.5px;">
            SCAMSHIELD AI
        </div>
        <div style="font-size: 11px; color: #475569; letter-spacing: 1px; text-transform: uppercase; margin-top: 2px;">
            Threat Intelligence Platform
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    def nav_button(label, page_key, icon=""):
        is_active = st.session_state.get("nav_page") == page_key
        style = (
            "background: rgba(56,189,248,0.12); border-left: 3px solid #38bdf8; color: #38bdf8;"
            if is_active else
            "background: transparent; color: #94a3b8;"
        )
        clicked = st.button(
            f"{icon}  {label}" if icon else label,
            key=f"nav_{page_key}",
            use_container_width=True
        )
        if clicked:
            st.session_state["nav_page"] = page_key
            st.rerun()

    nav_button("Dashboard", "Dashboard", "🏠")

    st.markdown('<div style="font-size:10px;color:#334155;letter-spacing:1.5px;text-transform:uppercase;padding:10px 0 4px 4px;">ANALYZE</div>', unsafe_allow_html=True)
    nav_button("Message Scanner", "Message Scanner", "💬")
    nav_button("URL Scanner", "URL Scanner", "🔗")
    nav_button("Screenshot Scanner", "Screenshot Scanner", "🖼️")
    nav_button("Voice Scanner", "Voice Scanner", "🎙️")
    nav_button("QR Scanner", "QR Scanner", "📱")

    st.markdown('<div style="font-size:10px;color:#334155;letter-spacing:1.5px;text-transform:uppercase;padding:10px 0 4px 4px;">INTELLIGENCE</div>', unsafe_allow_html=True)
    nav_button("Threat Analysis", "Threat Analysis", "🧬")

    st.markdown('<div style="font-size:10px;color:#334155;letter-spacing:1.5px;text-transform:uppercase;padding:10px 0 4px 4px;">HISTORY</div>', unsafe_allow_html=True)
    nav_button("Scan History", "Scan History", "📜")
    nav_button("Compare Scans", "Compare Scans", "⚖️")

    st.markdown('<div style="font-size:10px;color:#334155;letter-spacing:1.5px;text-transform:uppercase;padding:10px 0 4px 4px;">ANALYTICS</div>', unsafe_allow_html=True)
    nav_button("Analytics", "Analytics", "📊")

    st.divider()
    nav_button("Reports", "Reports", "📋")
    nav_button("Settings", "Settings", "⚙️")

    st.divider()

    # Status Indicator
    st.markdown("""
    <div style="
        display: flex; align-items: center; gap: 8px;
        padding: 8px 12px;
        background: rgba(16,185,129,0.08);
        border: 1px solid rgba(16,185,129,0.20);
        border-radius: 8px;
    ">
        <div style="
            width: 8px; height: 8px;
            background: #10b981;
            border-radius: 50%;
            box-shadow: 0 0 6px #10b981;
            animation: pulse 2s infinite;
        "></div>
        <div style="font-size: 12px; font-weight: 600; color: #34d399;">
            Protection Engine Active
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.get("privacy_mode"):
        st.markdown('<div style="margin-top:6px;font-size:11px;color:#60a5fa;text-align:center;">🔒 Privacy Mode ON</div>', unsafe_allow_html=True)
    if st.session_state.get("demo_mode"):
        st.markdown('<div style="margin-top:4px;font-size:11px;color:#fbbf24;text-align:center;">🧪 Demo Mode ON</div>', unsafe_allow_html=True)

# ─── PAGE ROUTER ──────────────────────────────────────────────────────────────
page = st.session_state.get("nav_page", "Dashboard")

try:
    if page == "Dashboard":
        from pages.dashboard import show_dashboard_page
        show_dashboard_page()

    elif page == "Message Scanner":
        from pages.message_scanner_page import show_message_scanner_page
        show_message_scanner_page()

    elif page == "URL Scanner":
        from pages.url_scanner_page import show_url_scanner_page
        show_url_scanner_page()

    elif page == "Screenshot Scanner":
        from pages.screenshot_scanner_page import show_screenshot_scanner_page
        show_screenshot_scanner_page()

    elif page == "Voice Scanner":
        from pages.voice_scanner_page import show_voice_scanner_page
        show_voice_scanner_page()

    elif page == "QR Scanner":
        from pages.qr_scanner_page import show_qr_scanner_page
        show_qr_scanner_page()

    elif page == "Threat Analysis":
        from pages.threat_analysis import show_threat_analysis_page
        show_threat_analysis_page()

    elif page == "Scan History":
        from pages.history import show_history_page
        show_history_page()

    elif page == "Compare Scans":
        from pages.compare_scans import show_compare_scans_page
        show_compare_scans_page()

    elif page == "Analytics":
        from pages.analytics import show_analytics_page
        show_analytics_page()

    elif page == "Reports":
        from pages.reports import show_reports_page
        show_reports_page()

    elif page == "Settings":
        from pages.settings import show_settings_page
        show_settings_page()

    else:
        from pages.dashboard import show_dashboard_page
        show_dashboard_page()

except Exception as e:
    st.error(f"Page load error: {e}")
    st.info("An error occurred loading this page. Please check the error above and try again.")
    import traceback
    st.code(traceback.format_exc())