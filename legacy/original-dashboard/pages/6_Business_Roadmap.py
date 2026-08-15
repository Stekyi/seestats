"""
Business Roadmap — Step-by-step execution guide grounded in Weiss + Bade methodology.
Specific to each commodity found by the analysis.
"""
import sys
import streamlit as st
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import page_header

st.set_page_config(page_title="Business Roadmap", page_icon="🗺️", layout="wide")
analysis = page_header("🗺️ Business Roadmap", "How to turn data into a real business — commodity by commodity")

st.info("""
**Weiss Core Law #1:** Find a buyer BEFORE you buy inventory.
**Weiss Core Law #2:** Maintain ≥20% gross margin after ALL landed costs.
**Bade Principle:** Document every transaction meticulously — your paper trail IS your business.
""")

top5 = analysis.get("top_5_overall", [])
export_opps = analysis.get("export_opportunities", [])
import_opps = analysis.get("import_opportunities", [])
all_opps = sorted(export_opps + import_opps, key=lambda x: x["score"], reverse=True)

commodity_names = [o["commodity"] for o in all_opps]
selected = st.selectbox("Select a commodity to see its full business roadmap:", commodity_names)
opp = next(o for o in all_opps if o["commodity"] == selected)
is_export = opp["type"] == "export_opportunity"

direction_label = "EXPORT — you source in Ghana and sell abroad" if is_export else "IMPORT — you buy from overseas and distribute in Ghana"
st.markdown(f"### {selected} | {direction_label}")

score_icon = "🟢" if opp["score"] >= 70 else ("🟡" if opp["score"] >= 50 else "🔴")
margin_icon = {"green": "🟢", "yellow": "🟡", "red": "🔴"}.get(opp["margin_flag"], "")
c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("Opportunity Score", f"{score_icon} {opp['score']}/100")
with c2: st.metric("Est. Gross Margin", f"{margin_icon} {opp['margin_pct']}%")
with c3: st.metric("Starting Order", f"GHC {opp['est_order_ghc']:,}")
with c4: st.metric("Est. Order Quantity", f"{opp['est_order_qty_mt']} MT")

st.markdown("---")

# PHASE 1 - RESEARCH
with st.expander("📋 PHASE 1 — Market Research (Weeks 1–3)", expanded=True):
    st.markdown("**Goal:** Validate demand and supply before spending any money.")

    if is_export:
        st.markdown(f"""
**1. Confirm there is a real buyer willing to pay**
- Contact at least 3 buyers in **{opp['best_market']}** (see Customer Directory page)
- Ask for a Letter of Intent (LOI) or Proforma Invoice Request — this is your proof of demand
- Confirm their required: quantity, quality specs, packaging, price ceiling, payment terms

**2. Confirm you can source the product in Ghana**
- Visit 3 production areas / processing centres
- Get quotes from 5 farmers/processors for {opp['est_order_qty_mt']} MT
- Confirm: availability, quality consistency, processing capability (cleaning, drying, grading)
- Compare prices to Ghana producer price benchmark: **${opp['ghana_producer_price_usd_mt']}/MT**

**3. Calculate your landed cost** (use this formula exactly):
```
Landed Cost = (Source price/MT × qty MT) + Processing + Export packing
            + Freight forwarder fee + Sea freight (CIF to destination port)
            + Export documentation (CoO, phytosanitary, fumigation if needed)
```
- Target: landed cost should leave you with ≥{opp['margin_pct']}% margin

**4. Check legal requirements**
- Does {selected} require an export permit in Ghana? → Check GEPA Ghana (gepaghana.org)
- What certifications does {opp['best_market']} require? → Check their customs authority
- Does the buyer require RSPO / Organic / Fair Trade? → Plan certification roadmap
""")
    else:
        best_sup = opp.get("best_supplier", "cheapest source")
        st.markdown(f"""
**1. Find buyers IN GHANA before you import anything**
- Visit 5+ wholesalers, retailers, or institutional buyers (see Customer Directory page)
- Get a soft purchase commitment: "If I deliver X kg at GHC Y, will you buy it?"
- Confirm buyer's requirements: quantity per week, preferred packaging, delivery schedule

**2. Get supplier quotes from {best_sup} and 2 alternatives**
- Contact 3 exporters for {selected} (see Customer Directory for supplier contacts)
- Request: price per MT (CIF Tema), MOQ, payment terms, lead time, sample availability
- Compare to benchmark: **${opp['best_price_usd_mt']}/MT** from {best_sup}

**3. Calculate your landed cost**:
```
Landed Cost = CIF Price + Ghana Customs Duty (check HS code {selected})
            + Port handling (Tema) + Customs broker fee
            + Inland transport (Tema → your buyer)
            + Your overhead (phone, fuel, storage for 30 days)
```
- Minimum target: sell at ≥{opp['margin_pct']}% above landed cost

**4. Check import regulations**
- Find the correct HS code for {selected} at Ghana Customs (customs.gov.gh)
- Check applicable duty rate (some food items have duty waivers in Ghana)
- Confirm if import license is required
""")

# PHASE 2 - SETUP
with st.expander("🏢 PHASE 2 — Business Registration (Weeks 3–6)"):
    st.markdown("**Goal:** Become a legal entity so banks, suppliers, and buyers can trust you.")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
**Ghana Business Registration (1–2 weeks)**
1. Register at the Registrar General's Department (RGD)
   - Cost: approx. GHC 500–2,000
   - Bring: Ghana Card / passport, 2 photos, proposed company name
   - Result: Certificate of Incorporation
2. Get Ghana Revenue Authority (GRA) TIN (Tax ID)
   - Required for customs clearance
   - Register online at gra.gov.gh
3. Open a dedicated business bank account
   - Required to receive foreign currency (USD) payments
   - Ask for a trade finance / forex account
""")
    with col2:
        if is_export:
            st.markdown("""
**Export-Specific Registration**
- Register with GEPA Ghana as an exporter (free for SMEs, gepaghana.org)
- Apply for export license if commodity requires it
- Register with Ghana Standards Authority (GSA) for product certification
- Check if your commodity needs Ghana FDA registration

**Quality certification plan** (start now — takes 3–12 months):
- HACCP / food safety (Ghana Standards Authority)
- RSPO / Organic / Fair Trade (if required by buyer)
- Certificate of Origin from Ghana Export Promotion Authority
""")
        else:
            st.markdown("""
**Import-Specific Registration**
- Register as an importer with Ghana Revenue Authority
- Find a licensed Customs House Broker (CHB) at Tema Port
  - Essential — they handle all port paperwork
  - Cost: ~1–2% of cargo value per shipment
- Research applicable duty rate for your HS code
- Understand VAT on imports (standard 15% in Ghana)

**Logistics setup** (before first shipment):
- Get 3 freight forwarder quotes for sea freight from source country
- Arrange marine/cargo insurance (required for LC transactions)
- Find warehouse / cold storage if commodity requires it
""")

# PHASE 3 - FIRST TRADE
with st.expander("🚢 PHASE 3 — First Sample Shipment (Weeks 6–14)"):
    if is_export:
        st.markdown(f"""
**Goal:** Ship a small sample (100 kg – 1 MT) to get your first buyer relationship and learn the logistics.

**Step-by-step:**
1. **Secure a written buyer commitment** (LOI or purchase order) for at least {opp['est_order_qty_mt']/4:.0f} MT at agreed price
2. **Source {selected}** from vetted farmers/processors — pay by mobile money, keep receipts
3. **Arrange processing/grading** to meet buyer's specifications — document with photos
4. **Book freight** with a freight forwarder (compare 3 quotes)
   - Mode: Air freight for first sample (expensive but fast and builds trust)
   - For commercial orders: sea freight (FCL or LCL)
5. **Get export documents** (your freight forwarder helps with most):
   - Phytosanitary certificate (Ministry of Food and Agriculture Ghana)
   - Certificate of Origin (GEPA Ghana or Chamber of Commerce)
   - Commercial Invoice + Packing List (you prepare)
   - Bill of Lading (freight forwarder issues)
6. **Receive payment** — best for first deal:
   - 30–50% deposit before shipping (via bank transfer to your business account)
   - Balance on receipt of shipping documents (or LC if buyer demands)
7. **Track shipment** and confirm delivery
8. **Invoice the balance** and collect payment
""")
    else:
        st.markdown(f"""
**Goal:** Import your first small batch (~{opp['est_order_qty_mt']/4:.0f}–{opp['est_order_qty_mt']:.0f} MT), clear customs, and deliver to your buyer.

**Step-by-step:**
1. **Secure your Ghana buyer's purchase commitment** — written order or verbal + deposit
2. **Place order with your overseas supplier**
   - Use a simple Purchase Order (template available from GEPA)
   - Payment: T/T (bank wire) 30% deposit if trusted, or Letter of Credit for first time
3. **Arrange shipping** with your freight forwarder
   - CIF Tema (supplier covers freight to Ghana port) = easiest for first shipment
4. **Prepare import documents** (your supplier provides most):
   - Commercial Invoice + Packing List
   - Bill of Lading or Airway Bill
   - Certificate of Origin from source country
   - Any quality/health certificates required by Ghana FDA
5. **Customs clearance at Tema** (your Customs Broker handles this)
   - Submit: import declaration (Ghana Customs Management System)
   - Pay: customs duty + VAT + ECOWAS levy
   - Receive goods from port (broker manages this)
6. **Inland delivery to your buyer** — hire a truck from Tema
7. **Collect payment from buyer** on delivery (or per agreed terms)
8. **Calculate actual margin** — compare to your projection
""")

# PHASE 4 - SCALE
with st.expander("🚀 PHASE 4 — Scale Up (Month 4 onwards)"):
    st.markdown(f"""
**Goal:** Once first trade is profitable, reinvest and grow systematically.

**Reinvestment strategy (Weiss):**
- Reinvest **80% of profit** from first trade into the next order
- Keep **20% as personal income** and emergency reserve
- Do NOT diversify to a second commodity until {selected} is generating consistent cash flow

**Volume milestones:**
| Order | Size | Target Month |
|---|---|---|
| Trial order | {opp['est_order_qty_mt']/4:.0f} MT | Month 2-3 |
| First commercial | {opp['est_order_qty_mt']:.0f} MT | Month 4-5 |
| Scale order | {opp['est_order_qty_mt']*2:.0f} MT | Month 6-8 |
| Container load | {opp['est_order_qty_mt']*4:.0f} MT | Month 9-12 |

**Adding buyers/markets:**
- After 3 successful trades with your first buyer, approach 2 more buyers
- For export: add one more country market after proving {opp['best_market']}
- For import: add one more city/region distribution point

**Value-add opportunities for {selected}:**
""")
    if selected == "Shea butter":
        st.markdown("- Move from raw shea → refined shea (higher price, +$300-500/MT premium)\n- Develop your own branded product (cosmetics, soap) for online export sales")
    elif selected == "Moringa powder":
        st.markdown("- Move from bulk powder → branded retail packs (50g, 100g pouches) for direct-to-consumer export\n- Organic certification unlocks 2–3x price premium")
    elif selected == "Ginger":
        st.markdown("- Move from raw/split-dried → powder or puree (value-added, higher margin)\n- Partner with a local processor to produce ginger oil (very high margin)")
    elif selected == "Cashew nuts":
        st.markdown("- Move from raw cashew nuts (RCN) → processed kernel (W320, W240 grades) for 3-5x value\n- Requires shelling equipment — possible with a cooperative")
    elif selected == "Rice":
        st.markdown("- Develop your own branded rice (private label packaging, premium variety)\n- Add value by offering branded 2 kg, 5 kg retail packs vs. 50 kg wholesale bags")
    elif selected == "Poultry":
        st.markdown("- Add cold-chain delivery service as a differentiator (most competitors don't)\n- Offer hotel/restaurant accounts with weekly subscription delivery")
    else:
        st.markdown("- Research value-added processing options specific to this commodity\n- Partner with a local processor to increase margin without capital-intensive equipment")

st.markdown("---")
st.caption("Framework: Weiss, K.D. (2007). *Building an Import/Export Business*, 4th ed. Wiley. | Bade, D.L. (2015). *Export/Import Procedures and Documentation*. AMACOM.")
