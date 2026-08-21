import streamlit as st
from src.database import get_scans, delete_scan, clear_all_scans

def show_history_page():
    st.title("📜 Scan History Log")
    st.write("Browse, filter, and review previous security assessment logs stored in SQLite database.")

    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        search_query = st.text_input("🔍 Search History", placeholder="Search by text, category...")
    with col2:
        scanner_filter = st.selectbox("Scanner Filter", ["All", "message", "url", "screenshot", "voice", "qr"])
    with col3:
        risk_filter = st.selectbox("Risk Filter", ["All", "SAFE", "LOW", "MEDIUM", "HIGH", "CRITICAL"])

    scans = get_scans(limit=100, scanner_type=scanner_filter, risk_level=risk_filter, search_query=search_query)

    if not scans:
        st.info("No threats analyzed yet.\n\nRun your first scan to start building your security overview.")
        return

    st.write(f"Showing **{len(scans)}** recorded scan logs:")

    selected_scans_for_compare = []

    for item in scans:
        scan_id = item["scan_id"]
        ts = item["timestamp"]
        stype = item["scanner_type"].title()
        score = item["risk_score"]
        level = item["risk_level"]
        cat = item["category"]
        summary = item["short_summary"] or "Scan evaluation log"

        with st.expander(f"[{ts}] {stype} Scanner — {level} RISK ({score}/100) — {cat}"):
            col_a, col_b = st.columns([4, 1])
            with col_a:
                st.write(f"**Scan ID:** `{scan_id}`")
                st.write(f"**Summary:** {summary}")
                st.json(item["full_json"])
            with col_b:
                if st.button("🗑️ Delete", key=f"del_{scan_id}"):
                    delete_scan(scan_id)
                    st.success("Deleted!")
                    st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚨 Clear Entire Scan History", type="secondary"):
        clear_all_scans()
        st.success("All scan records cleared!")
        st.rerun()
