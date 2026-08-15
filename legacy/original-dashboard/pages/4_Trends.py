import json
import sys
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import ensure_analysis, REPORTS_DIR

st.set_page_config(page_title="Trends", page_icon="📈", layout="wide")
st.title("📈 Trend Analysis")
ensure_analysis()
st.caption("Week-over-week tracking of opportunities, prices, and scores")


def load_all_reports() -> list:
    reports = []
    if not REPORTS_DIR.exists():
        return reports
    for folder in sorted(REPORTS_DIR.iterdir()):
        if not folder.is_dir():
            continue
        analysis_path = folder / "analysis.json"
        if analysis_path.exists():
            try:
                with open(analysis_path, encoding="utf-8") as f:
                    data = json.load(f)
                    data["_report_date"] = folder.name
                    reports.append(data)
            except Exception:
                continue
    return reports


all_reports = load_all_reports()

if len(all_reports) < 1:
    st.warning("No reports found. Run the pipeline first to generate data.")
    st.stop()

if len(all_reports) == 1:
    st.info("Only one report available. Trend charts will show once weekly runs accumulate.")

# Extract time series for each commodity's score
dates = [r["_report_date"] for r in all_reports]

# Build score trends per commodity
import_trend = {}
export_trend = {}
for report in all_reports:
    d = report["_report_date"]
    for opp in report.get("import_opportunities", []):
        comm = opp["commodity"]
        if comm not in import_trend:
            import_trend[comm] = {"dates": [], "scores": [], "margins": [], "growth": []}
        import_trend[comm]["dates"].append(d)
        import_trend[comm]["scores"].append(opp["score"])
        import_trend[comm]["margins"].append(opp["margin_pct"])
        import_trend[comm]["growth"].append(opp["yoy_growth_pct"])
    for opp in report.get("export_opportunities", []):
        comm = opp["commodity"]
        if comm not in export_trend:
            export_trend[comm] = {"dates": [], "scores": [], "margins": [], "growth": []}
        export_trend[comm]["dates"].append(d)
        export_trend[comm]["scores"].append(opp["score"])
        export_trend[comm]["margins"].append(opp["margin_pct"])
        export_trend[comm]["growth"].append(opp["yoy_growth_pct"])

# Score trend chart
st.subheader("🏆 Opportunity Score Trends (All Weeks)")

tab1, tab2 = st.tabs(["Import Opportunities", "Export Opportunities"])

with tab1:
    if import_trend:
        fig_imp_trend = go.Figure()
        for comm, data in import_trend.items():
            fig_imp_trend.add_trace(go.Scatter(
                x=data["dates"], y=data["scores"], mode="lines+markers",
                name=comm, line=dict(width=2),
            ))
        fig_imp_trend.add_hline(y=70, line_dash="dash", line_color="green", annotation_text="Strong (70)")
        fig_imp_trend.add_hline(y=50, line_dash="dash", line_color="orange", annotation_text="Moderate (50)")
        fig_imp_trend.update_layout(
            height=400, yaxis_title="Score /100", xaxis_title="Report Week",
            title="Import Opportunity Scores Over Time",
        )
        st.plotly_chart(fig_imp_trend, use_container_width=True)
    else:
        st.info("No import trend data yet.")

with tab2:
    if export_trend:
        fig_exp_trend = go.Figure()
        for comm, data in export_trend.items():
            fig_exp_trend.add_trace(go.Scatter(
                x=data["dates"], y=data["scores"], mode="lines+markers",
                name=comm, line=dict(width=2),
            ))
        fig_exp_trend.add_hline(y=70, line_dash="dash", line_color="green", annotation_text="Strong (70)")
        fig_exp_trend.add_hline(y=50, line_dash="dash", line_color="orange", annotation_text="Moderate (50)")
        fig_exp_trend.update_layout(
            height=400, yaxis_title="Score /100", xaxis_title="Report Week",
            title="Export Opportunity Scores Over Time",
        )
        st.plotly_chart(fig_exp_trend, use_container_width=True)
    else:
        st.info("No export trend data yet.")

st.markdown("---")

# Price trend charts from embedded data
st.subheader("💵 Commodity Price Trends (Historical)")

PRICE_DATA = {
    "Ginger (Ghana, $/MT)":        [580, 640, 710, 780, 820],
    "Shea butter (Ghana, $/MT)":   [450, 520, 610, 690, 750],
    "Cashew nuts (Ghana, $/MT)":   [850, 920, 980, 1050, 1100],
    "Moringa powder (Ghana, $/MT)":[1400, 1700, 1900, 2050, 2200],
    "Rice (import price, $/MT)":   [390, 400, 430, 490, 620],
    "Tomato paste (import, $/MT)": [580, 600, 630, 680, 651],
    "Poultry (import, $/MT)":      [1400, 1500, 1620, 1750, 1811],
}
years = [2019, 2020, 2021, 2022, 2023]

selected_comms = st.multiselect(
    "Select commodities to compare:",
    list(PRICE_DATA.keys()),
    default=list(PRICE_DATA.keys())[:4],
)

if selected_comms:
    fig_price = go.Figure()
    for comm in selected_comms:
        fig_price.add_trace(go.Scatter(
            x=years, y=PRICE_DATA[comm], mode="lines+markers", name=comm,
        ))
    fig_price.update_layout(
        height=400, yaxis_title="Price (USD/MT)", xaxis_title="Year",
        title="Historical Commodity Prices (2019–2023)",
    )
    st.plotly_chart(fig_price, use_container_width=True)

st.markdown("---")

# Summary table across all weeks
st.subheader("📋 Weekly Report Summary")
summary_rows = []
for report in all_reports:
    summ = report.get("summary", {})
    top_opp = report.get("top_5_overall", [{}])[0]
    summary_rows.append({
        "Week": report["_report_date"],
        "Import Opps": summ.get("total_import_opps", 0),
        "Export Opps": summ.get("total_export_opps", 0),
        "Green Margin Opps": summ.get("green_margin_opps", 0),
        "Budget-Fit Opps": summ.get("budget_fit_opps", 0),
        "Top Opportunity": top_opp.get("commodity", "N/A"),
        "Top Score": top_opp.get("score", 0),
    })

if summary_rows:
    st.dataframe(pd.DataFrame(summary_rows), use_container_width=True, hide_index=True)

st.markdown("---")
st.caption("Trends update every week when the pipeline runs (Monday 8am). Prices are sourced from FAOSTAT and World Bank.")
