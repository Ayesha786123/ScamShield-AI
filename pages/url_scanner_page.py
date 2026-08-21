import streamlit as st
from src.url_scanner import analyze_url
from pages.result_ui import render_pipeline_animation, render_unified_result_ui

def show_url_scanner_page():
    st.title("🔗 URL Scanner")
    st.write("Analyze suspicious links, shorteners, punycode domains, and brand spoofing.")

    demo_url = st.session_state.pop("demo_url_input", "")

    url_input = st.text_input(
        "Enter URL to Scan",
        value=demo_url,
        placeholder="https://verify-sbi-account-update.xyz/login"
    )

    if st.button("🔍 Scan URL", type="primary", use_container_width=True):
        if not url_input.strip():
            st.warning("Please enter a URL.")
        else:
            with st.spinner("Analyzing domain heuristics and threat vectors..."):
                render_pipeline_animation()
                result = analyze_url(url_input)
                render_unified_result_ui(result, scanner_name="URL", raw_input=url_input)
