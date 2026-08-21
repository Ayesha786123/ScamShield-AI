import streamlit as st
from PIL import Image
from src.qr_scanner import scan_qr_image
from pages.result_ui import render_pipeline_animation, render_unified_result_ui

def show_qr_scanner_page():
    st.title("📱 QR Code Scanner")
    st.write("Upload a QR code image to decode payload data and analyze payment or phishing risks.")

    uploaded_file = st.file_uploader(
        "Upload QR Code Image",
        type=["png", "jpg", "jpeg", "webp"]
    )

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded QR Code", width=250)

        if st.button("🔍 Decode & Analyze QR", type="primary", use_container_width=True):
            with st.spinner("Decoding QR code using OpenCV QRCodeDetector..."):
                render_pipeline_animation()
                result = scan_qr_image(uploaded_file)

                # Show Decoded payload expander
                payload = result.get("payload", "")
                payload_type = result.get("payload_type", "Unknown")
                if payload:
                    with st.expander(f"📱 Decoded QR Payload ({payload_type})"):
                        st.code(payload)

                render_unified_result_ui(result, scanner_name="QR Code", raw_input=f"[QR Image: {uploaded_file.name}]")
