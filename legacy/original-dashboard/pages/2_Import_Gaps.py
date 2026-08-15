import sys
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import page_header

st.set_page_config(page_title="Import Gaps", page_icon="📥", layout="wide")
analysis = page_header("📥 Import Gap Analysis", "Distribution opportunities for your GHC 100,000 budget")

import_opps = analysis.get("import_opportunities", [])
budget_ghc = analysis.get("budget_ghc", 100_000)
usd_ghc = 15.4

if not import_opps:
    st.warning("No import opportunities found in this report.")
    st.stop()

# Score summary table
st.subheader("📊 Ranked Import Opportunities")

df_data = []
for opp in import_opps:
    df_data.append({
        "Commodity": opp["commodity"],
        "Score": opp["score"],
        "Import Value ($M)": opp["ghana_import_usd_m"],
        "YoY Growth %": opp["yoy_growth_pct"],
        "Best Supplier": opp["best_supplier"],
        "Best Price ($/MT)": opp["best_price_usd_mt"],
        "Margin %": opp["margin_pct"],
        "Margin Flag": opp["margin_flag"],
        "Budget Fit": "✅" if opp["budget_fit"] else "⚠️",
        "Est. Order (MT)": opp["est_order_qty_mt"],
    })

df = pd.DataFrame(df_data)

# Colour rows by score
def colour_score(val):
    if val >= 70:
        return "background-color: #d4edda"
    elif val >= 50:
        return "background-color: #fff3cd"
    return "background-color: #f8d7da"

styled = df[["Commodity", "Score", "Import Value ($M)", "YoY Growth %", "Best Supplier",
             "Best Price ($/MT)", "Margin %", "Budget Fit", "Est. Order (MT)"]].style.map(
    colour_score, subset=["Score"]
)
st.dataframe(styled, use_container_width=True, hide_index=True)

st.markdown("---")

# Bubble chart: growth vs gap size
st.subheader("🫧 Opportunity Map — Gap Size vs Growth")
fig_bubble = px.scatter(
    df, x="YoY Growth %", y="Import Value ($M)",
    size="Margin %", color="Score",
    color_continuous_scale="RdYlGn",
    text="Commodity",
    title="Import Gaps: Growth Rate vs Market Size (bubble = margin %)",
    labels={"YoY Growth %": "YoY Growth (%)", "Import Value ($M)": "Ghana Import Value ($M)"},
)
fig_bubble.update_traces(textposition="top center")
fig_bubble.update_layout(height=450, coloraxis_colorbar_title="Score")
st.plotly_chart(fig_bubble, use_container_width=True)

st.markdown("---")

# Detailed view per commodity
st.subheader("🔍 Commodity Deep Dive")
selected = st.selectbox("Select commodity:", [o["commodity"] for o in import_opps])
opp = next(o for o in import_opps if o["commodity"] == selected)

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Opportunity Score", f"{opp['score']}/100")
    st.metric("Ghana Imports/yr", f"${opp['ghana_import_usd_m']}M")
with c2:
    score_label = "green" if opp["score"] >= 70 else ("yellow" if opp["score"] >= 50 else "red")
    st.metric("YoY Growth", f"+{opp['yoy_growth_pct']}%")
    st.metric("Gross Margin", f"{opp['margin_pct']}%")
with c3:
    st.metric("Est. Order Size", f"GHC {opp['est_order_ghc']:,}")
    st.metric("Est. Order Qty", f"{opp['est_order_qty_mt']} MT")

# Score breakdown radar
breakdown = opp.get("score_breakdown", {})
if breakdown:
    categories = list(breakdown.keys())
    values = list(breakdown.values())
    max_vals = {"gap_size": 30, "growth": 25, "margin": 25, "logistics": 10, "budget_fit": 10}
    pct_values = [round(v / max_vals.get(k, 10) * 100) for k, v in breakdown.items()]

    fig_radar = go.Figure(go.Scatterpolar(
        r=pct_values + [pct_values[0]],
        theta=categories + [categories[0]],
        fill="toself", fillcolor="rgba(46, 204, 113, 0.3)",
        line_color="#2ecc71",
    ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        title=f"Score Breakdown: {selected}",
        height=350,
    )
    st.plotly_chart(fig_radar, use_container_width=True)

# Suppliers table
suppliers = opp.get("all_suppliers", [])
if suppliers:
    st.subheader(f"🌍 Supply Sources for {selected}")
    sup_df = pd.DataFrame(suppliers)
    order_usd = 60_000 / usd_ghc
    sup_df["Est. Qty (MT) @ GHC 60k"] = (order_usd / sup_df["price_usd_mt"]).round(1)
    sup_df.columns = ["Country", "Price ($/MT)", "Distance", "Est. Order Qty (MT)"]
    st.dataframe(sup_df, use_container_width=True, hide_index=True)

# Budget calculator
st.subheader("💰 Budget Calculator")
budget_input = st.slider("Your available budget (GHC)", 20_000, 100_000, 60_000, step=5_000)
best_price = opp["best_price_usd_mt"]
if best_price > 0:
    order_usd = budget_input / usd_ghc
    qty_mt = order_usd / best_price
    # Estimate retail value (using margin)
    margin = opp["margin_pct"] / 100
    retail_ghc = budget_input * (1 + margin)
    profit_ghc = retail_ghc - budget_input
    st.success(
        f"GHC {budget_input:,} → buys **{qty_mt:.1f} MT** from {opp['best_supplier']} "
        f"→ estimated retail value **GHC {retail_ghc:,.0f}** → profit **GHC {profit_ghc:,.0f}**"
    )
    if margin < 0.20:
        st.error("⚠️ Margin below 20% — not recommended per Weiss framework")

st.markdown("---")
st.caption("Weiss Rule: Confirm a buyer before placing the order. Never stock inventory without a purchase commitment.")
