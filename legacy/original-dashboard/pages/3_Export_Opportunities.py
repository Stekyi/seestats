import sys
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import networkx as nx
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import page_header

st.set_page_config(page_title="Export Opportunities", page_icon="📤", layout="wide")
analysis = page_header("📤 Export Opportunity Analysis", "Source locally in Ghana, sell globally")

export_opps = analysis.get("export_opportunities", [])
budget_ghc = analysis.get("budget_ghc", 100_000)
usd_ghc = 15.4

if not export_opps:
    st.warning("No export opportunities found in this report.")
    st.stop()

# Ranked table
st.subheader("📊 Ranked Export Opportunities")
df_data = []
for opp in export_opps:
    df_data.append({
        "Commodity": opp["commodity"],
        "Score": opp["score"],
        "Ghana Export $M": opp["ghana_export_usd_m"],
        "YoY Growth %": opp["yoy_growth_pct"],
        "Best Market": opp["best_market"],
        "Market Demand Growth %": opp["market_demand_growth_pct"],
        "Price Premium": opp["price_premium"],
        "Ghana Price $/MT": opp["ghana_producer_price_usd_mt"],
        "Margin %": opp["margin_pct"],
        "Budget Fit": "✅" if opp["budget_fit"] else "⚠️",
    })

df = pd.DataFrame(df_data)

def colour_score(val):
    if val >= 70:
        return "background-color: #d4edda"
    elif val >= 50:
        return "background-color: #fff3cd"
    return "background-color: #f8d7da"

styled = df.style.map(colour_score, subset=["Score"])
st.dataframe(styled, use_container_width=True, hide_index=True)

st.markdown("---")

# Supply-demand opportunity graph (network)
st.subheader("🌐 Supply-Demand Opportunity Network")
graph_data = analysis.get("supply_demand_graph", {})
nodes = graph_data.get("nodes", [])
edges = graph_data.get("edges", [])

if nodes and edges:
    G = nx.DiGraph()
    for node in nodes:
        G.add_node(node["id"], label=node["label"], node_type=node["type"])
    for edge in edges:
        G.add_edge(edge["from"], edge["to"], label=edge.get("label", ""), edge_type=edge.get("type", ""))

    # Layout
    pos = nx.spring_layout(G, seed=42, k=2.5)

    edge_traces = []
    for u, v, data in G.edges(data=True):
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        color = "#2ecc71" if data.get("edge_type") == "export" else "#3498db"
        edge_traces.append(go.Scatter(
            x=[x0, x1, None], y=[y0, y1, None],
            mode="lines",
            line=dict(width=1.5, color=color),
            hoverinfo="none", showlegend=False,
        ))

    # Nodes
    type_colors = {"ghana": "#f39c12", "supplier": "#3498db", "buyer": "#2ecc71"}
    node_x, node_y, node_text, node_colors, node_sizes = [], [], [], [], []
    for node_id, data in G.nodes(data=True):
        x, y = pos[node_id]
        node_x.append(x)
        node_y.append(y)
        node_text.append(data.get("label", node_id))
        ntype = data.get("node_type", "buyer")
        node_colors.append(type_colors.get(ntype, "#95a5a6"))
        node_sizes.append(30 if ntype == "ghana" else 20)

    node_trace = go.Scatter(
        x=node_x, y=node_y, mode="markers+text",
        text=node_text, textposition="top center",
        marker=dict(color=node_colors, size=node_sizes, line=dict(width=1, color="white")),
        hoverinfo="text",
    )

    fig_graph = go.Figure(data=edge_traces + [node_trace])
    fig_graph.update_layout(
        title="Ghana Trade Network: Commodity → Supply/Demand Connections",
        showlegend=False,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=500,
        margin=dict(l=20, r=20, t=50, b=20),
        plot_bgcolor="#f8f9fa",
    )
    st.plotly_chart(fig_graph, use_container_width=True)
    st.caption("🟡 Ghana nodes | 🔵 Supply sources (imports) | 🟢 Demand markets (exports) | → flow direction")
else:
    st.info("Graph data not available in this report.")

st.markdown("---")

# Commodity deep dive
st.subheader("🔍 Commodity Deep Dive")
selected = st.selectbox("Select commodity:", [o["commodity"] for o in export_opps])
opp = next(o for o in export_opps if o["commodity"] == selected)

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Opportunity Score", f"{opp['score']}/100")
    st.metric("Ghana Export Value", f"${opp['ghana_export_usd_m']}M/yr")
with c2:
    st.metric("YoY Export Growth", f"+{opp['yoy_growth_pct']}%")
    st.metric("Gross Margin", f"{opp['margin_pct']}%")
with c3:
    st.metric("Ghana Producer Price", f"${opp['ghana_producer_price_usd_mt']}/MT")
    st.metric("Price Premium", opp["price_premium"].upper())

# Market demand bar chart
markets = opp.get("all_markets", [])
if markets:
    mkt_df = pd.DataFrame(markets)
    mkt_df.columns = ["Country", "Demand Growth %", "Price Premium"]
    fig_mkt = px.bar(
        mkt_df, x="Country", y="Demand Growth %",
        color="Price Premium",
        color_discrete_map={"high": "#2ecc71", "medium": "#f39c12", "low": "#e74c3c"},
        title=f"Target Markets for {selected} — Demand Growth Rate",
    )
    fig_mkt.update_layout(height=350)
    st.plotly_chart(fig_mkt, use_container_width=True)

# Score breakdown
breakdown = opp.get("score_breakdown", {})
if breakdown:
    categories = list(breakdown.keys())
    max_vals = {"export_value": 30, "growth": 25, "margin": 25, "market_demand": 10, "budget_fit": 10}
    pct_values = [round(v / max_vals.get(k, 10) * 100) for k, v in breakdown.items()]
    fig_radar = go.Figure(go.Scatterpolar(
        r=pct_values + [pct_values[0]],
        theta=categories + [categories[0]],
        fill="toself", fillcolor="rgba(46, 204, 113, 0.3)",
        line_color="#27ae60",
    ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        title=f"Score Breakdown: {selected}", height=350,
    )
    st.plotly_chart(fig_radar, use_container_width=True)

st.markdown("---")
# Budget profitability
st.subheader("💰 Export Profitability Estimate")
budget_input = st.slider("Your sourcing budget (GHC)", 20_000, 100_000, 55_000, step=5_000)
producer_price = opp["ghana_producer_price_usd_mt"]
margin = opp["margin_pct"] / 100
if producer_price > 0:
    budget_usd = budget_input / usd_ghc
    qty_mt = budget_usd / producer_price
    gross_revenue_usd = budget_usd * (1 + margin)
    profit_usd = gross_revenue_usd - budget_usd
    profit_ghc = profit_usd * usd_ghc
    st.success(
        f"GHC {budget_input:,} buys **{qty_mt:.1f} MT** of {selected} locally "
        f"→ export value **${gross_revenue_usd:,.0f}** "
        f"→ estimated profit **GHC {profit_ghc:,.0f}**"
    )
    if margin < 0.20:
        st.error("⚠️ Margin below 20% minimum threshold")

st.caption("Weiss Rule: Request sample order first. Get quality certified by Ghana Standards Authority before full export.")
