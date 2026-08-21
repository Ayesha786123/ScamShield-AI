import streamlit as st
from src.database import get_analytics_summary

def show_dashboard_page():
    # Hero Section
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(30,58,138,0.6) 0%, rgba(15,23,42,0.8) 50%, rgba(88,28,135,0.5) 100%);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 24px;
        padding: 40px;
        margin-bottom: 30px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    ">
        <div style="display:flex; align-items:center; justify-content:space-between;">
            <div>
                <div style="font-size: 14px; font-weight: 700; color: #38bdf8; letter-spacing: 2px; text-transform: uppercase;">
                    🛡️ AI-Powered Scam Intelligence Platform
                </div>
                <h1 style="font-size: 42px; font-weight: 800; color: #ffffff; margin: 10px 0 15px 0;">
                    SCAMSHIELD AI
                </h1>
                <p style="font-size: 18px; color: #cbd5e1; max-width: 650px; line-height: 1.6;">
                    Detect. Understand. Protect. Analyze suspicious messages, links, screenshots, QR codes, and voice recordings before they become a threat.
                </p>
            </div>
            <div style="font-size: 90px; filter: drop-shadow(0 0 20px rgba(56,189,248,0.4));">
                🛡️
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # CTA Buttons
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("💬 START MESSAGE SCAN", use_container_width=True, type="primary"):
            st.session_state["nav_page"] = "Message Scanner"
            st.rerun()
    with col2:
        if st.button("📊 VIEW SECURITY ANALYTICS", use_container_width=True):
            st.session_state["nav_page"] = "Analytics"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Real Database Metrics
    analytics = get_analytics_summary()
    total = analytics["total"]
    risk_counts = analytics["risk_counts"]
    high_cnt = risk_counts.get("HIGH", 0) + risk_counts.get("CRITICAL", 0)
    med_cnt = risk_counts.get("MEDIUM", 0)
    safe_cnt = risk_counts.get("SAFE", 0) + risk_counts.get("LOW", 0)

    st.markdown("### 📈 Live Security Overview")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("TOTAL SCANS", total)
    m2.metric("HIGH / CRITICAL RISK", high_cnt)
    m3.metric("MEDIUM RISK", med_cnt)
    m4.metric("SAFE / LOW RISK", safe_cnt)

    if total == 0:
        st.info("No threats analyzed yet. Run your first scan to start building your security overview.")

    st.markdown("<br>", unsafe_allow_html=True)

    # Quick Scanner Cards Grid
    st.markdown("### ⚡ Multimodal Security Modules")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div style="background: rgba(15,23,42,0.7); border:1px solid rgba(255,255,255,0.08); padding:22px; border-radius:18px;">
            <div style="font-size:32px;">💬</div>
            <h4 style="color:#f8fafc; margin:8px 0;">Message Scanner</h4>
            <p style="color:#94a3b8; font-size:14px;">Identify SMS, WhatsApp, and email phishing, OTP theft, and financial extortion.</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div style="background: rgba(15,23,42,0.7); border:1px solid rgba(255,255,255,0.08); padding:22px; border-radius:18px;">
            <div style="font-size:32px;">🔗</div>
            <h4 style="color:#f8fafc; margin:8px 0;">URL Scanner</h4>
            <p style="color:#94a3b8; font-size:14px;">Inspect domain risk, shorteners, punycode, brand spoofing, and malicious TLDs.</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div style="background: rgba(15,23,42,0.7); border:1px solid rgba(255,255,255,0.08); padding:22px; border-radius:18px;">
            <div style="font-size:32px;">🖼️</div>
            <h4 style="color:#f8fafc; margin:8px 0;">Screenshot Scanner</h4>
            <p style="color:#94a3b8; font-size:14px;">Extract screenshot text via PyTesseract OCR and detect hidden threats.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c4, c5 = st.columns(2)
    with c4:
        st.markdown("""
        <div style="background: rgba(15,23,42,0.7); border:1px solid rgba(255,255,255,0.08); padding:22px; border-radius:18px;">
            <div style="font-size:32px;">🎙️</div>
            <h4 style="color:#f8fafc; margin:8px 0;">Voice Scanner</h4>
            <p style="color:#94a3b8; font-size:14px;">Transcribe phone conversations with OpenAI Whisper and flag scam tactics.</p>
        </div>
        """, unsafe_allow_html=True)

    with c5:
        st.markdown("""
        <div style="background: rgba(15,23,42,0.7); border:1px solid rgba(255,255,255,0.08); padding:22px; border-radius:18px;">
            <div style="font-size:32px;">📱</div>
            <h4 style="color:#f8fafc; margin:8px 0;">QR Scanner</h4>
            <p style="color:#94a3b8; font-size:14px;">Decode OpenCV QR code payloads and evaluate embedded URL and UPI payment risks.</p>
        </div>
        """, unsafe_allow_html=True)
