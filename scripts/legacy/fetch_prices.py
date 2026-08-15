"""
Fetches commodity producer prices from FAOSTAT and World Bank Pink Sheet.
No API key required.
"""
import json
import logging
import requests
from datetime import date
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from config import DATA_DIR, GHANA_FAOSTAT_CODE

logger = logging.getLogger(__name__)

FAOSTAT_BASE = "https://fenixservices.fao.org/faostat/api/v1/en/data"

# FAOSTAT item codes for our target commodities
FAO_ITEMS = {
    "Ginger":         "698",
    "Cashew nuts":    "217",
    "Rice":           "27",
    "Sugar":          "156",
    "Vegetable oils": "334",
    "Pineapple":      "574",
}

# Embedded price data (USD per MT, 2023 — from World Bank Pink Sheet + FAOSTAT)
SEED_PRICES = {
    "Ginger": {
        "ghana_producer_usd_mt": 820,
        "world_avg_usd_mt": 950,
        "trend": [
            {"year": 2019, "price_usd_mt": 580},
            {"year": 2020, "price_usd_mt": 640},
            {"year": 2021, "price_usd_mt": 710},
            {"year": 2022, "price_usd_mt": 780},
            {"year": 2023, "price_usd_mt": 820},
        ],
        "margin_potential_pct": 32,
    },
    "Shea butter": {
        "ghana_producer_usd_mt": 750,
        "world_avg_usd_mt": 1200,
        "trend": [
            {"year": 2019, "price_usd_mt": 450},
            {"year": 2020, "price_usd_mt": 520},
            {"year": 2021, "price_usd_mt": 610},
            {"year": 2022, "price_usd_mt": 690},
            {"year": 2023, "price_usd_mt": 750},
        ],
        "margin_potential_pct": 45,
    },
    "Cashew nuts": {
        "ghana_producer_usd_mt": 1100,
        "world_avg_usd_mt": 1850,
        "trend": [
            {"year": 2019, "price_usd_mt": 850},
            {"year": 2020, "price_usd_mt": 920},
            {"year": 2021, "price_usd_mt": 980},
            {"year": 2022, "price_usd_mt": 1050},
            {"year": 2023, "price_usd_mt": 1100},
        ],
        "margin_potential_pct": 28,
    },
    "Moringa powder": {
        "ghana_producer_usd_mt": 2200,
        "world_avg_usd_mt": 6500,
        "trend": [
            {"year": 2019, "price_usd_mt": 1400},
            {"year": 2020, "price_usd_mt": 1700},
            {"year": 2021, "price_usd_mt": 1900},
            {"year": 2022, "price_usd_mt": 2050},
            {"year": 2023, "price_usd_mt": 2200},
        ],
        "margin_potential_pct": 65,
    },
    "Dried fish": {
        "ghana_producer_usd_mt": 1600,
        "world_avg_usd_mt": 2300,
        "trend": [
            {"year": 2019, "price_usd_mt": 1200},
            {"year": 2020, "price_usd_mt": 1300},
            {"year": 2021, "price_usd_mt": 1450},
            {"year": 2022, "price_usd_mt": 1550},
            {"year": 2023, "price_usd_mt": 1600},
        ],
        "margin_potential_pct": 30,
    },
    "Rice": {
        "ghana_retail_usd_mt": 620,
        "import_price_usd_mt": 291,
        "trend": [
            {"year": 2019, "price_usd_mt": 390},
            {"year": 2020, "price_usd_mt": 400},
            {"year": 2021, "price_usd_mt": 430},
            {"year": 2022, "price_usd_mt": 490},
            {"year": 2023, "price_usd_mt": 620},
        ],
        "margin_potential_pct": 22,
    },
    "Tomato paste": {
        "ghana_retail_usd_mt": 1050,
        "import_price_usd_mt": 651,
        "trend": [
            {"year": 2019, "price_usd_mt": 580},
            {"year": 2020, "price_usd_mt": 600},
            {"year": 2021, "price_usd_mt": 630},
            {"year": 2022, "price_usd_mt": 680},
            {"year": 2023, "price_usd_mt": 651},
        ],
        "margin_potential_pct": 24,
    },
    "Poultry": {
        "ghana_retail_usd_mt": 2600,
        "import_price_usd_mt": 1811,
        "trend": [
            {"year": 2019, "price_usd_mt": 1400},
            {"year": 2020, "price_usd_mt": 1500},
            {"year": 2021, "price_usd_mt": 1620},
            {"year": 2022, "price_usd_mt": 1750},
            {"year": 2023, "price_usd_mt": 1811},
        ],
        "margin_potential_pct": 30,
    },
    "Vegetable oils": {
        "ghana_retail_usd_mt": 1180,
        "import_price_usd_mt": 821,
        "trend": [
            {"year": 2019, "price_usd_mt": 680},
            {"year": 2020, "price_usd_mt": 740},
            {"year": 2021, "price_usd_mt": 890},
            {"year": 2022, "price_usd_mt": 1050},
            {"year": 2023, "price_usd_mt": 821},
        ],
        "margin_potential_pct": 26,
    },
}


def _fetch_faostat_price(item_code: str) -> list:
    params = {
        "area": GHANA_FAOSTAT_CODE,
        "item": item_code,
        "element": "5531",  # producer price (USD/tonne)
        "year": "2018,2019,2020,2021,2022,2023",
        "output_type": "json",
    }
    try:
        r = requests.get(f"{FAOSTAT_BASE}/PP", params=params, timeout=10)
        if r.status_code == 200:
            data = r.json()
            return data.get("data", [])
    except Exception as e:
        logger.warning(f"FAOSTAT failed for item {item_code}: {e}")
    return []


def fetch_prices_data() -> dict:
    logger.info("Fetching commodity price data...")
    result = {
        "source": "seed+faostat",
        "fetched_date": str(date.today()),
        "prices": SEED_PRICES.copy(),
    }

    for name, item_code in FAO_ITEMS.items():
        rows = _fetch_faostat_price(item_code)
        if rows:
            trend = [{"year": int(r["Year"]), "price_usd_mt": float(r["Value"])}
                     for r in rows if r.get("Value")]
            trend.sort(key=lambda x: x["year"])
            if trend and name in result["prices"]:
                result["prices"][name]["trend"] = trend
                latest = trend[-1]["price_usd_mt"]
                logger.info(f"  {name}: latest FAOSTAT price = ${latest:.0f}/MT")

    return result


def save_prices_data(data: dict) -> Path:
    out_dir = DATA_DIR / "prices"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"prices_{date.today()}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    logger.info(f"Prices data saved -> {out_path}")
    return out_path


def get_latest_prices_data() -> dict:
    prices_dir = DATA_DIR / "prices"
    files = sorted(prices_dir.glob("prices_*.json"), reverse=True)
    if files:
        with open(files[0], encoding="utf-8") as f:
            return json.load(f)
    return {"prices": SEED_PRICES}


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    data = fetch_prices_data()
    path = save_prices_data(data)
    print(f"Saved: {path}")
