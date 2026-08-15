"""
Fetches Ghana macro trade indicators from World Bank API.
No API key required. Falls back to embedded research data if API unavailable.
"""
import json
import logging
import requests
from datetime import date
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from config import DATA_DIR

logger = logging.getLogger(__name__)

WB_BASE = "https://api.worldbank.org/v2"
GHANA_ISO = "GHA"

INDICATORS = {
    "imports_usd":     "NE.IMP.GNFS.CD",
    "exports_usd":     "NE.EXP.GNFS.CD",
    "imports_pct_gdp": "TM.VAL.MRCH.GN.ZS",
    "exports_pct_gdp": "TX.VAL.MRCH.GN.ZS",
    "gdp_usd":         "NY.GDP.MKTP.CD",
    "trade_pct_gdp":   "NE.TRD.GNFS.ZS",
}

# Embedded seed data (from Ghana Statistical Service / WITS research, 2023-2024)
SEED_DATA = {
    "macro": {
        "2023": {
            "imports_usd": 16_394_000_000,
            "exports_usd": 16_875_000_000,
            "gdp_usd":     72_840_000_000,
            "trade_balance_usd": 481_000_000,
        },
        "2022": {
            "imports_usd": 17_200_000_000,
            "exports_usd": 16_100_000_000,
            "gdp_usd":     71_300_000_000,
            "trade_balance_usd": -1_100_000_000,
        },
        "2021": {
            "imports_usd": 13_900_000_000,
            "exports_usd": 15_300_000_000,
            "gdp_usd":     77_500_000_000,
            "trade_balance_usd": 1_400_000_000,
        },
    },
    "top_imports": [
        {"commodity": "Mineral fuels & oils",    "value_usd_m": 5242, "share_pct": 32.0, "yoy_growth": 8.5,  "hs": "27"},
        {"commodity": "Rice",                    "value_usd_m": 487,  "share_pct": 3.0,  "yoy_growth": 23.0, "hs": "1006"},
        {"commodity": "Poultry (frozen)",        "value_usd_m": 281,  "share_pct": 1.7,  "yoy_growth": 18.0, "hs": "0207"},
        {"commodity": "Tomato paste",            "value_usd_m": 147,  "share_pct": 0.9,  "yoy_growth": 15.0, "hs": "2002"},
        {"commodity": "Vegetable oils",          "value_usd_m": 203,  "share_pct": 1.2,  "yoy_growth": 11.0, "hs": "1509"},
        {"commodity": "Sugar & sugar products",  "value_usd_m": 182,  "share_pct": 1.1,  "yoy_growth": 9.0,  "hs": "1701"},
        {"commodity": "Wheat & wheat flour",     "value_usd_m": 124,  "share_pct": 0.8,  "yoy_growth": 7.0,  "hs": "1001"},
        {"commodity": "Machinery & equipment",   "value_usd_m": 1840, "share_pct": 11.2, "yoy_growth": 5.0,  "hs": "84"},
        {"commodity": "Vehicles",                "value_usd_m": 643,  "share_pct": 3.9,  "yoy_growth": -3.0, "hs": "87"},
        {"commodity": "Pharmaceuticals",         "value_usd_m": 312,  "share_pct": 1.9,  "yoy_growth": 12.0, "hs": "30"},
    ],
    "top_exports_nontrad": [
        {"commodity": "Shea butter/oil",         "value_usd_m": 174, "share_pct": 1.0,  "yoy_growth": 116.0, "hs": "1515"},
        {"commodity": "Cashew nuts",             "value_usd_m": 298, "share_pct": 1.8,  "yoy_growth": 10.2,  "hs": "0801"},
        {"commodity": "Tuna (canned/processed)", "value_usd_m": 214, "share_pct": 1.3,  "yoy_growth": 37.3,  "hs": "1604"},
        {"commodity": "Cocoa paste",             "value_usd_m": 789, "share_pct": 4.7,  "yoy_growth": 71.0,  "hs": "1803"},
        {"commodity": "Cocoa butter",            "value_usd_m": 636, "share_pct": 3.8,  "yoy_growth": 120.0, "hs": "1804"},
        {"commodity": "Ginger (processed)",      "value_usd_m": 45,  "share_pct": 0.3,  "yoy_growth": 25.0,  "hs": "0910"},
        {"commodity": "Pineapple",               "value_usd_m": 38,  "share_pct": 0.2,  "yoy_growth": 12.0,  "hs": "0804"},
        {"commodity": "Moringa products",        "value_usd_m": 8,   "share_pct": 0.1,  "yoy_growth": 45.0,  "hs": "1212"},
        {"commodity": "Dried/smoked fish",       "value_usd_m": 62,  "share_pct": 0.4,  "yoy_growth": 18.0,  "hs": "0305"},
        {"commodity": "Rubber",                  "value_usd_m": 94,  "share_pct": 0.6,  "yoy_growth": 6.0,   "hs": "4001"},
    ],
}


def _fetch_wb_indicator(indicator: str, years: int = 6) -> list:
    url = f"{WB_BASE}/country/{GHANA_ISO}/indicator/{indicator}"
    params = {"format": "json", "per_page": years, "mrv": years}
    try:
        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()
        payload = r.json()
        if len(payload) >= 2 and payload[1]:
            return payload[1]
    except Exception as e:
        logger.warning(f"World Bank API failed for {indicator}: {e}")
    return []


def fetch_ghana_data() -> dict:
    logger.info("Fetching Ghana macro data from World Bank API...")
    result = {"source": "seed+worldbank", "fetched_date": str(date.today()), "macro_timeseries": {}, **SEED_DATA}

    for key, indicator_code in INDICATORS.items():
        rows = _fetch_wb_indicator(indicator_code)
        if rows:
            ts = {str(r["date"]): r["value"] for r in rows if r.get("value") is not None}
            if ts:
                result["macro_timeseries"][key] = ts
                logger.info(f"  Got {key}: {len(ts)} years of data")

    return result


def save_ghana_data(data: dict) -> Path:
    out_dir = DATA_DIR / "ghana"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"ghana_trade_{date.today()}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    logger.info(f"Ghana data saved -> {out_path}")
    return out_path


def get_latest_ghana_data() -> dict:
    ghana_dir = DATA_DIR / "ghana"
    files = sorted(ghana_dir.glob("ghana_trade_*.json"), reverse=True)
    if files:
        with open(files[0], encoding="utf-8") as f:
            return json.load(f)
    return SEED_DATA


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    data = fetch_ghana_data()
    path = save_ghana_data(data)
    print(f"Saved: {path}")
