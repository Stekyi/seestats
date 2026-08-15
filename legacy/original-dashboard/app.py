"""
TradeOps Intelligence Dashboard — Entry Point
Run: streamlit run dashboard/app.py
"""
import json
import streamlit as st
from pathlib import Path
from datetime import date

REPORTS_DIR = Path(__file__).parent.parent / "reports"

st.set_page_config(
    page_title="TradeOps Ghana",
    page_icon="🇬🇭",
    layout="wide",
    initial_sidebar_state="expanded",
)


def get_report_dates() -> list:
    if not REPORTS_DIR.exists():
        return []
    return sorted([d.name for d in REPORTS_DIR.iterdir() if d.is_dir()], reverse=True)


def load_analysis(report_date: str) -> dict:
    path = REPORTS_DIR / report_date / "analysis.json"
    if path.exists():
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return {}


# Sidebar — report selector
st.sidebar.title("🇬🇭 TradeOps Ghana")
st.sidebar.caption("Ghana Trade Intelligence System")
st.sidebar.markdown("---")

dates = get_report_dates()
if dates:
    selected_date = st.sidebar.selectbox("📅 Report Week", dates, index=0)
    st.session_state["report_date"] = selected_date
    st.session_state["analysis"] = load_analysis(selected_date)
    st.sidebar.success(f"Loaded: {selected_date}")
else:
    st.session_state["report_date"] = None
    st.session_state["analysis"] = {}

st.sidebar.markdown("---")
st.sidebar.markdown("**Budget:** GHC 100,000")
st.sidebar.markdown("**Focus:** Non-traditional commodities")
st.sidebar.markdown("**Strategy:** Weiss Import/Export Method")
st.sidebar.markdown("---")
st.sidebar.markdown("**Data Sources:**")
st.sidebar.markdown("- World Bank API")
st.sidebar.markdown("- UN Comtrade")
st.sidebar.markdown("- FAOSTAT")
st.sidebar.markdown("- Ghana Statistical Service")
st.sidebar.markdown("---")
st.sidebar.caption("Auto-runs every Friday at 9 PM · Manual run: ⚙️ Pipeline Control")

# Home page content
st.title("🇬🇭 Ghana Trade Intelligence Dashboard")
st.caption(f"Your data-driven import/export business intelligence system | Today: {date.today()}")

if not dates:
    st.warning("No reports found. Run the pipeline first:")
    st.code("cd d:\\clawing\\tradeops && python scripts/run_pipeline.py", language="bash")
    st.stop()

analysis = st.session_state.get("analysis", {})
if not analysis:
    st.error(f"Could not load analysis for {selected_date}.")
    st.stop()

# KPI cards
summary = analysis.get("summary", {})
top5 = analysis.get("top_5_overall", [])

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Import Opportunities", summary.get("total_import_opps", 0))
with col2:
    st.metric("Export Opportunities", summary.get("total_export_opps", 0))
with col3:
    st.metric("Green Margin (≥30%)", summary.get("green_margin_opps", 0))
with col4:
    st.metric("Budget-Fit Opps", summary.get("budget_fit_opps", 0))

st.markdown("---")
st.subheader("🏆 Top 5 Opportunities This Week")

if top5:
    for i, opp in enumerate(top5, 1):
        direction = "🟦 IMPORT" if opp["type"] == "import_opportunity" else "🟩 EXPORT"
        score_color = "🟢" if opp["score"] >= 70 else ("🟡" if opp["score"] >= 50 else "🔴")
        margin_color = {"green": "🟢", "yellow": "🟡", "red": "🔴"}.get(opp["margin_flag"], "")

        with st.expander(f"#{i} {direction} — **{opp['commodity']}** | Score: {score_color} {opp['score']}/100 | Margin: {margin_color} {opp['margin_pct']}%"):
            c1, c2 = st.columns(2)
            with c1:
                if opp["type"] == "import_opportunity":
                    st.markdown(f"**Ghana imports:** ${opp['ghana_import_usd_m']}M/yr")
                    st.markdown(f"**Growth:** +{opp['yoy_growth_pct']}% YoY")
                    st.markdown(f"**Best supplier:** {opp['best_supplier']} @ ${opp['best_price_usd_mt']}/MT")
                else:
                    st.markdown(f"**Ghana exports:** ${opp['ghana_export_usd_m']}M/yr")
                    st.markdown(f"**Growth:** +{opp['yoy_growth_pct']}% YoY")
                    st.markdown(f"**Best market:** {opp['best_market']}")
            with c2:
                st.markdown(f"**Est. starting order:** GHC {opp['est_order_ghc']:,}")
                st.markdown(f"**Order quantity:** ~{opp['est_order_qty_mt']} MT")
                st.markdown(f"**Budget fit:** {'✅ Yes' if opp['budget_fit'] else '⚠️ Tight'}")

st.markdown("---")
st.info("💡 Use the sidebar pages to explore Import Gaps, Export Opportunities, and Trend Analysis in detail.")
st.caption("Based on *Building an Import/Export Business* (Weiss, 2007) methodology. Start with a confirmed buyer. Maintain ≥20% gross margin.")
