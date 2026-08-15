"""
Gap analysis engine: scores import deficits and export opportunities
for Ghana-based small-scale traders (GHC 100,000 budget).

Scoring criteria (from Weiss framework):
  - Gap/surplus size (30%)
  - YoY growth trend (25%)
  - Gross margin potential ≥ 20% (25%)
  - Logistics feasibility (10%)
  - Budget fit — order size ≤ GHC 50,000 (10%)
"""
import json
import logging
from datetime import date
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from config import (DATA_DIR, COMMODITIES, IMPORT_SUPPLIERS, EXPORT_MARKETS,
                    BUDGET_GHC, MAX_ORDER_GHC, USD_GHC_RATE)

logger = logging.getLogger(__name__)

GOVT_MONOPOLY = {"Gold", "Cocoa (raw)", "Petroleum", "Diamonds", "Bauxite"}
MIN_MARGIN_PCT = 20.0
LOGISTICS_SCORE = {"near": 10, "medium": 6, "far": 3}


def _score_import_opportunity(commodity: str, import_usd: float, yoy_growth: float,
                               margin_pct: float, suppliers: list) -> dict:
    best_supplier = suppliers[0] if suppliers else {}

    # 1. Gap size score (0-30): normalised against largest known import (Rice $487M)
    gap_score = min(30, (import_usd / 487_000_000) * 30)

    # 2. Growth trend score (0-25)
    growth_score = min(25, max(0, yoy_growth / 30 * 25))

    # 3. Margin score (0-25): full points if ≥30%, partial if 20-30%, 0 if <20%
    if margin_pct >= 30:
        margin_score = 25
    elif margin_pct >= MIN_MARGIN_PCT:
        margin_score = (margin_pct - MIN_MARGIN_PCT) / 10 * 25
    else:
        margin_score = 0

    # 4. Logistics score (0-10)
    distance = best_supplier.get("distance", "far")
    logistics_score = LOGISTICS_SCORE.get(distance, 3)

    # 5. Budget fit (0-10): can a GHC 60,000 order buy meaningful quantity?
    if best_supplier:
        price_usd_mt = best_supplier.get("price_usd_mt", 9999)
        order_usd = MAX_ORDER_GHC / USD_GHC_RATE
        order_qty_mt = order_usd / price_usd_mt if price_usd_mt else 0
        budget_score = 10 if order_qty_mt >= 5 else (10 * order_qty_mt / 5)
    else:
        budget_score = 5

    total = gap_score + growth_score + margin_score + logistics_score + budget_score
    total_100 = min(100, round(total))

    order_usd = MAX_ORDER_GHC / USD_GHC_RATE
    order_qty_mt = order_usd / best_supplier.get("price_usd_mt", 1) if best_supplier else 0

    return {
        "commodity": commodity,
        "type": "import_opportunity",
        "score": total_100,
        "margin_pct": margin_pct,
        "margin_flag": "green" if margin_pct >= 30 else ("yellow" if margin_pct >= MIN_MARGIN_PCT else "red"),
        "ghana_import_usd_m": round(import_usd / 1_000_000, 1),
        "yoy_growth_pct": yoy_growth,
        "best_supplier": best_supplier.get("country", "N/A"),
        "best_price_usd_mt": best_supplier.get("price_usd_mt", 0),
        "all_suppliers": suppliers,
        "est_order_qty_mt": round(order_qty_mt, 1),
        "est_order_ghc": MAX_ORDER_GHC,
        "budget_fit": budget_score >= 7,
        "score_breakdown": {
            "gap_size": round(gap_score, 1),
            "growth": round(growth_score, 1),
            "margin": round(margin_score, 1),
            "logistics": round(logistics_score, 1),
            "budget_fit": round(budget_score, 1),
        },
    }


def _score_export_opportunity(commodity: str, export_usd: float, yoy_growth: float,
                               margin_pct: float, markets: list,
                               ghana_price_usd_mt: float) -> dict:
    best_market = markets[0] if markets else {}

    # 1. Export value score (0-30)
    gap_score = min(30, (export_usd / 298_000_000) * 30)

    # 2. Growth trend (0-25)
    growth_score = min(25, max(0, yoy_growth / 120 * 25))

    # 3. Margin score (0-25)
    if margin_pct >= 40:
        margin_score = 25
    elif margin_pct >= MIN_MARGIN_PCT:
        margin_score = (margin_pct - MIN_MARGIN_PCT) / 20 * 25
    else:
        margin_score = 0

    # 4. Market demand score (0-10)
    demand_growth = best_market.get("demand_growth_pct", 0)
    logistics_score = min(10, demand_growth / 35 * 10)

    # 5. Budget fit: can we source GHC 50,000 worth?
    if ghana_price_usd_mt > 0:
        order_usd = MAX_ORDER_GHC / USD_GHC_RATE
        order_qty_mt = order_usd / ghana_price_usd_mt
        budget_score = 10 if order_qty_mt >= 2 else (10 * order_qty_mt / 2)
    else:
        budget_score = 5

    total_100 = min(100, round(gap_score + growth_score + margin_score + logistics_score + budget_score))

    order_usd = MAX_ORDER_GHC / USD_GHC_RATE
    order_qty_mt = order_usd / ghana_price_usd_mt if ghana_price_usd_mt else 0

    return {
        "commodity": commodity,
        "type": "export_opportunity",
        "score": total_100,
        "margin_pct": margin_pct,
        "margin_flag": "green" if margin_pct >= 30 else ("yellow" if margin_pct >= MIN_MARGIN_PCT else "red"),
        "ghana_export_usd_m": round(export_usd / 1_000_000, 1),
        "yoy_growth_pct": yoy_growth,
        "best_market": best_market.get("country", "N/A"),
        "market_demand_growth_pct": best_market.get("demand_growth_pct", 0),
        "price_premium": best_market.get("price_premium", "unknown"),
        "all_markets": markets,
        "ghana_producer_price_usd_mt": ghana_price_usd_mt,
        "est_order_qty_mt": round(order_qty_mt, 1),
        "est_order_ghc": MAX_ORDER_GHC,
        "budget_fit": budget_score >= 7,
        "score_breakdown": {
            "export_value": round(gap_score, 1),
            "growth": round(growth_score, 1),
            "margin": round(margin_score, 1),
            "market_demand": round(logistics_score, 1),
            "budget_fit": round(budget_score, 1),
        },
    }


def run_analysis(ghana_data: dict, comtrade_data: dict, prices_data: dict) -> dict:
    logger.info("Running gap analysis and opportunity scoring...")
    import_opps = []
    export_opps = []
    prices = prices_data.get("prices", {})
    commodities_ct = comtrade_data.get("commodities", {})
    top_imports = ghana_data.get("top_imports", [])
    top_exports = ghana_data.get("top_exports_nontrad", [])

    # Build lookup from top_imports/exports lists
    import_lookup = {r["commodity"]: r for r in top_imports}
    export_lookup = {r["commodity"]: r for r in top_exports}

    # Score import opportunities
    import_commodity_map = {
        "Rice":           "Rice",
        "Tomato paste":   "Tomato paste",
        "Poultry":        "Poultry (frozen)",
        "Vegetable oils": "Vegetable oils",
        "Sugar":          "Sugar & sugar products",
        "Wheat flour":    "Wheat & wheat flour",
    }
    for comm_name, lookup_key in import_commodity_map.items():
        if comm_name in GOVT_MONOPOLY:
            continue
        ghana_row = import_lookup.get(lookup_key, {})
        import_usd = ghana_row.get("value_usd_m", 0) * 1_000_000
        yoy_growth = ghana_row.get("yoy_growth", 10)
        price_info = prices.get(comm_name, {})
        margin_pct = price_info.get("margin_potential_pct", 0)
        suppliers = IMPORT_SUPPLIERS.get(comm_name, [])
        if import_usd > 0:
            opp = _score_import_opportunity(comm_name, import_usd, yoy_growth, margin_pct, suppliers)
            import_opps.append(opp)
            logger.info(f"  Import [{comm_name}]: score {opp['score']}/100, margin {margin_pct}%")

    # Score export opportunities
    export_commodity_map = {
        "Ginger":         "Ginger (processed)",
        "Shea butter":    "Shea butter/oil",
        "Cashew nuts":    "Cashew nuts",
        "Moringa powder": "Moringa products",
        "Dried fish":     "Dried/smoked fish",
        "Pineapple":      "Pineapple",
    }
    for comm_name, lookup_key in export_commodity_map.items():
        if comm_name in GOVT_MONOPOLY:
            continue
        ghana_row = export_lookup.get(lookup_key, {})
        export_usd = ghana_row.get("value_usd_m", 0) * 1_000_000
        yoy_growth = ghana_row.get("yoy_growth", 10)
        price_info = prices.get(comm_name, {})
        margin_pct = price_info.get("margin_potential_pct", 0)
        ghana_price = price_info.get("ghana_producer_usd_mt", 500)
        markets = EXPORT_MARKETS.get(comm_name, [])
        if export_usd > 0 or comm_name in commodities_ct:
            if export_usd == 0:
                ct = commodities_ct.get(comm_name, {})
                export_usd = ct.get("ghana_production_usd", 5_000_000)
                yoy_growth = ct.get("yoy_growth_pct", 10)
            opp = _score_export_opportunity(comm_name, export_usd, yoy_growth, margin_pct, markets, ghana_price)
            export_opps.append(opp)
            logger.info(f"  Export [{comm_name}]: score {opp['score']}/100, margin {margin_pct}%")

    import_opps.sort(key=lambda x: x["score"], reverse=True)
    export_opps.sort(key=lambda x: x["score"], reverse=True)
    all_opps = sorted(import_opps + export_opps, key=lambda x: x["score"], reverse=True)

    # Build supply-demand graph
    graph = {"nodes": [], "edges": []}
    for opp in all_opps[:10]:
        comm = opp["commodity"]
        graph["nodes"].append({"id": f"GHA_{comm}", "label": f"Ghana\n{comm}", "type": "ghana"})
        if opp["type"] == "import_opportunity":
            for sup in opp["all_suppliers"][:3]:
                node_id = sup["country"]
                if not any(n["id"] == node_id for n in graph["nodes"]):
                    graph["nodes"].append({"id": node_id, "label": node_id, "type": "supplier"})
                graph["edges"].append({
                    "from": node_id, "to": f"GHA_{comm}",
                    "label": f"${sup['price_usd_mt']}/MT", "type": "import"
                })
        else:
            for mkt in opp["all_markets"][:3]:
                node_id = mkt["country"]
                if not any(n["id"] == node_id for n in graph["nodes"]):
                    graph["nodes"].append({"id": node_id, "label": node_id, "type": "buyer"})
                graph["edges"].append({
                    "from": f"GHA_{comm}", "to": node_id,
                    "label": f"+{mkt['demand_growth_pct']}%", "type": "export"
                })

    return {
        "analysis_date": str(date.today()),
        "budget_ghc": BUDGET_GHC,
        "budget_usd": round(BUDGET_GHC / USD_GHC_RATE, 0),
        "import_opportunities": import_opps,
        "export_opportunities": export_opps,
        "top_5_overall": all_opps[:5],
        "supply_demand_graph": graph,
        "summary": {
            "total_import_opps": len(import_opps),
            "total_export_opps": len(export_opps),
            "green_margin_opps": sum(1 for o in all_opps if o["margin_flag"] == "green"),
            "budget_fit_opps": sum(1 for o in all_opps if o["budget_fit"]),
        }
    }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    from fetch_ghana import get_latest_ghana_data
    from fetch_comtrade import get_latest_comtrade_data
    from fetch_prices import get_latest_prices_data

    gh = get_latest_ghana_data()
    ct = get_latest_comtrade_data()
    pr = get_latest_prices_data()
    result = run_analysis(gh, ct, pr)
    print(json.dumps(result["top_5_overall"], indent=2))
