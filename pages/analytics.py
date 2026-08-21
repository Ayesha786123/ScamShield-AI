import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from src.database import get_scans, get_analytics_summary


def show_analytics_page():
    st.title("📊 Security Analytics Dashboard")
    st.write("Visualize threat patterns, category distributions, and scan activity from the SQLite scan database.")

    analytics = get_analytics_summary()
    total = analytics["total"]

    if total == 0:
        st.info("No threats analyzed yet.\n\nRun your first scan to start building your security overview.")
        return

    risk_counts = analytics["risk_counts"]
    category_counts = analytics["category_counts"]
    scanner_counts = analytics["scanner_counts"]

    # KPI Row
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Total Scans", total)
    m2.metric("CRITICAL", risk_counts.get("CRITICAL", 0))
    m3.metric("HIGH", risk_counts.get("HIGH", 0))
    m4.metric("MEDIUM", risk_counts.get("MEDIUM", 0))
    m5.metric("SAFE / LOW", risk_counts.get("SAFE", 0) + risk_counts.get("LOW", 0))

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # Risk Distribution Pie
    with col1:
        if risk_counts:
            fig_risk = px.pie(
                values=list(risk_counts.values()),
                names=list(risk_counts.keys()),
                title="Risk Level Distribution",
                color_discrete_map={
                    "SAFE": "#10b981",
                    "LOW": "#3b82f6",
                    "MEDIUM": "#f59e0b",
                    "HIGH": "#ef4444",
                    "CRITICAL": "#dc2626"
                },
                template="plotly_dark"
            )
            fig_risk.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#f8fafc"
            )
            st.plotly_chart(fig_risk, use_container_width=True)

    # Category Distribution Bar
    with col2:
        if category_counts:
            cats = list(category_counts.keys())
            vals = list(category_counts.values())
            fig_cat = px.bar(
                x=vals,
                y=[c[:30] for c in cats],
                orientation="h",
                title="Scam Category Distribution",
                template="plotly_dark",
                color=vals,
                color_continuous_scale="reds"
            )
            fig_cat.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#f8fafc",
                showlegend=False
            )
            st.plotly_chart(fig_cat, use_container_width=True)

    # Scanner Usage
    if scanner_counts:
        fig_scanner = px.bar(
            x=list(scanner_counts.keys()),
            y=list(scanner_counts.values()),
            title="Scanner Module Usage",
            template="plotly_dark",
            color=list(scanner_counts.values()),
            color_continuous_scale="blues"
        )
        fig_scanner.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#f8fafc",
            showlegend=False
        )
        st.plotly_chart(fig_scanner, use_container_width=True)

    # Timeline trend
    scans = get_scans(limit=200)
    if scans:
        df = pd.DataFrame(scans)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df["date"] = df["timestamp"].dt.date
        daily = df.groupby("date").size().reset_index(name="scans")
        fig_trend = px.line(
            daily, x="date", y="scans",
            title="Scan Activity Timeline",
            template="plotly_dark"
        )
        fig_trend.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#f8fafc"
        )
        st.plotly_chart(fig_trend, use_container_width=True)
