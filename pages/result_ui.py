import streamlit as st
import time
from src.database import save_scan
from src.report_generator import generate_markdown_report

def render_pipeline_animation():
    """
    Animated live scan pipeline execution indicator.
    """
    pipeline_html = """
    <div style="
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 12px 20px;
        margin: 15px 0 25px 0;
        font-size: 13px;
        font-weight: 600;
        color: #94a3b8;
    ">
        <div style="color:#38bdf8;">INPUT</div>
        <div>→</div>
        <div style="color:#38bdf8;">EXTRACTION</div>
        <div>→</div>
        <div style="color:#818cf8;">DETECTION</div>
        <div>→</div>
        <div style="color:#a855f7;">THREAT ANALYSIS</div>
        <div>→</div>
        <div style="color:#ec4899;">RISK ENGINE</div>
        <div>→</div>
        <div style="color:#f43f5e;">RESULT</div>
    </div>
    """
    st.markdown(pipeline_html, unsafe_allow_html=True)


def render_unified_result_ui(result_dict, scanner_name="Message", raw_input=""):
    """
    Renders the consistent V2 result screen.
    """
    score = result_dict.get("risk_score", 0)
    level = result_dict.get("risk_level", "SAFE")
    confidence = result_dict.get("confidence", 85)
    category = result_dict.get("category", "General")
    explanation = result_dict.get("explanation", "")
    indicators = result_dict.get("indicators", [])
    recommendation = result_dict.get("recommendation", "")
    scam_dna = result_dict.get("scam_dna", {})
    attack_chain = result_dict.get("attack_chain", [])

    # Color badge
    badge_colors = {
        "SAFE": "background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4);",
        "LOW": "background: rgba(59, 130, 246, 0.2); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.4);",
        "MEDIUM": "background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.4);",
        "HIGH": "background: rgba(239, 68, 68, 0.2); color: #fca5a5; border: 1px solid rgba(239, 68, 68, 0.4);",
        "CRITICAL": "background: rgba(220, 38, 38, 0.3); color: #f87171; border: 1px solid rgba(220, 38, 38, 0.6); box-shadow: 0 0 15px rgba(220,38,38,0.3);"
    }
    badge_style = badge_colors.get(level, badge_colors["SAFE"])

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("🔍 Scan Assessment Result")

    col1, col2, col3 = st.columns([1.5, 1, 1])

    with col1:
        st.markdown(f"""
        <div style="
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 20px;
            text-align: center;
        ">
            <div style="font-size: 13px; text-transform: uppercase; color: #94a3b8; letter-spacing: 1px;">Risk Score</div>
            <div style="font-size: 48px; font-weight: 800; color: #f8fafc; margin: 5px 0;">{score}<span style="font-size: 20px; color: #64748b;">/100</span></div>
            <div style="display: inline-block; padding: 4px 14px; border-radius: 20px; font-weight: 700; font-size: 13px; {badge_style}">
                {level} RISK
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 20px;
            text-align: center;
            height: 100%;
        ">
            <div style="font-size: 13px; text-transform: uppercase; color: #94a3b8; letter-spacing: 1px;">Category</div>
            <div style="font-size: 16px; font-weight: 700; color: #38bdf8; margin-top: 15px;">{category}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div style="
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 20px;
            text-align: center;
            height: 100%;
        ">
            <div style="font-size: 13px; text-transform: uppercase; color: #94a3b8; letter-spacing: 1px;">Confidence</div>
            <div style="font-size: 32px; font-weight: 800; color: #f8fafc; margin-top: 5px;">{confidence}%</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Explanation & Indicators
    st.markdown("#### 🧠 Why ScamShield Flagged This")
    st.info(explanation)

    if indicators:
        st.markdown("##### ⚠️ Detected Risk Indicators")
        for ind in indicators:
            st.warning(f"• {ind}")

    st.markdown("<br>", unsafe_allow_html=True)

    # Scam DNA & Attack Chain Tabs
    tab1, tab2 = st.tabs(["🧬 Scam DNA Profile", "🔗 Dynamic Attack Chain"])

    with tab1:
        st.markdown("##### Scam DNA Attributes")
        c1, c2 = st.columns(2)
        if isinstance(scam_dna, dict):
            keys = list(scam_dna.keys())
            half = len(keys) // 2 + 1
            with c1:
                for k in keys[:half]:
                    st.write(f"**{k.replace('_', ' ').title()}:** {scam_dna[k]}")
            with c2:
                for k in keys[half:]:
                    st.write(f"**{k.replace('_', ' ').title()}:** {scam_dna[k]}")

    with tab2:
        st.markdown("##### Step-by-Step Adversary Progression")
        if isinstance(attack_chain, list):
            for step in attack_chain:
                step_num = step.get("step", 1)
                title = step.get("title", "Phase")
                desc = step.get("desc", "")
                st.markdown(f"**Step {step_num}: {title}**")
                st.caption(desc)

    st.markdown("<br>", unsafe_allow_html=True)

    # Safety Copilot Recommendations
    st.markdown("#### 🛡️ What Should I Do?")
    rec_list = recommendation.split("; ")
    for r in rec_list:
        if r.strip():
            st.write(f"• {r.strip()}")

    st.markdown("<br>", unsafe_allow_html=True)

    # Action Buttons
    bcol1, bcol2, bcol3 = st.columns(3)

    with bcol1:
        md_report = generate_markdown_report(result_dict, scanner_name)
        st.download_button(
            "📄 Generate & Download Report",
            data=md_report,
            file_name=f"scamshield_report_{scanner_name.lower()}.md",
            mime="text/markdown",
            use_container_width=True
        )

    with bcol2:
        if st.button("💾 Save Scan to History", use_container_width=True):
            privacy_mode = st.session_state.get("privacy_mode", False)
            scan_id = save_scan(scanner_name.lower(), result_dict, raw_input=raw_input, privacy_mode=privacy_mode)
            st.success(f"Scan saved to SQLite database (ID: {scan_id})!")

    with bcol3:
        if st.button("🔄 Scan Another", use_container_width=True):
            st.rerun()
