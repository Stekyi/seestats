"""
First Mover Strategy — how to enter and own a market where no established
playbook exists: validate, position, build demand, and lock in advantage.
"""
import sys
import plotly.graph_objects as go
import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import date, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))
from discover_opportunities import get_all_discoveries

st.set_page_config(page_title="First Mover Strategy", page_icon="🚀", layout="wide")

st.title("🚀 First Mover Strategy")
st.caption(
    "You have found an undiscovered space. Now what? "
    "This page teaches you how to enter a market that doesn't have a roadmap yet."
)

st.warning(
    "**This is different from the Business Roadmap page.** "
    "That page covers established commodities with existing buyers. "
    "This page is for blue ocean discoveries where YOU must create the market, "
    "find buyers who don't know they need your product, and move fast before others follow."
)

discoveries = get_all_discoveries()
names = [d["name"].split("(")[0].strip() for d in discoveries]
selected_name = st.selectbox("Select a blue ocean discovery to plan your first-mover strategy:", names)
selected = next(d for d in discoveries if d["name"].startswith(selected_name))
is_export = selected["direction"] == "export"

tier_colors = {
    "EXTREME": "#e74c3c", "HIGH": "#e67e22", "MEDIUM-HIGH": "#f1c40f", "MEDIUM": "#27ae60"
}
tier_col = tier_colors.get(selected["blue_ocean_tier"], "#888")

st.markdown(
    f"<div style='padding:12px; border-left:5px solid {tier_col}; background:#111'>"
    f"<b style='font-size:1.1em'>{selected['name']}</b> | "
    f"Blue Ocean Tier: <b>{selected['blue_ocean_tier']}</b> | "
    f"Score: <b>{selected['total_score']}/100</b> | "
    f"Est. Margin: <b>{selected['gross_margin_pct']}%</b>"
    f"</div>",
    unsafe_allow_html=True,
)
st.markdown("")

# ─────────────────────────────────────────────────────────────────────────────
# Core principle box
# ─────────────────────────────────────────────────────────────────────────────
st.info("""
**The three laws of first-mover success (Blue Ocean adapted from Kim & Mauborgne):**

1. **Create demand, don't chase demand.** Established buyers don't yet know they want your product.
   You must show them, sample them, educate them. This takes 30-90 days, not 7.
2. **Move fast, lock in before imitation.** Once you prove the market works, competitors will follow
   within 12-18 months. Your job is to be the brand customers already know by then.
3. **Start small, learn fast.** A £200 Etsy test will tell you more than a 1-year feasibility study.
   Sell 10 units, read the reviews, adjust, then scale.
""")

st.markdown("---")

# ─────────────────────────────────────────────────────────────────────────────
# PHASE 1: Validation without existing buyers
# ─────────────────────────────────────────────────────────────────────────────
with st.expander("🧪 PHASE 1 — Validate Without Buyers (Weeks 1-4)", expanded=True):
    st.markdown("**Goal:** Prove people will pay for this BEFORE spending more than GHC 2,000.")

    st.markdown(f"""
**Why this phase is different from a normal import/export start:**
Established commodities (rice, shea butter) have published buyer databases — you find buyers, contact them, get a PO.
With {selected['name']}, there is no buyer database. You are creating a market.
The validation playbook:

**Step 1 — The £1 test (Free)**
Post on Facebook groups, Reddit r/Ghana, LinkedIn, and Twitter/X:
> "I have access to {selected['name'].split('(')[0].strip()} from Ghana.
> Would anyone pay [target price] for [quantity]? Reply below."
If 5+ people say yes, demand is real. If 0, reframe or reconsider.

**Step 2 — Send 10 free samples to the RIGHT people**
Don't send to friends. Send to:
- Buyers at specialty retailers (find on LinkedIn by title: "Procurement", "Buyer", "Category Manager")
- Food bloggers / beauty influencers in target market (UK, USA, Germany)
- Chefs at restaurants that serve cuisine related to your product
Total cost: shipping + product = under GHC 500.
Goal: 2-3 people respond with genuine interest or a written order.

**Step 3 — Sell your first unit within 14 days**
Open an Etsy shop or list on eBay. Price high (you can always discount).
If you sell 1 unit to a stranger, the market exists.
If you can't sell 1 unit in 14 days, the positioning or price is wrong — fix it.

**Step 4 — Get one written testimonial before scaling**
Ask your first buyer: "What made you buy this?" and "What would you tell a friend?"
This testimonial becomes your first marketing asset.
""")

    # Quick validation checklist
    st.markdown("**Validation Checklist:**")
    checks = [
        "Posted in 3 online communities to gauge interest",
        "Sent 10 physical samples with a brief product card",
        "Listed on Etsy / eBay / Amazon (whichever applies)",
        "Made first sale to a stranger (not a friend)",
        "Collected 1 written testimonial or review",
        "Confirmed: people understand what the product is and why they'd buy it",
    ]
    for c in checks:
        st.checkbox(c, key=f"phase1_{c[:20]}")

# ─────────────────────────────────────────────────────────────────────────────
# PHASE 2: Build the story and brand
# ─────────────────────────────────────────────────────────────────────────────
with st.expander("🎨 PHASE 2 — Build the Brand & Story (Weeks 3-8)"):
    st.markdown("**Goal:** In blue ocean markets, the STORY is the product — buyers don't have a reference point. Give them one.")

    st.markdown(f"""
**Why brand matters more here than in established commodities:**
When someone searches 'Shea butter' they know what it is. When someone encounters
'{selected['name'].split('(')[0].strip()}' for the first time, they are buying your explanation.
The brand IS the education.

**Your brand must answer four questions in 5 seconds:**
1. **What is it?** — one clear line. No jargon.
2. **Where does it come from?** — Ghana, specific region, specific farmers if possible.
3. **Why should I care?** — the benefit (health, taste, beauty, ethics, uniqueness).
4. **Why this brand?** — your specific story (founder, origin, mission).

**Brand assets to create (budget GHC 3,000-8,000):**
- Logo + brand name: Use Canva Pro or hire a Ghanaian graphic designer (GHC 500-1,500)
- Product packaging: Custom printed labels from VistaPrint or a local printer
- 1-page product data sheet: Product name, origin, usage, specifications, certifications
- Instagram / TikTok page: 10 posts before launch (sourcing story, farm, product shots)
- A simple landing page: Carrd.co (free) or Shopify ($29/month) with a "Buy Now" button

**Storytelling template for {selected['name'].split('(')[0].strip()}:**
> "In [region], Ghana, [farmers / trees / artisans] produce [product name]. For centuries,
> [local use or significance]. Now, for the first time, we are bringing it to [target market].
> [Key benefit in one sentence]. From source to shelf — [brand name]."

**Document everything:**
Photos of sourcing, farmers, processing, packaging. This visual content is your competitive moat.
It cannot be copied by a competitor who sources the same thing — your story is unique.
""")

# ─────────────────────────────────────────────────────────────────────────────
# PHASE 3: First commercial sales
# ─────────────────────────────────────────────────────────────────────────────
with st.expander("💰 PHASE 3 — First Commercial Sales (Weeks 6-16)"):
    ghc = selected["starting_order_ghc"]
    qty = selected["starting_qty_kg"]
    margin = selected["gross_margin_pct"]

    st.markdown(f"""
**Goal:** Generate your first GHC 10,000+ in revenue from real buyers. Prove unit economics.

**First-mover channel priority order:**

1. **DTC online (Etsy / Amazon / Shopify)** — fastest to market, no gatekeepers
   - No minimum order from buyers
   - You control pricing and positioning
   - International shipping from Ghana: ~$15-25 per 0.5-1 kg package (DHL Express)
   - Use Payoneer or Wise account for international payments

2. **Diaspora community sales** — African communities in UK/USA/Germany
   - Contact African food stores (walk in or email)
   - WhatsApp business groups for Ghanaian diaspora
   - Consignment: leave 20 units, collect payment after they sell

3. **Wholesale to one early-adopter retailer** — sign them as a named partner
   - Target: smaller independent retailers, NOT supermarkets yet
   - Offer exclusive distribution in their city for first 6 months (creates urgency)

**First commercial order sizing:**
- Starting investment: GHC {ghc:,}
- Starting quantity: {qty} kg (or equivalent)
- Target margin at this scale: {margin}%
- Break-even point: sell {int(ghc / (ghc / qty * margin / 100)):,} kg to recover investment

**Payment terms for first-time buyers:**
- DTC online: 100% upfront (standard for e-commerce)
- Diaspora stores: 50% upfront, 50% after 30 days
- NGO / institutional: 30% deposit, 70% on delivery
- NEVER offer 100% credit to an unknown buyer

**Proof of demand document to build:**
After every sale, record: buyer name, quantity, price, feedback.
After 10 sales, you have a "sales track record" that makes your next pitch to larger buyers credible.
""")

    if is_export:
        st.markdown(f"""
**Export logistics for a small first shipment ({qty} kg):**
- Air freight to UK/EU: DHL Express, ~$8-15/kg for parcels under 30 kg
- Courier option: Aramex Ghana has a dedicated e-commerce shipping service
- Documents needed: Commercial invoice, packing list, and phytosanitary certificate
  (if plant-based product — phyto cert from Ministry of Food & Agriculture, ~GHC 150 per shipment)
- Declare correctly at customs — underdeclaring is fraud, not a cost-saving strategy
""")
    else:
        st.markdown(f"""
**Import logistics for a small first batch:**
- Source from Alibaba.com (verified suppliers with trade assurance)
- DDP (Delivered Duty Paid) terms — supplier handles all shipping and customs
- Use trade assurance / escrow — never wire money direct on first order
- Your Customs House Broker at Tema handles Ghana import clearance
""")

# ─────────────────────────────────────────────────────────────────────────────
# PHASE 4: Lock in first-mover advantage
# ─────────────────────────────────────────────────────────────────────────────
with st.expander("🔒 PHASE 4 — Lock in First-Mover Advantage (Month 4-12)"):
    st.markdown(f"""
**Goal:** By month 4, competitors will notice if you're succeeding. Build moats before they arrive.

**The 5 moats for blue ocean first-movers:**

**Moat 1 — Brand & story ownership**
Your brand name, photos, story, and customer reviews cannot be replicated.
Register your brand as a trademark (EU: ~€850 via EUIPO; USA: ~$250 via USPTO).
A registered trademark blocks copycats from using your name.

**Moat 2 — Exclusive sourcing agreements**
Sign 1-2 year supply contracts with your farmers or processors.
A competitor who arrives 6 months after you finds your suppliers already locked up.
Cost: a written agreement — no money needed, just commitment.

**Moat 3 — Certification leadership**
Get the certifications your competitors won't bother with because they don't know the market exists.
For {selected['name'].split('(')[0].strip()}: {', '.join(selected.get('risks', ['HACCP', 'COA'])[:2]) if selected.get('risks') else 'relevant certifications'}.
A certified product blocks entry for buyers who require certification.

**Moat 4 — Customer relationship depth**
Know your top 10 buyers by name. Call them. Visit the UK/US buyers once a year.
Personal relationships are the hardest thing for a competitor to replicate.

**Moat 5 — Volume and price**
Once you hit 500 kg / month, your unit cost drops. Use some of that margin to lower price slightly.
A competitor entering at small scale cannot match your cost structure.

**Scale milestones for {selected['name'].split('(')[0].strip()}:**
| Month | Target Revenue (GHC) | Target Volume | Key Milestone |
|-------|---------------------|---------------|---------------|
| 1-2   | GHC 5,000           | {qty//4} kg test | First 10 sales, brand launched |
| 3-4   | GHC 20,000          | {qty//2} kg | First repeat buyer, 1 retail listing |
| 5-6   | GHC 50,000          | {qty} kg | Trademark filed, supply contract signed |
| 7-9   | GHC 100,000         | {qty*2} kg | 2nd market or channel added |
| 10-12 | GHC 200,000         | {qty*4} kg | Full container or established B2B account |
""")

# ─────────────────────────────────────────────────────────────────────────────
# First-mover specific action checklist
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.subheader(f"✅ First-Mover Action Checklist — {selected['name'].split('(')[0].strip()}")
st.markdown("These are the specific first-mover actions for this discovery (from research):")

today = date.today()
actions = selected.get("first_mover_actions", [])
for i, action in enumerate(actions):
    deadline = today + timedelta(weeks=(i + 1) * 2)
    col1, col2 = st.columns([5, 1])
    with col1:
        st.checkbox(f"**Week {(i+1)*2}:** {action}", key=f"fm_action_{i}")
    with col2:
        st.caption(f"By {deadline.strftime('%d %b')}")

# ─────────────────────────────────────────────────────────────────────────────
# Risk mitigation
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("⚠️ First-Mover Risks & How to Manage Them")

risks = selected.get("risks", [])

st.markdown("""
**Generic first-mover risks (apply to all discoveries):**
""")
generic_risks = [
    ("Market doesn't materialise", "MEDIUM",
     "If 30 days of Etsy/online sales produces zero orders, pivot the positioning or reconsider. "
     "Your test investment should be under GHC 3,000 — this is cheap learning."),
    ("Competitor copies you", "HIGH (after Month 6)",
     "Accept this is inevitable. Focus on being 12 months ahead: more certifications, "
     "more customer relationships, lower cost structure. The copy-cat enters a market YOU created."),
    ("Buyer education takes too long", "MEDIUM",
     "Switch channels — if retail buyers take 6 months to decide, try DTC first. "
     "Get 100 DTC customers before approaching buyers. They become your proof of concept."),
    ("Supply disruption", "HIGH",
     "Never depend on a single source. Have 3 supplier relationships from Day 1. "
     "Keep 30-day buffer stock once you hit regular orders."),
]
for risk, severity, mitigation in generic_risks:
    color = "#8b0000" if severity == "HIGH (after Month 6)" else "#b8860b"
    with st.expander(f"{'🔴' if 'HIGH' in severity else '🟡'} {risk}"):
        st.markdown(f"**Severity:** {severity}")
        st.info(f"**Mitigation:** {mitigation}")

if risks:
    st.markdown(f"**Specific risks for {selected['name'].split('(')[0].strip()}:**")
    for r in risks:
        st.warning(r)

# ─────────────────────────────────────────────────────────────────────────────
# Blue ocean pricing strategy
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("💡 Pricing Strategy for New Markets")

col1, col2 = st.columns(2)
with col1:
    prod_price = selected.get("ghana_producer_price_usd_kg", 2.0) or 2.0
    export_price = selected.get("estimated_export_price_usd_kg", 10.0) or 10.0
    usd_ghc = 15.4

    st.markdown("**Price ladder builder:**")
    src_ghc = round(prod_price * usd_ghc, 0)
    target_ghc = round(export_price * usd_ghc, 0)
    margin_ghc = round(target_ghc - src_ghc, 0)

    st.metric("Source price in Ghana", f"~GHC {src_ghc}/kg (${prod_price}/kg)")
    st.metric("Target export price", f"~GHC {target_ghc}/kg (${export_price}/kg)")
    st.metric("Gross margin per kg", f"GHC {margin_ghc}/kg ({selected['gross_margin_pct']}%)")
    st.caption("Always add: freight + packaging + certification fees before finalizing your sell price.")

with col2:
    st.markdown("""
**How to set price in a market with no reference:**
1. **Anchor high** — start at the price that feels too expensive, then discount if needed.
   It is easy to lower price; impossible to raise it after customers know your price.
2. **Find a comparable product** and price at a 10-20% premium (you're more unique).
3. **Test 3 price points** on Etsy: same product listed at 3 different prices under 3 different
   product listings. See which converts best.
4. **Never compete on price alone** — you have no volume advantage yet.
   Compete on story, origin, uniqueness, certifications.
5. **Raise price as demand grows** — Etsy sellers increase price with every 10 reviews.
""")

# ─────────────────────────────────────────────────────────────────────────────
# 90-day sprint plan
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("📅 Your 90-Day First-Mover Sprint")
today = date.today()

sprint_weeks = [
    (1, 2, "Validate", "Post in 3 communities. Send 10 samples. Get first online listing live."),
    (3, 4, "First sale", "Make first stranger sale. Collect testimonial. Confirm pricing works."),
    (5, 6, "Brand launch", "Professional packaging designed. Social media account live with 10 posts."),
    (7, 8, "Supplier locked", "Sign supply agreement with 2 farmers / processors."),
    (9, 10, "Scale order", f"Place first commercial order: {selected['starting_qty_kg']//2} kg."),
    (11, 12, "Second channel", "Approach 5 diaspora stores or wholesale buyers with your track record."),
    (13, 14, "Certification", "Submit application for first certification (COA or phytosanitary)."),
]

sprint_data = []
for w_start, w_end, milestone, action in sprint_weeks:
    week_start_date = today + timedelta(weeks=w_start - 1)
    sprint_data.append({
        "Weeks": f"{w_start}-{w_end}",
        "Date": week_start_date.strftime("%d %b"),
        "Milestone": milestone,
        "Action": action,
    })

sprint_df = pd.DataFrame(sprint_data)
st.dataframe(sprint_df, use_container_width=True, hide_index=True)

st.markdown("---")
st.caption(
    "Framework: Kim, W.C. & Mauborgne, R. (2005). *Blue Ocean Strategy*. Harvard Business Review Press. | "
    "Weiss, K.D. (2007). *Building an Import/Export Business*, 4th ed. Wiley. | "
    "Data: published trade research, ITC Trade Map, PubMed, specialty trade publications 2024-2025."
)
