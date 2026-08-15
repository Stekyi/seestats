"""
Customer prospect database for each commodity opportunity.
Sources: GEPA directories, ITC Trade Map, industry research, trade associations.
Prices and volumes are indicative — verify before contacting.
"""

CUSTOMERS = {

    "Shea butter": {
        "direction": "export",
        "description": "Ghana is the world's 2nd largest shea producer. Refined/unrefined shea butter is in high demand for cosmetics and food.",
        "target_markets": [
            {
                "country": "Netherlands",
                "why": "Rotterdam is Europe's largest port. Dutch companies are major shea ingredient buyers for cosmetics.",
                "customers": [
                    {
                        "name": "AAK Netherlands B.V.",
                        "type": "Specialty fats manufacturer — major shea buyer",
                        "website": "https://www.aak.com",
                        "linkedin": "https://www.linkedin.com/company/aak",
                        "address": "Zaandammerplein 6, 1014 GM Amsterdam",
                        "contact_role": "Raw Materials Procurement Manager",
                        "approach": "Email via their supplier registration portal at aak.com. State you are a West African shea supplier seeking preferred supplier status. They buy 500+ MT/year.",
                        "buying_volume_mt": "500+",
                        "price_range_usd_mt": "1,100–1,400 (refined)",
                        "payment_terms": "LC or 30-day net after relationship established",
                        "certifications_required": ["RSPO", "ISO 9001", "HACCP"],
                    },
                    {
                        "name": "Olvea Netherlands",
                        "type": "Vegetable oil importer / oleochemicals",
                        "website": "https://www.olvea.com",
                        "address": "Rotterdam area",
                        "contact_role": "Supply Chain Director",
                        "approach": "Contact via website contact form. Specialises in West African oils and actively sources from Ghana and Burkina Faso.",
                        "buying_volume_mt": "200–500",
                        "price_range_usd_mt": "950–1,200",
                        "payment_terms": "LC",
                        "certifications_required": ["RSPO preferred", "CoA required"],
                    },
                    {
                        "name": "De Wildt Schiedam",
                        "type": "Specialty butters and fats importer",
                        "website": "https://www.dewildt.com",
                        "address": "Schiedam, Netherlands",
                        "contact_role": "Purchasing Manager",
                        "approach": "Specialists in specialty butters. Send 1 kg sample with full product datasheet (FFA%, IV, moisture, colour). They pay premium for high-quality shea.",
                        "buying_volume_mt": "50–200",
                        "price_range_usd_mt": "1,200–1,600 (organic/certified)",
                        "payment_terms": "30% deposit, balance on delivery",
                        "certifications_required": ["CoA", "Organic preferred"],
                    },
                ],
            },
            {
                "country": "France",
                "why": "France is the world's largest cosmetic market. Major luxury brands source shea from West Africa.",
                "customers": [
                    {
                        "name": "Sophim SAS",
                        "type": "Cosmetic ingredient manufacturer",
                        "website": "https://www.sophim.com",
                        "address": "Zone Industrielle, 13300 Salon-de-Provence",
                        "contact_role": "Ingredients Procurement",
                        "approach": "Email their R&D purchasing team. They buy shea for cosmetic-grade fractionation. Require Halal/CoS certification.",
                        "buying_volume_mt": "100–300",
                        "price_range_usd_mt": "1,300–1,800",
                        "certifications_required": ["CoS (Certificate of Suitability)", "COSMOS/ECOCERT preferred"],
                    },
                    {
                        "name": "L'Occitane en Provence",
                        "type": "Premium cosmetics brand — direct sourcing from West Africa",
                        "website": "https://www.loccitane.com",
                        "address": "ZI Saint-Maurice, 04100 Manosque",
                        "contact_role": "Responsible Sourcing Manager",
                        "approach": "L'Occitane runs Fair Trade shea programmes in Burkina Faso and is expanding. Approach via their supplier diversity programme. Pays 20–30% premium for Fair Trade.",
                        "buying_volume_mt": "50–150",
                        "price_range_usd_mt": "1,500–2,200 (Fair Trade premium)",
                        "certifications_required": ["Fair Trade WFTO", "Organic"],
                    },
                ],
            },
            {
                "country": "South Korea",
                "why": "K-beauty boom driving strong demand for natural butters. South Korea imports large volumes of shea.",
                "customers": [
                    {
                        "name": "AMOREPACIFIC Corporation",
                        "type": "Korea's largest cosmetics company (Sulwhasoo, Laneige, Innisfree brands)",
                        "website": "https://www.apgroup.com",
                        "contact_role": "Global Ingredients Procurement",
                        "approach": "Supplier registration via their global procurement portal. Very large buyer — start by contacting their Singapore or Hong Kong regional office.",
                        "buying_volume_mt": "100–500",
                        "price_range_usd_mt": "1,200–1,800",
                        "certifications_required": ["ISO 22000", "CoA", "RSPO preferred"],
                    },
                    {
                        "name": "LG H&H (LG Household & Health Care)",
                        "type": "Major Korean cosmetics conglomerate (The Face Shop, Ohui brands)",
                        "website": "https://www.lghnh.com",
                        "contact_role": "Raw Material Sourcing Team",
                        "approach": "Contact via LinkedIn or their supplier portal. Growing interest in African natural ingredients.",
                        "buying_volume_mt": "50–200",
                        "price_range_usd_mt": "1,200–1,600",
                        "certifications_required": ["CoA", "HACCP"],
                    },
                ],
            },
        ],
        "trade_shows": [
            {"name": "in-cosmetics Global", "location": "Amsterdam / Barcelona", "timing": "April annually", "why": "World's #1 cosmetic ingredients trade show"},
            {"name": "BioFach", "location": "Nuremberg, Germany", "timing": "February annually", "why": "Organic ingredients — premium pricing"},
            {"name": "NYSCC Suppliers Day", "location": "New York, USA", "timing": "May annually", "why": "North American cosmetic ingredient buyers"},
        ],
        "intro_email_template": """Subject: Shea Butter Supply — Premium Quality, Ghana Origin | Sample Available

Dear [Procurement Manager Name],

I am writing from [Your Company Name], a small-scale shea butter producer/exporter based in Ghana.

We produce unrefined/refined shea butter sourced from [Region, e.g., Northern Ghana] women's cooperatives.

**Product Specifications:**
- FFA: <3% (unrefined) / <0.5% (refined)
- Moisture: <0.5%
- Iodine Value: 55–71
- Colour: Ivory/cream
- Packaging: 25 kg drums or bulk flexi-bags

**We offer:**
- Free 1 kg sample for quality assessment
- CIF pricing to Rotterdam / Le Havre from $[X]/MT
- MOQ: 5 MT (sample shipment) → 20 MT (commercial)
- Potential for RSPO and Organic certification (in progress)

We are committed to long-term, transparent partnerships and would welcome a call at your convenience.

Best regards,
[Your Name] | [Company] | [Phone] | [Email]""",
    },

    "Moringa powder": {
        "direction": "export",
        "description": "Moringa is the fastest-growing superfood globally. Ghana has year-round growing conditions and low labour costs.",
        "target_markets": [
            {
                "country": "USA",
                "why": "The US health supplement market is $50B+ annually. Moringa is in the top 20 fastest growing ingredients.",
                "customers": [
                    {
                        "name": "Sunfood Superfoods",
                        "type": "Superfood brand / bulk ingredient buyer",
                        "website": "https://www.sunfood.com",
                        "contact_role": "Sourcing / Procurement Department",
                        "approach": "Email sourcing@sunfood.com with your COA (Certificate of Analysis), heavy metals test results, and 500g sample. They buy organic moringa powder.",
                        "buying_volume_mt": "0.5–5",
                        "price_range_usd_kg": "5–8 (organic certified)",
                        "certifications_required": ["USDA Organic", "COA from accredited lab", "Heavy metals test"],
                    },
                    {
                        "name": "Frontier Co-op",
                        "type": "Organic herb & spice wholesale cooperative (supplies 25,000+ natural food stores)",
                        "website": "https://www.frontiercoop.com",
                        "contact_role": "Supplier Relations",
                        "approach": "Register as a supplier at frontiercoop.com/vendor-application. They require USDA Organic, COA, and minimum 3-year supply commitment.",
                        "buying_volume_mt": "1–10",
                        "price_range_usd_kg": "4–7 (certified)",
                        "certifications_required": ["USDA Organic", "COA", "Pesticide residue test", "Non-GMO"],
                    },
                    {
                        "name": "Starwest Botanicals",
                        "type": "Bulk herbs and botanicals — direct to consumers and manufacturers",
                        "website": "https://www.starwest-botanicals.com",
                        "contact_role": "Purchasing Department",
                        "approach": "Email purchasing@starwest-botanicals.com. They stock moringa leaf powder and are always looking for quality sources. Send COA + 500g sample.",
                        "buying_volume_mt": "1–5",
                        "price_range_usd_kg": "3.50–6",
                        "certifications_required": ["COA", "Heavy metals", "Pesticide screen"],
                    },
                    {
                        "name": "UNFI (United Natural Foods Inc.)",
                        "type": "Largest natural food distributor in North America (30,000+ retail accounts)",
                        "website": "https://www.unfi.com/suppliers",
                        "contact_role": "New Supplier Applications",
                        "approach": "If you can create a branded or private-label moringa product (e.g. '100g Ghana Moringa Powder'), UNFI distributes it to Whole Foods, Sprouts, and health food chains. Apply via supplier portal.",
                        "buying_volume_mt": "5–50 (as distributor)",
                        "price_range_usd_kg": "4–8",
                        "certifications_required": ["USDA Organic preferred", "GMP certified facility", "COA"],
                    },
                ],
            },
            {
                "country": "Germany",
                "why": "Germany is Europe's largest health supplement market. German buyers pay premium for certified organic.",
                "customers": [
                    {
                        "name": "Kräuter Mix GmbH",
                        "type": "German bulk herb importer / private label manufacturer",
                        "website": "https://www.kraeutermix.de",
                        "contact_role": "Raw Material Procurement",
                        "approach": "Email procurement with your EU-format COA and sample. Germany requires EU Organic certification (ECOCERT/Naturland) for organic claims.",
                        "buying_volume_mt": "0.5–3",
                        "price_range_usd_kg": "5–9 (EU Organic)",
                        "certifications_required": ["EU Organic (ECOCERT/Naturland)", "COA", "Aflatoxin test"],
                    },
                    {
                        "name": "BARF-Welt / Organic Africa distributors",
                        "type": "Organic ingredient importer (African origin focus)",
                        "approach": "Several German importers specialise in African organic products. Search 'moringa Importeur Deutschland' on LinkedIn for active buyers.",
                        "buying_volume_mt": "0.2–2",
                        "price_range_usd_kg": "6–10 (premium African organic)",
                        "certifications_required": ["EU Organic", "Fair Trade preferred"],
                    },
                ],
            },
        ],
        "trade_shows": [
            {"name": "Natural Products Expo West", "location": "Anaheim, California, USA", "timing": "March annually", "why": "World's largest natural products trade show — 3,500+ exhibitors"},
            {"name": "BioFach", "location": "Nuremberg, Germany", "timing": "February annually", "why": "World's largest organic food trade show"},
            {"name": "Vitafoods Europe", "location": "Geneva, Switzerland", "timing": "May annually", "why": "Nutraceuticals and health ingredients"},
        ],
        "intro_email_template": """Subject: Premium Moringa Leaf Powder — Ghana, Organic Available | Free Sample

Dear [Name],

I represent [Company], a moringa powder producer in Ghana. We shade-dry and mill certified moringa leaf powder from sustainably managed farms.

**Product Highlights:**
- Moisture: <8% | Protein: >27% | Bright green colour
- Available: Conventional and USDA/EU Organic certified
- Packaging: 1 kg bags, 5 kg bags, 25 kg sacks
- MOQ: 100 kg (trial) | Commercial: 500 kg+

**Quality Documentation:**
- Certificate of Analysis (accredited lab)
- Heavy metals and pesticide residue test
- Aflatoxin test
- Country of Origin: Ghana

We would like to send a FREE 200g sample for your laboratory evaluation.

Please reply with your shipping address and I will arrange delivery within 5 business days.

Best regards,
[Name] | [Company] | [Country: Ghana] | [Email] | [WhatsApp]""",
    },

    "Ginger": {
        "direction": "export",
        "description": "Ghana produces fresh and dried ginger. Global demand is growing, especially for processed ginger in health and food markets.",
        "target_markets": [
            {
                "country": "Germany",
                "why": "Germany is the world's largest ginger importer. Frankfurt/Hamburg are major spice trading hubs.",
                "customers": [
                    {
                        "name": "HAGESUED Interspice GmbH",
                        "type": "Germany's largest spice importer",
                        "website": "https://www.hagesued.de",
                        "address": "Fasanenweg 15, 70771 Leinfelden-Echterdingen",
                        "contact_role": "Raw Material Purchasing",
                        "approach": "One of the top 3 German spice importers. Email their purchasing team with product spec and CIF Hamburg price. They buy ginger in all forms: fresh, split-dried, powder.",
                        "buying_volume_mt": "5–50",
                        "price_range_usd_mt": "800–1,200 (split-dried)",
                        "certifications_required": ["HACCP", "EU MRL pesticide compliance", "Phytosanitary certificate from Ghana"],
                    },
                    {
                        "name": "Fuchs Group",
                        "type": "Major European spice and seasoning producer",
                        "website": "https://www.fuchsgroup.de",
                        "address": "Rote Straße 7, 55543 Bad Kreuznach",
                        "contact_role": "Ingredient Procurement",
                        "approach": "Global spice processor sourcing raw materials. Contact via their supplier portal or procurement email.",
                        "buying_volume_mt": "10–100",
                        "price_range_usd_mt": "850–1,100",
                        "certifications_required": ["FSSC 22000", "HACCP", "Pesticide MRL"],
                    },
                ],
            },
            {
                "country": "USA",
                "why": "US ginger imports are growing 22% annually driven by health food, ginger beer, and supplement demand.",
                "customers": [
                    {
                        "name": "The Ginger People",
                        "type": "Ginger-focused food brand (ginger beer, crystallised ginger, pickled ginger)",
                        "website": "https://www.gingerpeople.com",
                        "contact_role": "Ingredient Sourcing",
                        "approach": "Contact their ingredient team. They source raw ginger globally for various products. Quality and consistency are key.",
                        "buying_volume_mt": "5–20",
                        "price_range_usd_mt": "900–1,400",
                        "certifications_required": ["HACCP", "COA", "Pesticide residue test"],
                    },
                    {
                        "name": "Frontier Co-op",
                        "type": "Organic herbs and spices cooperative buyer",
                        "website": "https://www.frontiercoop.com",
                        "contact_role": "Vendor Relations",
                        "approach": "Register as a vendor. They buy organic dried ginger and ginger powder. USDA Organic certification required.",
                        "buying_volume_mt": "2–10",
                        "price_range_usd_mt": "1,100–1,600 (organic)",
                        "certifications_required": ["USDA Organic", "COA", "Non-GMO"],
                    },
                ],
            },
        ],
        "trade_shows": [
            {"name": "ANUGA", "location": "Cologne, Germany", "timing": "October (odd years)", "why": "World's largest food trade show"},
            {"name": "SIAL Paris", "location": "Paris, France", "timing": "October (even years)", "why": "Major European food ingredient buyers"},
            {"name": "Fancy Food Show", "location": "New York/San Francisco, USA", "timing": "January & June", "why": "Specialty and gourmet food buyers"},
        ],
        "intro_email_template": """Subject: Ghana Ginger Supply — Split-Dried & Powder | CIF Hamburg Quote

Dear [Name],

I am a ginger supplier based in Ghana, exporting split-dried ginger (Zingiber officinale) to European markets.

**Product Specifications:**
- Variety: Ghana yellow/white ginger
- Form: Split-dried, whole-dried, or powder
- Moisture: <12% | Volatile oil: >1.5% | Ash: <5%
- Packaging: 50 kg jute bags or PP bags

**Compliance:**
- Phytosanitary certificate from Ghana Plant Protection
- Pesticide residue analysis (EU MRL compliant)
- HACCP-compliant processing facility

**Pricing:** Indicative CIF Hamburg from $[X]/MT | MOQ: 2 MT (trial) → 5 MT+ commercial

Available for immediate shipment. Free 1 kg sample on request.

Best regards,
[Name] | [Company] | Ghana | [Contact]""",
    },

    "Cashew nuts": {
        "direction": "export",
        "description": "Ghana is Africa's 3rd largest cashew producer. Raw cashew nuts (RCN) are in year-round demand from Indian and Vietnamese processors.",
        "target_markets": [
            {
                "country": "India",
                "why": "India processes 60% of the world's cashew nuts. Mangalore and Kollam are the main processing hubs.",
                "customers": [
                    {
                        "name": "Cashew Export Promotion Council (CEPC) India",
                        "type": "Trade body — provides free directory of Indian RCN importers",
                        "website": "https://www.cashewindia.org",
                        "contact_role": "Secretary General",
                        "approach": "Contact CEPC for their member directory of raw cashew importers. This is the fastest way to find 20+ verified buyers in one step.",
                        "buying_volume_mt": "Directory access",
                        "price_range_usd_mt": "1,000–1,300 (RCN)",
                        "certifications_required": ["Phytosanitary certificate", "Fumigation certificate", "Certificate of Origin"],
                    },
                    {
                        "name": "Agro International (IndiaMART)",
                        "type": "Raw cashew nut processor / bulk importer — Mangalore",
                        "website": "https://www.indiamart.com (search: raw cashew nut importer)",
                        "contact_role": "Proprietor",
                        "approach": "Search IndiaMART for 'raw cashew nut importer Mangalore'. Multiple verified buyers. WhatsApp contact preferred. They buy during Ghana's March-June harvest season.",
                        "buying_volume_mt": "20–500",
                        "price_range_usd_mt": "1,050–1,250",
                        "certifications_required": ["Phytosanitary", "Fumigation", "Weight certificate"],
                    },
                ],
            },
            {
                "country": "Vietnam",
                "why": "Vietnam processes 35% of world cashew. They actively seek West African RCN suppliers.",
                "customers": [
                    {
                        "name": "Vinacas (Vietnam Cashew Association)",
                        "type": "Trade association — connects to 200+ Vietnamese cashew processors",
                        "website": "https://www.vinacas.com.vn",
                        "contact_role": "Trade Relations Office",
                        "approach": "One email to Vinacas can connect you with 20+ Vietnamese buyers simultaneously. This is the most efficient entry point for Vietnam.",
                        "buying_volume_mt": "50–500+",
                        "price_range_usd_mt": "1,000–1,200",
                        "certifications_required": ["Phytosanitary", "Weight/quality certificate"],
                    },
                ],
            },
        ],
        "trade_shows": [
            {"name": "World Cashew Convention", "location": "Rotating (Dubai, Singapore, India)", "timing": "Annual", "why": "The only dedicated global cashew industry event"},
            {"name": "Gulfood", "location": "Dubai, UAE", "timing": "February annually", "why": "Middle East and global food buyers"},
        ],
        "intro_email_template": """Subject: Ghana Raw Cashew Nuts (RCN) — 2026 Crop | CIF Chennai/Ho Chi Minh

Dear [Name],

I am a cashew exporter from Ghana offering raw cashew nuts (RCN) from the 2026 harvest (March–June season).

**Product Details:**
- Origin: Ghana (Brong-Ahafo / Volta / Eastern regions)
- KOR (Kernel Out-turn Ratio): 48–52 lbs
- Moisture: <10%
- Admixture: <2%
- Packaging: 80 kg jute bags

**Logistics:**
- Nearest port: Tema, Ghana
- Shipping: CIF Chennai or Ho Chi Minh City
- MOQ: 1 x 20ft container (~18 MT)
- Payment: LC at sight preferred

Available for pre-harvest contracts (December–February) for preferential pricing.

Phytosanitary and fumigation certificates provided.

Best regards,
[Name] | [Company] | Ghana | [Contact]""",
    },

    "Rice": {
        "direction": "import",
        "description": "Ghana imports $487M of rice annually — the #1 food import. Distribution from port to wholesale/retail is the business model.",
        "buyers_in_ghana": [
            {
                "name": "Agbogbloshie Market — Grain Section",
                "type": "Ghana's largest wholesale food market",
                "address": "Agbogbloshie, Accra (near Abossey Okai)",
                "contact_role": "Chief grain traders / market women leaders",
                "approach": "Visit in person on a weekday morning (6am–10am). Introduce yourself as a rice importer. Market leaders ('queen mothers') control bulk buying. Offer competitive price and consistent delivery. These traders buy 50–500 bags per week.",
                "buying_volume": "50–500 bags/week (50 kg bags)",
                "payment_terms": "Cash on delivery or 7-day credit after trust established",
            },
            {
                "name": "Kumasi Central Market (Kejetia)",
                "type": "Ashanti region's main wholesale hub",
                "address": "Kejetia, Kumasi",
                "contact_role": "Grain section traders",
                "approach": "Second largest rice market in Ghana. Good for Ashanti regional distribution. Visit in person. Complement Accra distribution with a Kumasi partner.",
                "buying_volume": "30–300 bags/week",
                "payment_terms": "Cash preferred",
            },
            {
                "name": "Maxmart Supermarkets",
                "type": "Modern retail chain",
                "address": "Multiple Accra locations (Spintex, Airport, Tema)",
                "website": "https://www.maxmart.com.gh",
                "contact_role": "Category Buyer — Grocery/Dry Goods",
                "approach": "Contact buying department. They need branded, packaged rice. Offer private-label packaging (your brand on 2 kg, 5 kg bags). Requires consistent weekly delivery of 2–5 MT.",
                "buying_volume": "2–10 MT/week",
                "payment_terms": "30-day invoice",
            },
            {
                "name": "Palace Hypermarket / Shoprite Ghana",
                "type": "Modern retail hypermarket",
                "address": "Accra Mall, West Hills Mall",
                "contact_role": "Procurement Manager — Fresh & Grocery",
                "approach": "Requires: supplier registration, food safety certification, consistent supply, and invoicing capability. Target initially as a backup/overflow supplier while building volume.",
                "buying_volume": "5–20 MT/week",
                "payment_terms": "30–60 day invoice",
            },
            {
                "name": "Finatrade Ghana Ltd",
                "type": "One of Ghana's largest rice importers and distributors",
                "address": "Ring Road Central, Accra",
                "contact_role": "Sales Manager",
                "approach": "They are a competitor but also a potential off-taker if you import a variety they don't carry. Alternatively, approach as a regional sub-distributor (carry their rice for a district/region).",
                "buying_volume": "Large volume — partnership model",
                "payment_terms": "Varies",
            },
        ],
        "suppliers": [
            {
                "name": "India Rice Exporters Council (IREC)",
                "country": "India",
                "website": "https://www.irec.in",
                "approach": "Find IREC-certified rice exporters who ship to West Africa. India is cheapest source for parboiled rice ($290/MT CIF Tema).",
            },
            {
                "name": "Vietnam Food Association (VFA)",
                "country": "Vietnam",
                "website": "https://www.vietfood.org.vn",
                "approach": "VFA members export fragrant and parboiled varieties. Good for premium market positioning.",
            },
        ],
        "intro_email_template": """[For approaching Ghana buyers]
Subject: Rice Supply Partnership — Competitive Pricing, Consistent Delivery

Dear [Name / Market Leader],

I am establishing a rice import business in Ghana and looking for reliable wholesale buyers to partner with.

I import:
- Parboiled long grain rice (India origin, 50 kg bags)
- Price: GHC [X] per bag (competitive, below current market rate)
- Minimum first order: 50 bags
- Delivery: Tema → Your location within 48 hours of order

I am specifically looking for traders who buy regularly (weekly or bi-weekly) to build a long-term supply relationship.

I would like to visit you personally to discuss. When would be a convenient time?

Regards,
[Name] | [Phone/WhatsApp]""",
    },

    "Poultry": {
        "direction": "import",
        "description": "Ghana imports $281M of frozen poultry annually. Institutional buyers (hotels, fast food, hospitals) pay premium for consistent cold-chain supply.",
        "buyers_in_ghana": [
            {
                "name": "KFC Ghana / Chicken Republic",
                "type": "Fast food chains — institutional buyer",
                "address": "Multiple Accra/Kumasi locations",
                "contact_role": "Supply Chain Manager Ghana",
                "approach": "Fast food chains need certified suppliers. Contact their Ghana operations manager. They pay premium for consistency. Requires: halal certification, cold chain, regular delivery.",
                "buying_volume": "200–500 kg/week per restaurant",
                "payment_terms": "30-day invoice",
            },
            {
                "name": "Marriott Accra / Holiday Inn / Movenpick",
                "type": "5-star hotels — weekly institutional buyers",
                "address": "Airport Residential, Accra",
                "contact_role": "Food & Beverage Purchasing Manager",
                "approach": "Hotels pay 15–25% above market for consistent quality and cold-chain delivery. Email F&B manager. Offer a free sample delivery for evaluation.",
                "buying_volume": "100–300 kg/week per hotel",
                "payment_terms": "30-day invoice",
            },
            {
                "name": "Accra Central Cold Store (Kantamanto)",
                "type": "Frozen foods wholesale market",
                "address": "Kantamanto Market, Accra Central",
                "contact_role": "Section traders (direct approach)",
                "approach": "The biggest frozen meat market in Accra. Approach traders directly, introduce yourself as an importer. They buy weekly. Relationship-based — visit several times before a deal.",
                "buying_volume": "50–500 kg/week",
                "payment_terms": "Cash on delivery",
            },
            {
                "name": "Tema General Hospital / KATH",
                "type": "Public hospitals — institutional buyer",
                "address": "Tema / Kumasi",
                "contact_role": "Procurement Officer",
                "approach": "Public hospitals procure via tender. Register as a supplier with Ghana Health Service and bid on tenders. Lower price sensitivity, payment via government cheque.",
                "buying_volume": "100–500 kg/week",
                "payment_terms": "30–90 day government invoice",
            },
        ],
        "suppliers": [
            {
                "name": "BRF S.A. (Sadia / Perdigão brands)",
                "country": "Brazil",
                "website": "https://www.brf-global.com",
                "approach": "World's largest poultry exporter. Contact their West Africa regional office (Lagos). They work with registered importers. Minimum 1 x 40ft reefer container.",
            },
            {
                "name": "USAPEEC (USA Poultry & Egg Export Council)",
                "country": "USA",
                "website": "https://www.usapeec.org",
                "approach": "Free directory of US poultry exporters approved for Ghana. Contact USAPEEC for a buyer-supplier match.",
            },
        ],
        "intro_email_template": """[For approaching Ghana institutional buyers]
Subject: Frozen Poultry Supply — Reliable Cold Chain, Halal Certified

Dear [Name],

I am establishing a frozen poultry import and distribution business in Ghana.

**What I offer:**
- Whole frozen chicken, drumsticks, thighs, wings (Brazilian origin, Sadia/BRF certified)
- Halal certified, cold-chain maintained from Tema port to delivery
- Price: GHC [X]/kg (10% below current market rate for first order)
- Minimum first order: 200 kg
- Delivery: Refrigerated vehicle directly to your kitchen/store

I would like to offer a **trial delivery of 50 kg at no cost** so you can assess quality before committing.

May I call to arrange a brief meeting?

Regards,
[Name] | [Company] | [WhatsApp]""",
    },
}
