import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"
LOGS_DIR = BASE_DIR / "logs"

COMTRADE_API_KEY = os.getenv("COMTRADE_API_KEY", "")
GHANA_REPORTER_CODE = "288"
GHANA_FAOSTAT_CODE = "59"
BUDGET_GHC = 100_000
USD_GHC_RATE = 15.4
BUDGET_USD = BUDGET_GHC / USD_GHC_RATE
MAX_ORDER_GHC = 60_000

# Target commodities: HS code, FAOSTAT item code, trade direction
COMMODITIES = {
    "Ginger":         {"hs": "0910", "fao_item": "698",  "direction": "export", "perishable": False},
    "Shea butter":    {"hs": "1515", "fao_item": "263",  "direction": "export", "perishable": False},
    "Cashew nuts":    {"hs": "0801", "fao_item": "217",  "direction": "export", "perishable": False},
    "Moringa powder": {"hs": "1212", "fao_item": None,   "direction": "export", "perishable": False},
    "Dried fish":     {"hs": "0305", "fao_item": "1183", "direction": "export", "perishable": False},
    "Pineapple":      {"hs": "0804", "fao_item": "574",  "direction": "export", "perishable": True},
    "Rice":           {"hs": "1006", "fao_item": "27",   "direction": "import", "perishable": False},
    "Tomato paste":   {"hs": "2002", "fao_item": "544",  "direction": "import", "perishable": False},
    "Poultry":        {"hs": "0207", "fao_item": "1058", "direction": "import", "perishable": False},
    "Vegetable oils": {"hs": "1509", "fao_item": "334",  "direction": "import", "perishable": False},
    "Sugar":          {"hs": "1701", "fao_item": "156",  "direction": "import", "perishable": False},
    "Wheat flour":    {"hs": "1101", "fao_item": "16",   "direction": "import", "perishable": False},
}

# Known global supply sources for import commodities (price per MT in USD)
IMPORT_SUPPLIERS = {
    "Rice":         [{"country": "India",    "price_usd_mt": 290, "distance": "medium"},
                     {"country": "Vietnam",  "price_usd_mt": 310, "distance": "far"},
                     {"country": "Thailand", "price_usd_mt": 350, "distance": "far"}],
    "Tomato paste": [{"country": "China",    "price_usd_mt": 650,  "distance": "far"},
                     {"country": "Turkey",   "price_usd_mt": 780,  "distance": "medium"},
                     {"country": "Italy",    "price_usd_mt": 1100, "distance": "medium"}],
    "Poultry":      [{"country": "Brazil",   "price_usd_mt": 1800, "distance": "far"},
                     {"country": "EU",       "price_usd_mt": 2100, "distance": "medium"},
                     {"country": "USA",      "price_usd_mt": 1950, "distance": "far"}],
    "Vegetable oils":[{"country": "Malaysia","price_usd_mt": 820,  "distance": "far"},
                     {"country": "Indonesia","price_usd_mt": 790,  "distance": "far"},
                     {"country": "Senegal",  "price_usd_mt": 950,  "distance": "near"}],
    "Sugar":        [{"country": "Brazil",   "price_usd_mt": 380,  "distance": "far"},
                     {"country": "India",    "price_usd_mt": 360,  "distance": "medium"},
                     {"country": "Thailand", "price_usd_mt": 395,  "distance": "far"}],
    "Wheat flour":  [{"country": "Turkey",   "price_usd_mt": 290,  "distance": "medium"},
                     {"country": "USA",      "price_usd_mt": 320,  "distance": "far"},
                     {"country": "EU",       "price_usd_mt": 310,  "distance": "medium"}],
}

# Known export demand markets
EXPORT_MARKETS = {
    "Ginger":         [{"country": "USA",         "demand_growth_pct": 22, "price_premium": "high"},
                       {"country": "Germany",     "demand_growth_pct": 18, "price_premium": "high"},
                       {"country": "Japan",       "demand_growth_pct": 15, "price_premium": "medium"}],
    "Shea butter":    [{"country": "Netherlands", "demand_growth_pct": 25, "price_premium": "high"},
                       {"country": "France",      "demand_growth_pct": 20, "price_premium": "high"},
                       {"country": "South Korea", "demand_growth_pct": 30, "price_premium": "high"}],
    "Cashew nuts":    [{"country": "India",       "demand_growth_pct": 12, "price_premium": "medium"},
                       {"country": "Vietnam",     "demand_growth_pct": 10, "price_premium": "medium"},
                       {"country": "EU",          "demand_growth_pct": 18, "price_premium": "high"}],
    "Moringa powder": [{"country": "USA",         "demand_growth_pct": 35, "price_premium": "high"},
                       {"country": "EU",          "demand_growth_pct": 30, "price_premium": "high"},
                       {"country": "Japan",       "demand_growth_pct": 28, "price_premium": "high"}],
    "Dried fish":     [{"country": "Nigeria",     "demand_growth_pct": 15, "price_premium": "medium"},
                       {"country": "Cote d Ivoire","demand_growth_pct": 12, "price_premium": "medium"},
                       {"country": "Cameroon",    "demand_growth_pct": 10, "price_premium": "medium"}],
    "Pineapple":      [{"country": "EU",          "demand_growth_pct": 8,  "price_premium": "medium"},
                       {"country": "USA",         "demand_growth_pct": 10, "price_premium": "medium"},
                       {"country": "Middle East", "demand_growth_pct": 15, "price_premium": "high"}],
}
