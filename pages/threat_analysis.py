import streamlit as st
from src.scam_categories import CATEGORY_DESCRIPTIONS

def show_threat_analysis_page():
    st.title("🧬 Threat Analysis & Scam DNA")
    st.write("Explore ScamShield AI's threat taxonomy, social engineering vectors, and attack chain blueprints.")

    st.markdown("### 📚 Scam Taxonomy & Vector Catalog")
    for category, desc in CATEGORY_DESCRIPTIONS.items():
        with st.expander(f"📌 {category}"):
            st.write(desc)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🛡️ Social Engineering Indicators")

    c1, c2 = st.columns(2)
    with c1:
        st.info("🚨 **Fear & Coercion Tactics**\n\nThreats of account suspension, arrest, legal action, or law enforcement impersonation designed to induce panic.")
        st.info("💰 **Advance Fee & Greed Baits**\n\nFake lottery winnings, job offers, or cashback rewards that demand an upfront registration or processing fee.")
    with c2:
        st.info("⚡ **Manufactured Urgency**\n\nStrict deadlines ('act now', 'within 24 hours') enforcing compliance before victims can verify information.")
        st.info("🔑 **Credential & OTP Harvesting**\n\nDeceptive requests for 2FA OTP codes, passwords, PINs, or card CVVs under the guise of security verification.")
