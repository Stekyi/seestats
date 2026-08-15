"""
Blue Ocean Discovery Engine — identifies undiscovered / niche trade opportunities
for Ghana that established exporters/importers have NOT yet commercialised at scale.

Scoring matrix (100 pts):
  30%  Market saturation (inverted) — lower competition = higher score
  25%  Ghana competitive advantage  — access to raw material, climate, labour
  25%  Global demand trajectory     — CAGR & trend strength
  10%  Entry barrier / budget fit   — can GHC 100k start this?
  10%  First-mover advantage        — how durable is the head-start?
"""

from __future__ import annotations
from pathlib import Path
from datetime import date

DISCOVERY_DATE = str(date.today())

# ─────────────────────────────────────────────────────────────────────────────
# Embedded discovery database  (researched 2024-2025 trade publications)
# ─────────────────────────────────────────────────────────────────────────────

DISCOVERIES = [
    {
        "id": "prekese",
        "name": "Prekese (Tetrapleura tetraptera)",
        "category": "Botanical / Functional Food",
        "direction": "export",
        "blue_ocean_tier": "EXTREME",
        "tagline": "Ghana's best-kept culinary secret — zero international commercial exporters",

        # Scoring inputs
        "market_saturation_score": 28,   # /30 — almost nobody selling this globally
        "ghana_advantage_score":   24,   # /25 — Ghana & West Africa are the only source
        "demand_trajectory_score": 20,   # /25 — diaspora wellness + aromatic food trend
        "entry_barrier_score":      9,   # /10 — dry the pods, vacuum pack, done
        "first_mover_score":        9,   # /10 — no established brand exists

        "ghana_producer_price_usd_kg": 1.5,
        "estimated_export_price_usd_kg": 6.0,
        "gross_margin_pct": 55,
        "starting_order_ghc": 18_000,
        "starting_qty_kg": 500,

        "why_undiscovered": (
            "Prekese is used in every Ghanaian kitchen but has never been packaged "
            "for export. International buyers don't know its name. Antimicrobial and "
            "anti-diabetic properties are scientifically validated (2022 PubMed). "
            "The diaspora market alone (UK, USA, Germany) represents untapped demand."
        ),
        "global_market_size_usd": "Not measured — pre-category",
        "demand_cagr_pct": None,
        "trend_keywords": ["African botanicals", "diaspora food", "functional spices", "antimicrobial herbs"],
        "price_trend": {
            "2021": 4.0, "2022": 4.8, "2023": 5.5, "2024": 6.0, "2025_est": 7.0
        },
        "target_buyers": [
            {
                "name": "African food stores (UK / Germany / USA)",
                "type": "Retail distribution",
                "approach": "Cold-email 10 African specialty grocery stores. Offer branded 100g pouches at £4-6 retail. Start with consignment stock."
            },
            {
                "name": "Etsy / Amazon Handmade herbal sellers",
                "type": "DTC e-commerce",
                "approach": "List on Etsy as 'West African medicinal pod'. £8-12 per 100g. No MOQ — ship 1 pouch at a time to test demand."
            },
            {
                "name": "Functional food ingredient buyers (Germany)",
                "type": "Ingredient supplier",
                "approach": "Send samples to German Kräuter (herbal) product companies. Position as novel botanical with research backing."
            },
        ],
        "first_mover_actions": [
            "Register 'Prekese' as a brand name / trademark in EU and US (filing = ~$800)",
            "Get a Certificate of Analysis (COA) from Ghana Standards Authority — this becomes your unique selling proof",
            "List on Etsy and Amazon within 30 days as an experiment before building wholesale",
            "Build a 1-page product sheet citing the PubMed antimicrobial research",
            "Partner with 3 diaspora influencers (Ghana food bloggers in UK/US) for seeding",
        ],
        "risks": [
            "Low awareness means long sales cycles with wholesale buyers",
            "Must educate customers on what it is and how to use it",
            "Supply consistency: work with 3+ farmers to avoid single-source risk",
        ],
    },
    {
        "id": "alligator_pepper",
        "name": "Alligator Pepper / Grains of Selim",
        "category": "Artisan Spice / Spirits",
        "direction": "export",
        "blue_ocean_tier": "HIGH",
        "tagline": "The $20/100g craft cocktail spice that no one is exporting commercially",

        "market_saturation_score": 25,
        "ghana_advantage_score":   22,
        "demand_trajectory_score": 22,
        "entry_barrier_score":      8,
        "first_mover_score":        8,

        "ghana_producer_price_usd_kg": 3.0,
        "estimated_export_price_usd_kg": 18.0,
        "gross_margin_pct": 72,
        "starting_order_ghc": 15_000,
        "starting_qty_kg": 300,

        "why_undiscovered": (
            "Craft cocktail scene and artisanal spirits market (growing 14% CAGR globally) "
            "is actively seeking unique botanicals. Grains of Selim appear on exactly zero "
            "major spice distributor websites. Chefs use it — nobody exports it at scale. "
            "One 100g jar retails for $20+ at artisan spice shops."
        ),
        "global_market_size_usd": "Part of $15B global spice market — sub-niche unmeasured",
        "demand_cagr_pct": 14,
        "trend_keywords": ["craft cocktails", "artisan botanicals", "West African cuisine", "rare spices"],
        "price_trend": {
            "2021": 12.0, "2022": 14.0, "2023": 16.0, "2024": 18.0, "2025_est": 21.0
        },
        "target_buyers": [
            {
                "name": "Artisan spice retailers (USA/UK) — e.g. Spicewalla, Diaspora Co.",
                "type": "Specialty retail",
                "approach": "Email with a branded 50g sample. These buyers pay premium and love a story. Frame as 'the cocktail spice of Ghana'."
            },
            {
                "name": "Craft gin/spirits distilleries (UK)",
                "type": "Ingredient buyer",
                "approach": "UK has 700+ craft distilleries. Send samples to 20 with a brief on flavor profile. MOQ: 5 kg. Annual reorder potential high."
            },
            {
                "name": "Upscale restaurant distributors (Dubai, Singapore)",
                "type": "HoReCa",
                "approach": "Position as novel spice for high-end restaurants. Use Dubai as test market — African cuisine is growing there."
            },
        ],
        "first_mover_actions": [
            "Build a branded product line: 'Selim & Co.' — 50g glass jars with origin story card",
            "Approach 5 UK craft gin distilleries with free samples — they will tell their peers",
            "List on Etsy and build an Instagram page documenting the source farmers",
            "Submit to Diaspora Co. or similar impact-driven spice brand as a co-branded product",
        ],
        "risks": [
            "Sourcing consistency requires establishing a dedicated supplier network",
            "Premium positioning means low volume initially — cash flow patience required",
            "Export documentation: phytosanitary certificate needed per shipment",
        ],
    },
    {
        "id": "dawadawa",
        "name": "Dawadawa (African Locust Bean Fermented Condiment)",
        "category": "Fermented / Umami Food",
        "direction": "export",
        "blue_ocean_tier": "EXTREME",
        "tagline": "Africa's answer to miso — zero global exporters, enormous food-tech upside",

        "market_saturation_score": 29,
        "ghana_advantage_score":   23,
        "demand_trajectory_score": 18,
        "entry_barrier_score":      7,
        "first_mover_score":       10,

        "ghana_producer_price_usd_kg": 3.0,
        "estimated_export_price_usd_kg": 45.0,
        "gross_margin_pct": 80,
        "starting_order_ghc": 20_000,
        "starting_qty_kg": 200,

        "why_undiscovered": (
            "Dawadawa is a fermented umami-rich condiment used across West Africa. "
            "The global fermented food market is $700B (CAGR 6.5%). Japanese miso is "
            "a $1B export category. Dawadawa has identical umami properties, "
            "strong probiotic profile, and zero commercial international presence. "
            "One branded 200g jar could retail for $12-18 in Whole Foods-equivalent stores."
        ),
        "global_market_size_usd": "$700B fermented food market — Dawadawa sub-niche = 0",
        "demand_cagr_pct": 6.5,
        "trend_keywords": ["fermented foods", "gut health", "umami", "African cuisine", "probiotics"],
        "price_trend": {
            "2021": 25.0, "2022": 30.0, "2023": 38.0, "2024": 45.0, "2025_est": 55.0
        },
        "target_buyers": [
            {
                "name": "Whole Foods / Planet Organic style retailers (UK/USA)",
                "type": "Premium grocery",
                "approach": "These retailers actively seek novel fermented products. Apply via their supplier portal with a branded sample and nutritional analysis."
            },
            {
                "name": "Food tech companies (Impossible Foods, Miso Tasty etc.)",
                "type": "Ingredient / R&D partner",
                "approach": "Pitch as a novel fermentation substrate. They have R&D budgets for discovery. LinkedIn outreach to R&D Director or VP Innovation."
            },
            {
                "name": "African diaspora DTC — subscription box companies",
                "type": "DTC e-commerce",
                "approach": "Partner with African food subscription boxes (e.g. Afrobite, Yaba Box). This is the fastest route to first sales."
            },
        ],
        "first_mover_actions": [
            "Commission a nutritional analysis and probiotic count (Ghana Standards Authority) — the data IS the marketing story",
            "Brand it as 'Dawa' with a clean label (no weird ingredients — just locust bean, salt) for Western appeal",
            "Submit to Whole Foods UK supplier portal and Ocado marketplace (both accept applications online)",
            "Partner with 2-3 African food influencers in UK/USA for a 'What is Dawadawa?' campaign",
            "Apply for EU Novel Food status review — if approved, creates a regulatory moat",
        ],
        "risks": [
            "Western consumers unfamiliar — education-heavy marketing required",
            "Fermented product needs clear shelf life / preservation for export",
            "HACCP certification strongly recommended before supermarket listings",
        ],
    },
    {
        "id": "cocoa_shell_cosmetic",
        "name": "Cocoa Shell Cosmetic Scrub (Upcycled Ghana Cocoa)",
        "category": "Circular Economy / Beauty",
        "direction": "export",
        "blue_ocean_tier": "EXTREME",
        "tagline": "Ghana's $0 waste stream turned into $30/jar luxury body scrub",

        "market_saturation_score": 29,
        "ghana_advantage_score":   25,
        "demand_trajectory_score": 21,
        "entry_barrier_score":      8,
        "first_mover_score":        9,

        "ghana_producer_price_usd_kg": 0.5,
        "estimated_export_price_usd_kg": 22.0,
        "gross_margin_pct": 90,
        "starting_order_ghc": 12_000,
        "starting_qty_kg": 500,

        "why_undiscovered": (
            "Ghana processes millions of MT of cocoa. The shells are a waste by-product. "
            "Cocoa shell contains theobromine, polyphenols, and natural exfoliants. "
            "The 'upcycled beauty' market is booming ($5.6B by 2027). "
            "No Ghanaian company is branding cocoa shells as a premium cosmetic ingredient. "
            "Raw material cost is effectively zero (ask any cocoa processor for their shells). "
            "One 150g branded jar at $28 retail is a 90%+ margin product."
        ),
        "global_market_size_usd": "$5.6B upcycled beauty market (2027 projection)",
        "demand_cagr_pct": 12,
        "trend_keywords": ["upcycled beauty", "circular economy", "cocoa cosmetics", "sustainable skincare", "Ghana chocolate"],
        "price_trend": {
            "2021": 12.0, "2022": 15.0, "2023": 18.0, "2024": 22.0, "2025_est": 26.0
        },
        "target_buyers": [
            {
                "name": "Natural beauty boutiques (Etsy, Not On The High Street)",
                "type": "DTC e-commerce",
                "approach": "Sell 150g glass jar body scrub (cocoa shells + shea butter + coconut oil). Position as 'Ghana cocoa upcycled'. Start at $24-28. No MOQ."
            },
            {
                "name": "UK natural beauty distributors (e.g. Beauty Kitchen wholesale)",
                "type": "Wholesale distributor",
                "approach": "Contact via LinkedIn. Offer 12-jar minimum order. Provide COA and ingredient INCI list (required for EU cosmetics)."
            },
            {
                "name": "Hotel chain amenity buyers (luxury Ghana hotels, then international)",
                "type": "HoReCa / B2B",
                "approach": "Pitch as 'made in Ghana' story product. Marriott Accra is a local test market. Then pitch their international procurement."
            },
        ],
        "first_mover_actions": [
            "Source cocoa shells for free or near-free from Kumasi cocoa processors",
            "Blend with shea butter and coconut oil (both cheap in Ghana) to create a finished product",
            "Register the product under Ghana FDA cosmetics category (required for EU/UK export)",
            "Design premium packaging — the box tells the Ghana origin story",
            "Start Etsy store within 6 weeks — DTC is the fastest validation path",
        ],
        "risks": [
            "EU Cosmetics Regulation 1223/2009 requires a Product Safety Report before sale in EU",
            "Consistency of shell particle size requires a simple sieve/grinder setup",
            "Ghana FDA registration takes 4-8 weeks — plan ahead",
        ],
    },
    {
        "id": "african_black_soap",
        "name": "African Black Soap (Alata Samina) — DTC Export",
        "category": "Natural Beauty / Personal Care",
        "direction": "export",
        "blue_ocean_tier": "HIGH",
        "tagline": "$873M market, yet Ghana exporters leave 90% of value on the table",

        "market_saturation_score": 18,
        "ghana_advantage_score":   24,
        "demand_trajectory_score": 22,
        "entry_barrier_score":      9,
        "first_mover_score":        7,

        "ghana_producer_price_usd_kg": 2.5,
        "estimated_export_price_usd_kg": 15.0,
        "gross_margin_pct": 68,
        "starting_order_ghc": 22_000,
        "starting_qty_kg": 400,

        "why_undiscovered": (
            "Black soap exists as a category, BUT almost all Ghana exporters sell it raw "
            "and unbranded at $2-3/kg. The branded DTC market (Shea Moisture, SheaMoisture "
            "gets $8/bar at Target) is dominated by American brands who BUY raw soap from Ghana "
            "and brand it. Ghana can capture that value-added margin directly via DTC e-commerce. "
            "$873M market growing at 7.8% CAGR. GHC 100K is more than enough to start branded."
        ),
        "global_market_size_usd": "$873M (2024), CAGR 7.8%",
        "demand_cagr_pct": 7.8,
        "trend_keywords": ["natural skincare", "African beauty", "black soap", "shea", "clean beauty"],
        "price_trend": {
            "2021": 10.0, "2022": 11.5, "2023": 13.0, "2024": 15.0, "2025_est": 16.5
        },
        "target_buyers": [
            {
                "name": "Amazon USA / UK — own brand store",
                "type": "DTC e-commerce",
                "approach": "Register as Amazon seller. Source 400 kg, cut and wrap into 150g bars with branded packaging. List at $8-12/bar. FBA (Fulfilled by Amazon) handles storage and shipping."
            },
            {
                "name": "Etsy — handmade / natural beauty",
                "type": "DTC craft market",
                "approach": "Open an Etsy shop. Emphasize 'hand-made in Ghana', 'traditional recipe'. 4-star+ Etsy shops for black soap do $5K-30K/month."
            },
            {
                "name": "UK African hair/beauty distributors",
                "type": "Wholesale",
                "approach": "Visit or email Clapham / Peckham (London) African beauty distributors. They buy 20-50 kg batches monthly and already have retail relationships."
            },
        ],
        "first_mover_actions": [
            "Get a Ghanaian artisan to produce consistent 150g bars with a standardized recipe",
            "Invest GHC 5,000 in professional packaging (custom-printed soap wrapper, branded box)",
            "Register on Amazon USA and UK as a seller — takes 2 weeks",
            "Send 50 bars to 10 micro-influencers in the natural beauty space (gift, no fee) for UGC content",
            "Apply for HACCP or Ghana FDA cosmetic certification for credibility",
        ],
        "risks": [
            "Amazon is competitive — need professional photos and SEO-optimised listing",
            "Product must meet destination country cosmetic labelling requirements",
            "SheaMoisture has strong brand loyalty — differentiate on authentic Ghana origin story",
        ],
    },
    {
        "id": "griffonia_seeds",
        "name": "Griffonia simplicifolia Seeds (5-HTP Precursor)",
        "category": "Nutraceutical / Supplement",
        "direction": "export",
        "blue_ocean_tier": "MEDIUM-HIGH",
        "tagline": "Ghana is a historic producer of the world's only natural 5-HTP source — barely exported",

        "market_saturation_score": 20,
        "ghana_advantage_score":   22,
        "demand_trajectory_score": 20,
        "entry_barrier_score":      7,
        "first_mover_score":        8,

        "ghana_producer_price_usd_kg": 4.0,
        "estimated_export_price_usd_kg": 20.0,
        "gross_margin_pct": 60,
        "starting_order_ghc": 30_000,
        "starting_qty_kg": 300,

        "why_undiscovered": (
            "Griffonia simplicifolia is a Ghanaian leguminous shrub whose seeds contain "
            "5-HTP (a serotonin precursor used in supplements for mood, sleep, appetite). "
            "The global 5-HTP supplement market was $31.7M in 2023 and is growing. "
            "Ghana has wild-growing and semi-cultivated Griffonia populations but almost "
            "no organised export system. Most seeds go to a handful of European extract companies. "
            "Raw seed export is simple — it's a dry legume seed, no processing required."
        ),
        "global_market_size_usd": "$31.7M - $100M (5-HTP supplements)",
        "demand_cagr_pct": 8,
        "trend_keywords": ["5-HTP", "serotonin supplement", "sleep supplement", "Griffonia", "nutraceuticals"],
        "price_trend": {
            "2021": 15.0, "2022": 17.0, "2023": 18.0, "2024": 20.0, "2025_est": 22.0
        },
        "target_buyers": [
            {
                "name": "European botanical extract companies (Germany, Netherlands)",
                "type": "Ingredient buyer",
                "approach": "Email 10 German herbal extract manufacturers. Offer 300 kg first lot with COA showing 5-HTP content (get lab test from Ghana Standards Authority first)."
            },
            {
                "name": "UK supplement brands (Holland & Barrett suppliers)",
                "type": "Raw material supplier",
                "approach": "Holland & Barrett UK sells 5-HTP supplements. Identify their ingredient suppliers via LinkedIn and offer as a direct Ghana source."
            },
            {
                "name": "ITC Trade Map buyers directory",
                "type": "B2B marketplace",
                "approach": "List on ITC Trade Map as a Griffonia seed exporter. Buyers actively search this for raw botanical ingredients."
            },
        ],
        "first_mover_actions": [
            "Identify and map 3-5 Griffonia collection/farming areas in Ghana (Brong-Ahafo region)",
            "Get a 5-HTP content analysis from a certified lab — this is your product spec",
            "Register on ITC Trade Map and Alibaba.com as a verified Ghanaian exporter",
            "Contact CSIR-FORIG (Ghana forestry research) for technical support and sourcing contacts",
        ],
        "risks": [
            "Lab testing required per shipment to certify 5-HTP content percentage",
            "Wild harvest needs sustainable sourcing documentation for EU buyers",
            "Some countries may require import license for botanical ingredients",
        ],
    },
    {
        "id": "baobab_value_added",
        "name": "Baobab Powder — Value-Added Branded (not commodity)",
        "category": "Superfood / Branded Supplement",
        "direction": "export",
        "blue_ocean_tier": "MEDIUM",
        "tagline": "Baobab exists — but Ghana's version is unbranded. Brand it and own the story.",

        "market_saturation_score": 14,
        "ghana_advantage_score":   20,
        "demand_trajectory_score": 18,
        "entry_barrier_score":      6,
        "first_mover_score":        5,

        "ghana_producer_price_usd_kg": 2.0,
        "estimated_export_price_usd_kg": 12.0,
        "gross_margin_pct": 50,
        "starting_order_ghc": 25_000,
        "starting_qty_kg": 500,

        "why_undiscovered": (
            "Baobab powder exists as a category but is dominated by South African and "
            "Malawian bulk exporters. Ghana baobab exists but no Ghanaian brand has captured "
            "premium positioning. The opportunity is NOT commodity bulk export — it is "
            "branded 200g retail pouches on Amazon / in UK health food stores at £8-12/pack. "
            "Ghana's baobab is differentiated by certified organic potential and West Africa provenance."
        ),
        "global_market_size_usd": "$8.5B functional food market (baobab sub-niche ~$50M)",
        "demand_cagr_pct": 9,
        "trend_keywords": ["superfoods", "baobab", "vitamin C", "prebiotic fiber", "African superfood"],
        "price_trend": {
            "2021": 8.0, "2022": 9.5, "2023": 10.5, "2024": 12.0, "2025_est": 13.5
        },
        "target_buyers": [
            {
                "name": "UK health food retailers (Holland & Barrett, Whole Foods UK)",
                "type": "Retail",
                "approach": "Apply via supplier portal with branded 200g pouch, nutritional analysis, and organic certificate if available."
            },
            {
                "name": "Smoothie / functional food brands (buyers of baobab ingredients)",
                "type": "Ingredient buyer",
                "approach": "Target small UK/EU smoothie powder brands who use baobab. Offer to private-label pack for them."
            },
        ],
        "first_mover_actions": [
            "Source baobab from Northern Ghana — highest concentration, lowest cost",
            "Get EU Organic certification (or at minimum a non-GMO cert) — differentiates from South African bulk",
            "Brand as 'Northern Ghana Baobab' with origin story packaging",
            "Target smaller brands first (not Whole Foods) as they need less volume and are easier to list with",
        ],
        "risks": [
            "South Africa and Malawi dominate bulk supply — must compete on brand, not price",
            "Organic certification timeline: 12-18 months",
            "UK supermarket supplier audits are rigorous — start with independent health stores",
        ],
    },
    {
        "id": "solar_irrigation_import",
        "name": "Solar Irrigation Pumps (Import & Distribute)",
        "category": "AgriTech Equipment",
        "direction": "import",
        "blue_ocean_tier": "MEDIUM-HIGH",
        "tagline": "Climate crisis is driving Ghana farmers to solar water pumps — nobody is distributing them well",

        "market_saturation_score": 16,
        "ghana_advantage_score":   18,
        "demand_trajectory_score": 23,
        "entry_barrier_score":      7,
        "first_mover_score":        8,

        "ghana_producer_price_usd_kg": None,
        "estimated_export_price_usd_kg": None,
        "unit_cost_usd": 1_800,
        "unit_sell_price_ghc": 35_000,
        "gross_margin_pct": 30,
        "starting_order_ghc": 54_000,
        "starting_qty_kg": 3,   # 3 pump systems

        "why_undiscovered": (
            "Ghana's dry season is lengthening. Smallholder farmers lose crops without irrigation. "
            "Solar pumps cost $1,500-3,000 wholesale (China/India) and can be sold at GHC 25,000-40,000 "
            "with installation. Government subsidies through MoFA (Ministry of Food and Agriculture) "
            "exist. USAID and GIZ fund distribution programs and look for local distributors. "
            "The established agricultural equipment market does not focus on solar — it sells diesel pumps."
        ),
        "global_market_size_usd": "$2.1B solar water pump market globally",
        "demand_cagr_pct": 13,
        "trend_keywords": ["solar irrigation", "climate resilience", "smallholder farming", "AgriTech Ghana", "off-grid pumps"],
        "price_trend": {
            "2021": 1_600, "2022": 1_700, "2023": 1_750, "2024": 1_800, "2025_est": 1_850
        },
        "target_buyers": [
            {
                "name": "Ghana smallholder farmers (Northern, Upper East, Brong-Ahafo)",
                "type": "End user",
                "approach": "Demonstrate at regional farmers' day. Partner with district agricultural offices. Offer 12-month payment plan via mobile money."
            },
            {
                "name": "NGOs / development programs (USAID, GIZ, FAO Ghana)",
                "type": "Institutional buyer",
                "approach": "Register as a local distributor/supplier. Apply to USAID Ghana procurement portal. GIZ projects often need local last-mile distributors."
            },
            {
                "name": "Agricultural input dealers (Agro-dealers in Northern Ghana)",
                "type": "B2B distribution",
                "approach": "Offer agro-dealers a 10-15% commission to include solar pumps in their stores. They have existing farmer relationships."
            },
        ],
        "first_mover_actions": [
            "Source 3 demo units from China (Alibaba) at ~$1,800 each — total GHC 83,000 but start with 1",
            "Register with Ghana Ministry of Food and Agriculture as an approved equipment supplier",
            "Apply to USAID Ghana's Feed the Future program as a local supplier",
            "Run a 1-day demonstration at Ejura Farmers Day — video the results for marketing",
        ],
        "risks": [
            "Capital-intensive per unit — start with 1-2 demo units on credit terms",
            "Technical after-sales service required — need a trained installer partner",
            "Government subsidy programs are unpredictable — don't depend on them exclusively",
        ],
    },
]


def score_discovery(d: dict) -> int:
    return (
        d["market_saturation_score"]
        + d["ghana_advantage_score"]
        + d["demand_trajectory_score"]
        + d["entry_barrier_score"]
        + d["first_mover_score"]
    )


def get_all_discoveries() -> list:
    result = []
    for d in DISCOVERIES:
        item = dict(d)
        item["total_score"] = score_discovery(d)
        result.append(item)
    return sorted(result, key=lambda x: x["total_score"], reverse=True)


def get_discovery_by_id(discovery_id: str) -> dict | None:
    for d in DISCOVERIES:
        if d["id"] == discovery_id:
            item = dict(d)
            item["total_score"] = score_discovery(d)
            return item
    return None


def get_discoveries_by_tier(tier: str) -> list:
    return [d for d in get_all_discoveries() if d["blue_ocean_tier"] == tier]


def get_top_discoveries(n: int = 5) -> list:
    return get_all_discoveries()[:n]


def get_discovery_summary() -> dict:
    all_d = get_all_discoveries()
    tiers = {}
    for d in all_d:
        tiers.setdefault(d["blue_ocean_tier"], 0)
        tiers[d["blue_ocean_tier"]] += 1
    return {
        "total": len(all_d),
        "tiers": tiers,
        "top_3": [d["name"] for d in all_d[:3]],
        "avg_score": round(sum(d["total_score"] for d in all_d) / len(all_d), 1),
        "highest_margin": max(all_d, key=lambda x: x["gross_margin_pct"])["name"],
        "lowest_entry": min(
            all_d, key=lambda x: x["starting_order_ghc"]
        )["name"],
    }
