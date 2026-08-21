import streamlit as st
from PIL import Image
from src.screenshot_scanner import analyze_screenshot
from pages.result_ui import render_pipeline_animation, render_unified_result_ui

def show_screenshot_scanner_page():
    st.title("🖼️ Screenshot Scanner")
    st.write("Upload a screenshot containing suspicious messages, payment requests, or text.")

    uploaded_file = st.file_uploader(
        "Upload Screenshot Image",
        type=["png", "jpg", "jpeg", "webp"]
    )

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Screenshot Preview", use_container_width=True)

        if st.button("🔍 Analyze Screenshot", type="primary", use_container_width=True):
            with st.spinner("Extracting OCR text and scanning image content..."):
                render_pipeline_animation()
                result = analyze_screenshot(uploaded_file)

                # Show OCR Extracted text expander
                extracted_text = result.get("text", "")
                if extracted_text:
                    with st.expander("📝 View Extracted Text (OCR)"):
                        st.code(extracted_text)

                render_unified_result_ui(result, scanner_name="Screenshot", raw_input=f"[Screenshot Image: {uploaded_file.name}]")
