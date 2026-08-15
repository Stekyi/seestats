"""
Blue Ocean Discovery Space — undiscovered / niche Ghana trade opportunities
that established exporters and importers have NOT yet commercialised at scale.
"""
import sys
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import pandas as pd
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))
from discover_opportunities import (
    get_all_discoveries,
    get_top_discoveries,
    get_discovery_summary,
    DISCOVERY_DATE,
)

st.set_page_config(page_title="Discovery Space", page_icon="🔭", layout="wide")

st.title("🔭 Blue Ocean Discovery Space")
st.caption(
    "Undiscovered, niche, and first-mover opportunities nobody else is chasing yet — "
    "researched from global trade trends, diaspora markets, and category white-space analysis."
)

st.info(
    "**What makes these 'blue ocean'?** These are commodities or products where Ghana has "
    "a real competitive advantage, global demand is growing, but NO established exporter "
    "or importer has yet built a brand or system around it. First-mover wins the whole market."
)

# ─── Summary KPIs ────────────────────────────────────────────────────────────
summary = get_discovery_summary()
discoveries = get_all_discoveries()

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Total Discoveries Identified", summary["total"])
with c2:
    extreme = summary["tiers"].get("EXTREME", 0)
    st.metric("EXTREME Blue Ocean Picks", extreme, delta="Act now")
with c3:
    st.metric("Avg Discovery Score", f"{summary['avg_score']}/100")
with c4:
    st.metric("Highest Margin Product", summary["highest_margin"][:20] + "…")

st.markdown("---")

# ─── Tier legend ─────────────────────────────────────────────────────────────
with st.expander("📖 How to read the Blue Ocean Tiers", expanded=False):
    st.markdown("""
| Tier | Meaning | Action |
|------|---------|--------|
| 🔴 EXTREME | Zero or near-zero competition, high margin, Ghana advantage is undeniable | Start within 90 days |
| 🟠 HIGH | Very few competitors, strong demand signal, niche is confirmed | Start within 6 months |
| 🟡 MEDIUM-HIGH | Some early movers exist, but Ghana can still differentiate | Plan carefully, move fast |
| 🟢 MEDIUM | Emerging opportunity, needs more validation or has moderate competition | Watch and validate |

**Scoring (100 pts total):**
- 30% Market saturation (inverted) — lower competition = higher score
- 25% Ghana competitive advantage
- 25% Global demand trajectory (CAGR & trend)
- 10% Entry barrier / budget fit (GHC 100,000 budget)
- 10% First-mover advantage durability
    """)

# ─── Scatter: Score vs Margin ─────────────────────────────────────────────────
st.subheader("📊 Discovery Map — Score vs Gross Margin")
st.caption("Ideal discoveries are in the top-right quadrant: high score AND high margin.")

tier_colors = {"EXTREME": "#e74c3c", "HIGH": "#e67e22", "MEDIUM-HIGH": "#f1c40f", "MEDIUM": "#27ae60"}
df = pd.DataFrame([
    {
        "Name": d["name"].split("(")[0].strip(),
        "Score": d["total_score"],
        "Margin %": d["gross_margin_pct"],
        "Tier": d["blue_ocean_tier"],
        "Direction": d["direction"].upper(),
        "Starting GHC": d["starting_order_ghc"],
        "Color": tier_colors.get(d["blue_ocean_tier"], "#95a5a6"),
    }
    for d in discoveries
])

fig = go.Figure()
for tier, color in tier_colors.items():
    sub = df[df["Tier"] == tier]
    if sub.empty:
        continue
    fig.add_trace(go.Scatter(
        x=sub["Score"], y=sub["Margin %"],
        mode="markers+text",
        name=tier,
        marker=dict(size=14, color=color, line=dict(width=1, color="white")),
        text=sub["Name"],
        textposition="top center",
        hovertemplate=(
            "<b>%{text}</b><br>Score: %{x}/100<br>Margin: %{y}%<extra></extra>"
        ),
    ))

fig.add_hline(y=20, line_dash="dash", line_color="gray",
              annotation_text="20% margin minimum (Weiss threshold)")
fig.add_vline(x=70, line_dash="dash", line_color="gray",
              annotation_text="Score threshold 70+")
fig.update_layout(
    xaxis_title="Blue Ocean Score (/100)",
    yaxis_title="Gross Margin (%)",
    height=500,
    legend_title="Blue Ocean Tier",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
)
st.plotly_chart(fig, use_container_width=True)

# ─── Ranked table ─────────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("🏆 All Discoveries — Ranked by Blue Ocean Score")

tier_emoji = {"EXTREME": "🔴", "HIGH": "🟠", "MEDIUM-HIGH": "🟡", "MEDIUM": "🟢"}

table_rows = []
for d in discoveries:
    table_rows.append({
        "Tier": f"{tier_emoji.get(d['blue_ocean_tier'], '')} {d['blue_ocean_tier']}",
        "Discovery": d["name"].split("(")[0].strip(),
        "Category": d["category"],
        "Direction": d["direction"].upper(),
        "Score": d["total_score"],
        "Est. Margin": f"{d['gross_margin_pct']}%",
        "Start (GHC)": f"GHC {d['starting_order_ghc']:,}",
        "Tagline": d["tagline"],
    })

tdf = pd.DataFrame(table_rows)

def colour_score(val):
    if val >= 85:
        return "background-color: #1a5c1a; color: white"
    if val >= 70:
        return "background-color: #3d7a00; color: white"
    if val >= 55:
        return "background-color: #b8860b; color: white"
    return "background-color: #8b0000; color: white"

st.dataframe(
    tdf.style.map(colour_score, subset=["Score"]),
    use_container_width=True,
    hide_index=True,
)

# ─── Detail drill-down ────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("🔍 Drill into a Discovery")

names = [d["name"].split("(")[0].strip() for d in discoveries]
selected_name = st.selectbox("Select a discovery to explore in depth:", names)
selected = next(d for d in discoveries if d["name"].startswith(selected_name))

tier_colors_css = {
    "EXTREME": "#e74c3c", "HIGH": "#e67e22", "MEDIUM-HIGH": "#f1c40f", "MEDIUM": "#27ae60"
}
tier_col = tier_colors_css.get(selected["blue_ocean_tier"], "#888")

st.markdown(
    f"<div style='padding:12px; border-left: 5px solid {tier_col}; background:#111'>"
    f"<b style='font-size:1.2em'>{selected['name']}</b><br>"
    f"<em>{selected['tagline']}</em>"
    f"</div>",
    unsafe_allow_html=True,
)
st.markdown("")

col_a, col_b = st.columns([3, 2])

with col_a:
    st.markdown("#### Why is this undiscovered?")
    st.write(selected["why_undiscovered"])

    st.markdown("#### Who to sell to (Early-adopter buyers)")
    for b in selected.get("target_buyers", []):
        with st.expander(f"🏢 {b['name']} — {b['type']}"):
            st.info(b["approach"])

with col_b:
    # Radar / score breakdown
    categories = [
        "Market Saturation\n(inverted)",
        "Ghana Advantage",
        "Demand Trajectory",
        "Entry Barrier",
        "First Mover",
    ]
    max_vals = [30, 25, 25, 10, 10]
    actual = [
        selected["market_saturation_score"],
        selected["ghana_advantage_score"],
        selected["demand_trajectory_score"],
        selected["entry_barrier_score"],
        selected["first_mover_score"],
    ]
    pct = [a / m * 100 for a, m in zip(actual, max_vals)]

    radar_fig = go.Figure(go.Scatterpolar(
        r=pct + [pct[0]],
        theta=categories + [categories[0]],
        fill="toself",
        fillcolor="rgba(231, 76, 60, 0.3)",
        line=dict(color="#e74c3c"),
    ))
    radar_fig.update_layout(
        polar=dict(radialaxis=dict(range=[0, 100], visible=True)),
        showlegend=False,
        height=320,
        margin=dict(l=40, r=40, t=40, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(radar_fig, use_container_width=True)

    # Key numbers
    st.markdown("#### At a glance")
    st.metric("Blue Ocean Score", f"{selected['total_score']}/100")
    st.metric("Estimated Gross Margin", f"{selected['gross_margin_pct']}%")
    st.metric("Starting Investment", f"GHC {selected['starting_order_ghc']:,}")
    if selected.get("global_market_size_usd"):
        st.metric("Global Market Size", selected["global_market_size_usd"])
    if selected.get("demand_cagr_pct"):
        st.metric("Demand CAGR", f"{selected['demand_cagr_pct']}%")

# Price trend chart
price_trend = selected.get("price_trend", {})
if price_trend:
    st.markdown("#### Price / Value Trend (USD/kg or USD/unit)")
    years = list(price_trend.keys())
    prices = list(price_trend.values())
    trend_fig = go.Figure(go.Scatter(
        x=years, y=prices,
        mode="lines+markers",
        line=dict(color="#e74c3c", width=2),
        marker=dict(size=8),
        hovertemplate="%{x}: $%{y}<extra></extra>",
    ))
    trend_fig.update_layout(
        height=280,
        yaxis_title="USD per kg (or unit)",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    # Mark the estimate year differently
    if years:
        last_year = years[-1]
        if "est" in str(last_year).lower() or "2025" in str(last_year):
            trend_fig.add_annotation(
                x=last_year, y=prices[-1],
                text="Estimate",
                showarrow=True, arrowhead=2,
                font=dict(color="yellow"),
            )
    st.plotly_chart(trend_fig, use_container_width=True)

# Trend keywords
kws = selected.get("trend_keywords", [])
if kws:
    st.markdown("#### Trending search terms (Google Trends / social)")
    st.markdown(" · ".join([f"`{k}`" for k in kws]))

# Risks
st.markdown("#### ⚠️ Risks to manage")
for r in selected.get("risks", []):
    st.warning(r)

# ─── Discovery vs Established comparison ──────────────────────────────────────
st.markdown("---")
st.subheader("📈 Why Now? Discovery vs Established Commodity Score Comparison")
st.caption(
    "Established opportunities have more data but more competition. "
    "Discoveries have less data but the field is open."
)

established = [
    {"name": "Shea butter", "score": 78, "saturation": "High", "type": "Established"},
    {"name": "Cashew nuts", "score": 71, "saturation": "High", "type": "Established"},
    {"name": "Moringa powder", "score": 75, "saturation": "Medium", "type": "Established"},
    {"name": "Rice (import)", "score": 68, "saturation": "High", "type": "Established"},
]
discovery_compare = [
    {"name": d["name"].split("(")[0].strip()[:22], "score": d["total_score"],
     "saturation": "Low", "type": "Discovery"}
    for d in discoveries[:5]
]
compare_df = pd.DataFrame(established + discovery_compare)

bar_fig = px.bar(
    compare_df,
    x="name", y="score",
    color="type",
    color_discrete_map={"Established": "#3498db", "Discovery": "#e74c3c"},
    labels={"name": "Commodity / Discovery", "score": "Score /100"},
    title="Established Opportunities vs Blue Ocean Discoveries",
    barmode="group",
)
bar_fig.update_layout(
    height=400,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    xaxis_tickangle=-30,
)
st.plotly_chart(bar_fig, use_container_width=True)

st.markdown("---")
st.caption(
    f"Discovery data compiled: {DISCOVERY_DATE} | "
    "Sources: PubMed, ITC Trade Map, UNCTAD, EU Organic data, Amazon bestseller analysis, "
    "specialty food trade publications. Prices are indicative estimates based on published research."
)
