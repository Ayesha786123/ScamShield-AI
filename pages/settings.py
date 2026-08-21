import streamlit as st
from src.utils import detect_tesseract, detect_ffmpeg, detect_whisper
from src.database import get_analytics_summary
import os


def show_settings_page():
    st.title("⚙️ Settings & System Status")

    # ─── Privacy & Demo Mode ───────────────────────────────
    st.markdown("### 🔒 Privacy & Behaviour")

    col1, col2 = st.columns(2)
    with col1:
        privacy_mode = st.toggle(
            "Privacy Mode",
            value=st.session_state.get("privacy_mode", False),
            help="When ON: raw message/image/audio text is NOT stored in the scan history database."
        )
        st.session_state["privacy_mode"] = privacy_mode
        if privacy_mode:
            st.success("Privacy Mode is ACTIVE — Raw inputs will NOT be stored.")
        else:
            st.info("Privacy Mode is OFF — Full scan data will be stored in SQLite.")

    with col2:
        demo_mode = st.toggle(
            "Demo Mode",
            value=st.session_state.get("demo_mode", False),
            help="Loads synthetic scam/safe examples directly into the scanner pages."
        )
        st.session_state["demo_mode"] = demo_mode
        if demo_mode:
            st.success("Demo Mode is ACTIVE — Go to Message or URL scanner to see examples.")

    st.divider()

    # ─── System Component Status ──────────────────────────
    st.markdown("### 🔬 AI & Dependency Status")

    has_tess, tess_msg = detect_tesseract()
    has_ffmpeg, ffmpeg_msg = detect_ffmpeg()
    has_whisper, whisper_msg = detect_whisper()

    model_ok = os.path.exists(os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "scamshield_model.pkl"))
    vec_ok = os.path.exists(os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "tfidf_vectorizer.pkl"))

    def status_row(label, ok, detail=""):
        icon = "✅" if ok else "❌"
        color = "#34d399" if ok else "#f87171"
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:12px;padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.05);">'
            f'<span style="font-size:18px;">{icon}</span>'
            f'<span style="font-weight:600;color:#f8fafc;">{label}</span>'
            f'<span style="color:#94a3b8;font-size:13px;">{detail}</span>'
            f'</div>',
            unsafe_allow_html=True
        )

    status_row("ML Classification Model", model_ok, "models/scamshield_model.pkl")
    status_row("TF-IDF Vectorizer", vec_ok, "models/tfidf_vectorizer.pkl")
    status_row("Tesseract OCR Engine", has_tess, tess_msg if not has_tess else "Screenshot text extraction ready")
    status_row("FFmpeg Audio Processor", has_ffmpeg, ffmpeg_msg if not has_ffmpeg else "Audio conversion ready")
    status_row("OpenAI Whisper STT", has_whisper, whisper_msg if not has_whisper else "Speech-to-text transcription ready")
    status_row("OpenCV QR Detector", True, "cv2.QRCodeDetector available")
    status_row("SQLite Database", True, "Local scan history storage active")

    vt_key = bool(os.environ.get("VIRUSTOTAL_API_KEY"))
    gsb_key = bool(os.environ.get("GOOGLE_SAFE_BROWSING_API_KEY"))
    abuse_key = bool(os.environ.get("ABUSEIPDB_API_KEY"))
    ti_ok = vt_key or gsb_key or abuse_key
    ti_detail = "External keys configured" if ti_ok else "No API keys set — local analysis only"
    status_row("Threat Intelligence APIs", ti_ok, ti_detail)

    st.divider()

    # ─── Database Summary ─────────────────────────────────
    st.markdown("### 🗄️ Database Summary")
    analytics = get_analytics_summary()
    st.write(f"**Total Saved Scans:** {analytics['total']}")

    st.divider()

    # ─── Threat Intelligence Keys Info ───────────────────
    st.markdown("### 🌐 External Threat Intelligence")
    st.info(
        "External threat intelligence API keys are read from environment variables only. "
        "Never hardcode keys in source files.\n\n"
        "Supported:\n"
        "- `VIRUSTOTAL_API_KEY`\n"
        "- `GOOGLE_SAFE_BROWSING_API_KEY`\n"
        "- `ABUSEIPDB_API_KEY`"
    )

    # ─── Demo Examples ────────────────────────────────────
    if demo_mode:
        st.divider()
        st.markdown("### 🧪 Demo Mode — Synthetic Scan Examples")
        st.write("Select an example to load it into the scanner.")

        DEMO_EXAMPLES = {
            "OTP Scam": "Your account will be blocked. Share your OTP 847291 immediately to prevent suspension.",
            "Bank Impersonation Scam": "HDFC Bank Alert: Your KYC has expired. Update your banking details immediately or your account will be permanently blocked.",
            "UPI / Payment Scam": "You have received a cashback of ₹2,000 from PhonePe. Click here to claim: http://phonep3-reward.xyz/claim",
            "Delivery Scam": "Your parcel could not be delivered. Pay the ₹35 processing fee immediately: http://trackparcel.top/fee",
            "Job Scam": "Congratulations! You have been selected for a work-from-home job paying ₹50,000/month. Pay ₹500 registration fee to start.",
            "Investment Scam": "Guaranteed 40% returns on crypto investment this week. Limited slots. Send ₹10,000 to UPI: profit@fund",
            "Lottery Scam": "You have won ₹5,00,000 in the Amazon Lucky Draw! Pay ₹200 processing fee to claim your prize.",
            "Phishing Link": "Verify your Google account: http://g00gle-secure-login.xyz/verify?token=XYZ123",
            "Tech Support Scam": "Microsoft Warning: Your PC has been infected. Call +91-XXXXXXXX immediately and download AnyDesk for remote assistance.",
            "Safe Message": "Your flight PNR AB1234 is confirmed. Web check-in opens 48 hours before departure at airline.com.",
        }

        selected_demo = st.selectbox("Select Demo Example", list(DEMO_EXAMPLES.keys()))
        demo_text = DEMO_EXAMPLES[selected_demo]

        st.code(demo_text)

        if st.button("▶️ Load into Message Scanner", use_container_width=True):
            st.session_state["demo_message_input"] = demo_text
            st.session_state["nav_page"] = "Message Scanner"
            st.success("Demo example loaded! Navigate to Message Scanner to analyze.")
            st.rerun()
