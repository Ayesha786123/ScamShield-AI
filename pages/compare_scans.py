import streamlit as st
from src.database import get_scans

def show_compare_scans_page():
    st.title("⚖️ Compare Scans")
    st.write("Compare two recent scan results side-by-side to analyze threat evolution.")

    scans = get_scans(limit=50)

    if len(scans) < 2:
        st.info("At least 2 saved scan records are required to compare results. Run more scans to enable comparison.")
        return

    options = {f"[{s['timestamp']}] {s['scanner_type'].title()} - {s['risk_level']} ({s['category']}) - ID: {s['scan_id']}": s for s in scans}
    labels = list(options.keys())

    c1, c2 = st.columns(2)
    with c1:
        scan_a_label = st.selectbox("Select Scan A", labels, index=0)
    with c2:
        scan_b_label = st.selectbox("Select Scan B", labels, index=min(1, len(labels)-1))

    scan_a = options[scan_a_label]
    scan_b = options[scan_b_label]

    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown(f"### 🔵 Scan A ({scan_a['scanner_type'].title()})")
        st.metric("Risk Score", f"{scan_a['risk_score']}/100", delta=scan_a['risk_level'])
        st.write(f"**Category:** {scan_a['category']}")
        st.write(f"**Timestamp:** {scan_a['timestamp']}")
        st.json(scan_a['full_json'])

    with col_b:
        st.markdown(f"### 🟣 Scan B ({scan_b['scanner_type'].title()})")
        st.metric("Risk Score", f"{scan_b['risk_score']}/100", delta=scan_b['risk_level'])
        st.write(f"**Category:** {scan_b['category']}")
        st.write(f"**Timestamp:** {scan_b['timestamp']}")
        st.json(scan_b['full_json'])
