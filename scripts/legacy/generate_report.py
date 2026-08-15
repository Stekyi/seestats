"""
Assembles weekly trade intelligence reports from analysis results.
Outputs: Markdown files + opportunity-graph.json in reports/YYYY-MM-DD/
"""
import json
import logging
from datetime import date
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from config import REPORTS_DIR, BUDGET_GHC, USD_GHC_RATE

logger = logging.getLogger(__name__)

# Weiss-book-derived action steps per commodity type
NEXT_STEPS = {
    "import": [
        "Contact GEPA Ghana (gepaghana.org) for approved import supplier lists",
        "Visit 3 wholesalers in Accra/Kumasi to confirm retail price and demand",
        "Request sample order (≤ GHC 5,000) before full commitment",
        "Check Ghana Customs (customs.gov.gh) for applicable duty rates",
        "Secure a buyer (retailer/wholesaler) with written purchase commitment first",
    ],
    "export": [
        "Register with GEPA Ghana as an exporter (free SME program)",
        "Contact 3 international buyers via trade leads (intracen.org/trade-leads)",
        "Get a product sample tested and certified (Ghana Standards Authority)",
        "Confirm packaging/labelling requirements for target market",
        "Start with small air-freight sample before full sea container",
    ],
}

DISCLAIMER = (
    "> **Disclaimer:** Data sourced from World Bank API, UN Comtrade, FAOSTAT, and published research (2023-2024). "
    "Prices and volumes are estimates. Always conduct your own due diligence before investing capital."
)


def _format_money(usd_m: float) -> str:
    if usd_m >= 1000:
        return f"${usd_m/1000:.1f}B"
    return f"${usd_m:.1f}M"


def _trend_arrow(pct: float) -> str:
    if pct > 15:
        return "↑↑"
    if pct > 0:
        return "↑"
    if pct < -5:
        return "↓↓"
    return "→"


def write_ghana_imports(report_dir: Path, ghana_data: dict):
    top_imports = ghana_data.get("top_imports", [])
    lines = [
        "# Ghana Import Report",
        f"**Week of {date.today()} | Budget: GHC {BUDGET_GHC:,} (~${BUDGET_GHC/USD_GHC_RATE:,.0f} USD)**\n",
        DISCLAIMER + "\n",
        "## Top Ghana Imports by Value (2023)\n",
        "| # | Commodity | Value | Share | YoY Growth | Signal |",
        "|---|---|---|---|---|---|",
    ]
    for i, row in enumerate(top_imports[:15], 1):
        val = row.get("value_usd_m", 0)
        yoy = row.get("yoy_growth", 0)
        arrow = _trend_arrow(yoy)
        govt = "🔒 Govt" if any(g in row["commodity"] for g in ["fuel", "oil", "mineral"]) else ""
        lines.append(
            f"| {i} | {row['commodity']} {govt} | ${val:.0f}M | {row.get('share_pct',0):.1f}% | {yoy:+.1f}% {arrow} | {'⚠️ High growth' if yoy > 20 else ''} |"
        )

    lines += [
        "",
        "## Import Opportunities for Small Business\n",
        "Commodities highlighted below are NOT government-monopolized and have viable distribution models",
        "within a GHC 100,000 budget:\n",
        "| Commodity | Annual Import | Growth | Why Viable |",
        "|---|---|---|---|",
        "| Rice | $487M | +23% | Distributor play — source from India/Vietnam |",
        "| Poultry (frozen) | $281M | +18% | Cold-chain distribution, consistent demand |",
        "| Tomato paste | $147M | +15% | High-turnover pantry staple |",
        "| Vegetable oils | $203M | +11% | Essential cooking ingredient, stable demand |",
        "| Sugar | $182M | +9%  | Industrial & retail, low barrier to entry |",
    ]
    (report_dir / "ghana-imports.md").write_text("\n".join(lines), encoding="utf-8")
    logger.info("  [OK] ghana-imports.md")


def write_ghana_exports(report_dir: Path, ghana_data: dict):
    top_exports = ghana_data.get("top_exports_nontrad", [])
    lines = [
        "# Ghana Non-Traditional Exports Report",
        f"**Week of {date.today()}**\n",
        DISCLAIMER + "\n",
        "## Top Non-Traditional Exports (2023)\n",
        "| # | Commodity | Value | Share | YoY Growth | Signal |",
        "|---|---|---|---|---|---|",
    ]
    for i, row in enumerate(top_exports[:15], 1):
        val = row.get("value_usd_m", 0)
        yoy = row.get("yoy_growth", 0)
        arrow = _trend_arrow(yoy)
        lines.append(
            f"| {i} | {row['commodity']} | ${val:.0f}M | {row.get('share_pct',0):.1f}% | {yoy:+.1f}% {arrow} | {'🚀 Hot' if yoy > 50 else ('📈 Growing' if yoy > 15 else '')} |"
        )
    lines += [
        "",
        "## Key Takeaways\n",
        "- **Shea butter/oil** leads non-traditional exports with **+116% YoY growth** — value-added processing is the opportunity",
        "- **Cashew nuts** are stable at $298M — large volume, existing export infrastructure",
        "- **Moringa** is small but growing fastest in the health supplement category",
        "- **Ginger** has strong consistent demand from Germany, USA, Japan",
        "- **Cocoa-derived** products are growing sharply but require processing capacity",
    ]
    (report_dir / "ghana-exports.md").write_text("\n".join(lines), encoding="utf-8")
    logger.info("  [OK] ghana-exports.md")


def write_gap_analysis(report_dir: Path, analysis: dict):
    import_opps = analysis.get("import_opportunities", [])
    export_opps = analysis.get("export_opportunities", [])
    summary = analysis.get("summary", {})

    lines = [
        "# Trade Gap Analysis",
        f"**Week of {date.today()} | GHC {BUDGET_GHC:,} Budget Analysis**\n",
        DISCLAIMER + "\n",
        "## Score Legend",
        "- 🟢 Score ≥ 70 — Strong opportunity",
        "- 🟡 Score 50-69 — Moderate opportunity",
        "- 🔴 Score < 50 — Low priority",
        "- Margin flag: 🟢 ≥30% | 🟡 20-29% | 🔴 <20%\n",
        f"## Summary: {summary.get('total_import_opps',0)} import + {summary.get('total_export_opps',0)} export opportunities identified",
        f"- **{summary.get('green_margin_opps',0)}** have green (≥30%) margin",
        f"- **{summary.get('budget_fit_opps',0)}** fit within GHC {BUDGET_GHC:,} budget\n",
        "## Import Opportunities (Ranked)\n",
        "| Score | Commodity | Ghana Import | Growth | Best Supplier | Price/MT | Est. Margin |",
        "|---|---|---|---|---|---|---|",
    ]
    for opp in import_opps:
        score = opp["score"]
        icon = "🟢" if score >= 70 else ("🟡" if score >= 50 else "🔴")
        mflag = {"green": "🟢", "yellow": "🟡", "red": "🔴"}.get(opp["margin_flag"], "")
        lines.append(
            f"| {icon} **{score}** | {opp['commodity']} | ${opp['ghana_import_usd_m']}M | "
            f"+{opp['yoy_growth_pct']}% | {opp['best_supplier']} | ${opp['best_price_usd_mt']}/MT | "
            f"{mflag} {opp['margin_pct']}% |"
        )

    lines += ["", "## Export Opportunities (Ranked)\n",
              "| Score | Commodity | Ghana Export | Growth | Best Market | Market Demand | Est. Margin |",
              "|---|---|---|---|---|---|---|"]
    for opp in export_opps:
        score = opp["score"]
        icon = "🟢" if score >= 70 else ("🟡" if score >= 50 else "🔴")
        mflag = {"green": "🟢", "yellow": "🟡", "red": "🔴"}.get(opp["margin_flag"], "")
        lines.append(
            f"| {icon} **{score}** | {opp['commodity']} | ${opp['ghana_export_usd_m']}M | "
            f"+{opp['yoy_growth_pct']}% | {opp['best_market']} | "
            f"+{opp['market_demand_growth_pct']}% | {mflag} {opp['margin_pct']}% |"
        )

    (report_dir / "gap-analysis.md").write_text("\n".join(lines), encoding="utf-8")
    logger.info("  [OK] gap-analysis.md")


def write_opportunities_brief(report_dir: Path, analysis: dict):
    top5 = analysis.get("top_5_overall", [])
    lines = [
        "# Top 5 Actionable Trade Opportunities",
        f"**Week of {date.today()} | Based on GHC {BUDGET_GHC:,} starting capital**\n",
        DISCLAIMER + "\n",
        "> *Principle (Weiss): Secure a confirmed buyer BEFORE spending capital on inventory.*\n",
    ]

    for rank, opp in enumerate(top5, 1):
        is_import = opp["type"] == "import_opportunity"
        direction = "IMPORT (distribute in Ghana)" if is_import else "EXPORT (sell abroad)"
        margin_icon = {"green": "🟢", "yellow": "🟡", "red": "🔴"}.get(opp["margin_flag"], "")
        score_icon = "🟢" if opp["score"] >= 70 else "🟡"
        commodity = opp["commodity"]

        lines += [
            f"---",
            f"## #{rank} — {commodity} | {direction}",
            f"**Opportunity Score: {score_icon} {opp['score']}/100 | Margin: {margin_icon} {opp['margin_pct']}%**\n",
        ]

        if is_import:
            lines += [
                f"- **Ghana imports:** ${opp['ghana_import_usd_m']}M/year, growing **+{opp['yoy_growth_pct']}% YoY**",
                f"- **Cheapest source:** {opp['best_supplier']} at **${opp['best_price_usd_mt']}/MT**",
                f"- **Starting order:** GHC {opp['est_order_ghc']:,} buys ~**{opp['est_order_qty_mt']} MT**",
                "",
                "**Supply sources:**",
            ]
            for sup in opp.get("all_suppliers", []):
                lines.append(f"  - {sup['country']}: ${sup['price_usd_mt']}/MT ({sup['distance']} distance)")
        else:
            lines += [
                f"- **Ghana exports:** ${opp['ghana_export_usd_m']}M/year, growing **+{opp['yoy_growth_pct']}% YoY**",
                f"- **Best market:** {opp['best_market']} (demand growing +{opp['market_demand_growth_pct']}%/yr)",
                f"- **Ghana producer price:** ${opp['ghana_producer_price_usd_mt']}/MT",
                f"- **Starting order:** GHC {opp['est_order_ghc']:,} buys ~**{opp['est_order_qty_mt']} MT**",
                f"- **Price premium:** {opp['price_premium'].upper()}",
                "",
                "**Target markets:**",
            ]
            for mkt in opp.get("all_markets", []):
                lines.append(f"  - {mkt['country']}: +{mkt['demand_growth_pct']}% demand growth, {mkt['price_premium']} premium")

        opp_type = "import" if is_import else "export"
        lines += ["", "**Next steps (Weiss method):**"]
        for step in NEXT_STEPS[opp_type]:
            lines.append(f"  - [ ] {step}")
        lines.append("")

    lines += [
        "---",
        "## Budget Allocation Suggestion\n",
        f"Starting capital: **GHC {BUDGET_GHC:,}** (~${BUDGET_GHC/USD_GHC_RATE:,.0f} USD)\n",
        "| Allocation | GHC | Purpose |",
        "|---|---|---|",
        f"| First shipment | 55,000 | 1 commodity, sample order |",
        f"| Working capital buffer | 25,000 | 3 months operating costs |",
        f"| Market research & travel | 10,000 | Buyer visits, supplier verification |",
        f"| Regulatory & customs | 7,000 | Broker fees, certifications |",
        f"| Emergency reserve | 3,000 | Contingency |",
        "",
        "> Start with ONE commodity. Master it. Reinvest profits before diversifying.",
    ]

    (report_dir / "opportunities-brief.md").write_text("\n".join(lines), encoding="utf-8")
    logger.info("  [OK] opportunities-brief.md")


def write_graph_json(report_dir: Path, analysis: dict):
    graph = analysis.get("supply_demand_graph", {})
    out = report_dir / "opportunity-graph.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(graph, f, indent=2)
    logger.info("  [OK] opportunity-graph.json")


def generate_all_reports(ghana_data: dict, analysis: dict) -> Path:
    today = str(date.today())
    report_dir = REPORTS_DIR / today
    report_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Writing reports to {report_dir}...")

    write_ghana_imports(report_dir, ghana_data)
    write_ghana_exports(report_dir, ghana_data)
    write_gap_analysis(report_dir, analysis)
    write_opportunities_brief(report_dir, analysis)
    write_graph_json(report_dir, analysis)

    # Save full analysis JSON for dashboard
    with open(report_dir / "analysis.json", "w", encoding="utf-8") as f:
        json.dump(analysis, f, indent=2)
    logger.info(f"All reports saved -> {report_dir}")
    return report_dir


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    from fetch_ghana import get_latest_ghana_data
    from fetch_comtrade import get_latest_comtrade_data
    from fetch_prices import get_latest_prices_data
    from analyze_gaps import run_analysis

    gh = get_latest_ghana_data()
    ct = get_latest_comtrade_data()
    pr = get_latest_prices_data()
    analysis = run_analysis(gh, ct, pr)
    path = generate_all_reports(gh, analysis)
    print(f"Reports in: {path}")
