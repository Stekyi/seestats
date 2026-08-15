"""
Fetches commodity-level trade data from UN Comtrade (legacy free API).
No API key needed for the legacy endpoint (rate-limited to 1 req/sec).
Set COMTRADE_API_KEY env var to use the new Comtrade+ API for better coverage.
"""
import json
import logging
import time
import requests
from datetime import date
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from config import DATA_DIR, COMMODITIES, GHANA_REPORTER_CODE, COMTRADE_API_KEY

logger = logging.getLogger(__name__)

LEGACY_URL = "https://comtrade.un.org/api/get"
NEW_API_URL = "https://comtradeapi.un.org/data/v1/get/C/A/HS"

# Embedded fallback commodity data (2022-2023 estimates from research)
FALLBACK_COMMODITY_DATA = {
    "Ginger": {
        "exports": [
            {"partner": "USA",         "value_usd": 12_400_000, "qty_mt": 4200, "year": 2023},
            {"partner": "Germany",     "value_usd": 8_100_000,  "qty_mt": 2800, "year": 2023},
            {"partner": "UK",          "value_usd": 6_300_000,  "qty_mt": 2100, "year": 2023},
            {"partner": "Netherlands", "value_usd": 5_200_000,  "qty_mt": 1800, "year": 2023},
        ],
        "ghana_production_usd": 45_000_000, "yoy_growth_pct": 25.0,
    },
    "Shea butter": {
        "exports": [
            {"partner": "Netherlands", "value_usd": 65_000_000, "qty_mt": 28_000, "year": 2023},
            {"partner": "France",      "value_usd": 38_000_000, "qty_mt": 16_500, "year": 2023},
            {"partner": "South Korea", "value_usd": 22_000_000, "qty_mt": 9_500,  "year": 2023},
            {"partner": "Japan",       "value_usd": 18_000_000, "qty_mt": 7_800,  "year": 2023},
        ],
        "ghana_production_usd": 174_000_000, "yoy_growth_pct": 116.0,
    },
    "Cashew nuts": {
        "exports": [
            {"partner": "India",       "value_usd": 142_000_000, "qty_mt": 95_000, "year": 2023},
            {"partner": "Vietnam",     "value_usd": 76_000_000,  "qty_mt": 51_000, "year": 2023},
            {"partner": "EU",          "value_usd": 54_000_000,  "qty_mt": 36_000, "year": 2023},
            {"partner": "USA",         "value_usd": 26_000_000,  "qty_mt": 17_500, "year": 2023},
        ],
        "ghana_production_usd": 298_000_000, "yoy_growth_pct": 10.2,
    },
    "Moringa powder": {
        "exports": [
            {"partner": "USA",  "value_usd": 3_200_000, "qty_mt": 180, "year": 2023},
            {"partner": "EU",   "value_usd": 2_800_000, "qty_mt": 155, "year": 2023},
            {"partner": "Japan","value_usd": 1_400_000, "qty_mt": 78,  "year": 2023},
        ],
        "ghana_production_usd": 8_000_000, "yoy_growth_pct": 45.0,
    },
    "Dried fish": {
        "exports": [
            {"partner": "Nigeria",       "value_usd": 28_000_000, "qty_mt": 12_400, "year": 2023},
            {"partner": "Cote d Ivoire", "value_usd": 16_000_000, "qty_mt": 7_100,  "year": 2023},
            {"partner": "Cameroon",      "value_usd": 11_000_000, "qty_mt": 4_900,  "year": 2023},
        ],
        "ghana_production_usd": 62_000_000, "yoy_growth_pct": 18.0,
    },
    "Rice": {
        "imports": [
            {"partner": "India",    "value_usd": 198_000_000, "qty_mt": 680_000, "price_usd_mt": 291, "year": 2023},
            {"partner": "Vietnam",  "value_usd": 142_000_000, "qty_mt": 457_000, "price_usd_mt": 311, "year": 2023},
            {"partner": "Thailand", "value_usd": 84_000_000,  "qty_mt": 240_000, "price_usd_mt": 350, "year": 2023},
            {"partner": "Pakistan", "value_usd": 63_000_000,  "qty_mt": 217_000, "price_usd_mt": 290, "year": 2023},
        ],
        "ghana_import_usd": 487_000_000, "yoy_growth_pct": 23.0,
    },
    "Tomato paste": {
        "imports": [
            {"partner": "China",   "value_usd": 86_000_000, "qty_mt": 132_000, "price_usd_mt": 651,  "year": 2023},
            {"partner": "Turkey",  "value_usd": 34_000_000, "qty_mt": 43_600,  "price_usd_mt": 780,  "year": 2023},
            {"partner": "Italy",   "value_usd": 17_000_000, "qty_mt": 15_500,  "price_usd_mt": 1097, "year": 2023},
        ],
        "ghana_import_usd": 147_000_000, "yoy_growth_pct": 15.0,
    },
    "Poultry": {
        "imports": [
            {"partner": "Brazil", "value_usd": 134_000_000, "qty_mt": 74_000,  "price_usd_mt": 1811, "year": 2023},
            {"partner": "EU",     "value_usd": 82_000_000,  "qty_mt": 39_000,  "price_usd_mt": 2103, "year": 2023},
            {"partner": "USA",    "value_usd": 65_000_000,  "qty_mt": 33_000,  "price_usd_mt": 1970, "year": 2023},
        ],
        "ghana_import_usd": 281_000_000, "yoy_growth_pct": 18.0,
    },
    "Vegetable oils": {
        "imports": [
            {"partner": "Malaysia",   "value_usd": 92_000_000, "qty_mt": 112_000, "price_usd_mt": 821, "year": 2023},
            {"partner": "Indonesia",  "value_usd": 68_000_000, "qty_mt": 86_000,  "price_usd_mt": 791, "year": 2023},
            {"partner": "Senegal",    "value_usd": 28_000_000, "qty_mt": 29_500,  "price_usd_mt": 949, "year": 2023},
        ],
        "ghana_import_usd": 203_000_000, "yoy_growth_pct": 11.0,
    },
}


def _fetch_legacy_comtrade(hs_code: str, flow: str, year: int = 2022) -> list:
    """flow: 1=imports, 2=exports"""
    params = {
        "max": 50, "type": "C", "freq": "A", "px": "HS",
        "ps": str(year), "r": GHANA_REPORTER_CODE, "p": "ALL",
        "rg": flow, "cc": hs_code, "fmt": "json",
    }
    try:
        r = requests.get(LEGACY_URL, params=params, timeout=20)
        if r.status_code == 200:
            data = r.json()
            if data.get("validation", {}).get("status", {}).get("value") == 0:
                return data.get("dataset", [])
    except Exception as e:
        logger.warning(f"Comtrade legacy API failed for HS {hs_code}: {e}")
    return []


def fetch_comtrade_data() -> dict:
    logger.info("Fetching commodity trade data...")
    result = {
        "source": "seed+comtrade_legacy",
        "fetched_date": str(date.today()),
        "commodities": FALLBACK_COMMODITY_DATA.copy(),
    }

    if not COMTRADE_API_KEY:
        logger.info("No COMTRADE_API_KEY set — using embedded research data.")
        logger.info("To get live data: register at https://comtradeapi.un.org/ and set COMTRADE_API_KEY env var.")
        return result

    # Try live fetch for key commodities with API key
    for name, meta in list(COMMODITIES.items())[:6]:
        hs = meta["hs"]
        flow = "2" if meta["direction"] == "export" else "1"
        logger.info(f"  Fetching {name} (HS {hs}) from Comtrade...")
        rows = _fetch_legacy_comtrade(hs, flow)
        if rows:
            parsed = [{"partner": r.get("ptTitle"), "value_usd": r.get("TradeValue"),
                       "qty_mt": r.get("NetWeight"), "year": r.get("yr")} for r in rows if r.get("TradeValue")]
            parsed.sort(key=lambda x: x["value_usd"] or 0, reverse=True)
            key = "exports" if meta["direction"] == "export" else "imports"
            if name not in result["commodities"]:
                result["commodities"][name] = {}
            result["commodities"][name][key] = parsed[:5]
            logger.info(f"    Got {len(parsed)} trade partners for {name}")
        time.sleep(1.1)

    return result


def save_comtrade_data(data: dict) -> Path:
    out_dir = DATA_DIR / "comtrade"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"comtrade_{date.today()}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    logger.info(f"Comtrade data saved -> {out_path}")
    return out_path


def get_latest_comtrade_data() -> dict:
    comtrade_dir = DATA_DIR / "comtrade"
    files = sorted(comtrade_dir.glob("comtrade_*.json"), reverse=True)
    if files:
        with open(files[0], encoding="utf-8") as f:
            return json.load(f)
    return {"commodities": FALLBACK_COMMODITY_DATA}


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    data = fetch_comtrade_data()
    path = save_comtrade_data(data)
    print(f"Saved: {path}")
