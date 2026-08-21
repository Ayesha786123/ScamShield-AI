import streamlit as st
from src.predict import predict_message
from pages.result_ui import render_pipeline_animation, render_unified_result_ui

def show_message_scanner_page():
    st.title("💬 Message Scanner")
    st.write("Paste an SMS, WhatsApp message, email, or suspicious text to analyze scam risk.")

    demo_text = st.session_state.pop("demo_message_input", "")

    message_input = st.text_area(
        "Suspicious Message Text",
        value=demo_text,
        height=160,
        placeholder="Example: Your SBI bank account will be blocked today. Verify your account immediately at https://example.com"
    )

    if st.button("🔍 Analyze Message", type="primary", use_container_width=True):
        if not message_input.strip():
            st.warning("Please enter a message to analyze.")
        else:
            with st.spinner("Scanning message with ScamShield AI Risk Engine..."):
                render_pipeline_animation()
                result = predict_message(message_input)
                render_unified_result_ui(result, scanner_name="Message", raw_input=message_input)
