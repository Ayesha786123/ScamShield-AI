import streamlit as st
from src.database import get_scans
from src.report_generator import generate_markdown_report
import json


def show_reports_page():
    st.title("📋 Security Reports")
    st.write("Generate and download detailed Markdown security reports from your scan history.")

    scans = get_scans(limit=50)

    if not scans:
        st.info("No scan history available yet.\n\nRun scans to generate security reports.")
        return

    options = {
        f"[{s['timestamp']}] {s['scanner_type'].title()} — {s['risk_level']} — {s['category']}": s
        for s in scans
    }
    selected_label = st.selectbox("Select Scan to Generate Report For", list(options.keys()))
    selected_scan = options[selected_label]

    st.write(f"**Scan ID:** `{selected_scan['scan_id']}`")
    st.write(f"**Risk Score:** {selected_scan['risk_score']}/100 ({selected_scan['risk_level']})")
    st.write(f"**Category:** {selected_scan['category']}")

    if st.button("📄 Generate Markdown Report", type="primary", use_container_width=True):
        try:
            result_data = selected_scan["full_json"]
            if isinstance(result_data, str):
                result_data = json.loads(result_data)

            scanner_name = selected_scan["scanner_type"].title()
            report_md = generate_markdown_report(result_data, scanner_type=scanner_name)

            st.download_button(
                "⬇️ Download Report (.md)",
                data=report_md,
                file_name=f"scamshield_{selected_scan['scan_id']}_report.md",
                mime="text/markdown",
                use_container_width=True
            )

            with st.expander("📄 Preview Report"):
                st.markdown(report_md)

        except Exception as e:
            st.error(f"Report generation error: {e}")
