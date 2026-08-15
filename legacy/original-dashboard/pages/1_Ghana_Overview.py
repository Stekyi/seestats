import json
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from pathlib import Path

REPORTS_DIR = Path(__file__).parent.parent.parent / "reports"

st.set_page_config(page_title="Ghana Overview", page_icon="📊", layout="wide")
st.title("📊 Ghana Trade Overview")

analysis = st.session_state.get("analysis", {})
report_date = st.session_state.get("report_date", "N/A")
if not analysis:
    st.warning("Please select a report date from the home page.")
    st.stop()

# Load Ghana data from reports
ghana_path = REPORTS_DIR / report_date / "analysis.json"
budget_usd = analysis.get("budget_usd", 6493)
budget_ghc = analysis.get("budget_ghc", 100000)

st.caption(f"Report: {report_date} | Budget: GHC {budget_ghc:,} (~${budget_usd:,.0f} USD)")

# Trade balance summary
import_opps = analysis.get("import_opportunities", [])
export_opps = analysis.get("export_opportunities", [])

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Ghana Total Imports (2023)", "$16.4B", "+6% YoY")
with col2:
    st.metric("Ghana Total Exports (2023)", "$16.9B", "+5% YoY")
with col3:
    st.metric("Trade Balance", "+$481M", "Surplus ✅")

st.markdown("---")

# Top imports chart
import_data = [
    {"Commodity": "Mineral fuels", "Value ($M)": 5242, "Category": "Regulated"},
    {"Commodity": "Machinery", "Value ($M)": 1840, "Category": "Industrial"},
    {"Commodity": "Vehicles", "Value ($M)": 643, "Category": "Consumer"},
    {"Commodity": "Rice", "Value ($M)": 487, "Category": "SME Opportunity"},
    {"Commodity": "Poultry (frozen)", "Value ($M)": 281, "Category": "SME Opportunity"},
    {"Commodity": "Vegetable oils", "Value ($M)": 203, "Category": "SME Opportunity"},
    {"Commodity": "Sugar", "Value ($M)": 182, "Category": "SME Opportunity"},
    {"Commodity": "Tomato paste", "Value ($M)": 147, "Category": "SME Opportunity"},
    {"Commodity": "Pharmaceuticals", "Value ($M)": 312, "Category": "Regulated"},
    {"Commodity": "Wheat flour", "Value ($M)": 124, "Category": "SME Opportunity"},
]
df_imp = pd.DataFrame(import_data).sort_values("Value ($M)", ascending=True)
color_map = {"SME Opportunity": "#2ecc71", "Regulated": "#e74c3c", "Industrial": "#95a5a6", "Consumer": "#3498db"}

col_l, col_r = st.columns(2)
with col_l:
    st.subheader("Top Ghana Imports")
    fig_imp = px.bar(
        df_imp, x="Value ($M)", y="Commodity", orientation="h",
        color="Category", color_discrete_map=color_map,
        title="Top Ghana Imports by Value (2023)",
    )
    fig_imp.update_layout(height=400, legend_title="Category")
    st.plotly_chart(fig_imp, use_container_width=True)

# Top exports chart
export_data = [
    {"Commodity": "Cocoa butter", "Value ($M)": 636, "YoY %": 120},
    {"Commodity": "Cocoa paste", "Value ($M)": 789, "YoY %": 71},
    {"Commodity": "Tuna (canned)", "Value ($M)": 214, "YoY %": 37},
    {"Commodity": "Shea butter/oil", "Value ($M)": 174, "YoY %": 116},
    {"Commodity": "Cashew nuts", "Value ($M)": 298, "YoY %": 10},
    {"Commodity": "Rubber", "Value ($M)": 94, "YoY %": 6},
    {"Commodity": "Dried/smoked fish", "Value ($M)": 62, "YoY %": 18},
    {"Commodity": "Ginger (processed)", "Value ($M)": 45, "YoY %": 25},
    {"Commodity": "Pineapple", "Value ($M)": 38, "YoY %": 12},
    {"Commodity": "Moringa products", "Value ($M)": 8, "YoY %": 45},
]
df_exp = pd.DataFrame(export_data).sort_values("Value ($M)", ascending=True)

with col_r:
    st.subheader("Top Non-Traditional Exports")
    fig_exp = px.bar(
        df_exp, x="Value ($M)", y="Commodity", orientation="h",
        color="YoY %", color_continuous_scale="Greens",
        title="Ghana Non-Traditional Exports (2023)",
    )
    fig_exp.update_coloraxes(colorbar_title="YoY Growth %")
    fig_exp.update_layout(height=400)
    st.plotly_chart(fig_exp, use_container_width=True)

st.markdown("---")

# Trade balance over time
st.subheader("Ghana Trade Balance Trend (2021–2023)")
years = [2021, 2022, 2023]
imports_b = [13.9, 17.2, 16.4]
exports_b = [15.3, 16.1, 16.9]
balance = [e - i for e, i in zip(exports_b, imports_b)]

fig_trend = go.Figure()
fig_trend.add_trace(go.Bar(name="Exports ($B)", x=years, y=exports_b, marker_color="#2ecc71"))
fig_trend.add_trace(go.Bar(name="Imports ($B)", x=years, y=imports_b, marker_color="#e74c3c"))
fig_trend.add_trace(go.Scatter(name="Balance ($B)", x=years, y=balance, mode="lines+markers",
                                line=dict(color="#f39c12", width=3), yaxis="y"))
fig_trend.update_layout(
    barmode="group", height=350,
    yaxis_title="USD Billions",
    title="Ghana Merchandise Trade Balance",
)
st.plotly_chart(fig_trend, use_container_width=True)

st.markdown("---")
st.info("🟢 Green bars = SME-accessible import distribution opportunities | Navigate to **Import Gaps** page for scored analysis")
