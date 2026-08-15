import sys
import streamlit as st
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import ensure_analysis

st.set_page_config(page_title="Business Checklist", page_icon="✅", layout="wide")
ensure_analysis()
st.title("✅ Business Setup Checklist")
st.caption("Step-by-step guide based on Kenneth D. Weiss — Building an Import/Export Business (2007)")

st.info("💡 **Weiss Core Principle:** Find a buyer FIRST. Only spend capital on inventory after you have a confirmed purchase order.")

# Phase selector
phase = st.radio("Jump to phase:", ["All phases", "Phase 1: Research", "Phase 2: Setup", "Phase 3: First Trade", "Phase 4: Scale"], horizontal=True)

show_all = phase == "All phases"

# Phase 1
if show_all or phase == "Phase 1: Research":
    st.markdown("---")
    st.subheader("📋 Phase 1: Market Research (Weeks 1–4)")
    st.markdown("**Goal:** Identify 1-2 viable commodities with confirmed buyer interest before spending money.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Commodity Selection")
        st.checkbox("Identify 3-5 product ideas from TradeOps top opportunities")
        st.checkbox("Confirm commodity is NOT government-monopolized (no gold, raw cocoa, petroleum)")
        st.checkbox("Verify commodity is shelf-stable (not highly perishable for first trade)")
        st.checkbox("Check if commodity requires import/export license in Ghana")
        st.checkbox("Research seasonal availability if agricultural")

        st.markdown("#### Buyer Research")
        st.checkbox("Interview 5+ potential buyers (retailers, wholesalers, distributors)")
        st.checkbox("Get 1 informal purchase commitment (verbal or written)")
        st.checkbox("Confirm buyer's required: quantity, quality spec, packaging, price range")
        st.checkbox("Check buyer's payment terms (upfront? Net 30? On delivery?)")

    with col2:
        st.markdown("#### Supplier Research")
        st.checkbox("Contact 3+ potential suppliers for chosen commodity")
        st.checkbox("Request product catalog, samples, and price list")
        st.checkbox("Verify supplier is a registered business")
        st.checkbox("Get 2+ formal price quotations (CIF Tema port preferred)")
        st.checkbox("Check supplier's minimum order quantity (MOQ) vs your budget")

        st.markdown("#### Financial Check")
        st.checkbox("Build simple break-even model (landed cost + margin)")
        st.checkbox("Confirm gross margin ≥ 20% after all landed costs")
        st.checkbox("Estimate 3-month working capital requirements")
        st.checkbox("Ensure you can cover: product + shipping + duties + broker + 3 months overhead")

    st.markdown("**Key resources:**")
    st.markdown("- [GEPA Ghana (export promotion)](https://www.gepaghana.org/)")
    st.markdown("- [ITC Trade Map (global trade data)](https://www.trademap.org/)")
    st.markdown("- [Ghana Customs Authority](https://customs.gov.gh/)")
    st.markdown("- [Ghana Standards Authority](https://www.gsa.gov.gh/)")

# Phase 2
if show_all or phase == "Phase 2: Setup":
    st.markdown("---")
    st.subheader("🏢 Phase 2: Business Setup (Weeks 4–8)")
    st.markdown("**Goal:** Register your business and build foundational trade relationships.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Legal & Registration")
        st.checkbox("Register business with Registrar General's Department (Ghana)")
        st.checkbox("Obtain Ghana Revenue Authority (GRA) Taxpayer ID")
        st.checkbox("Open a business bank account (for Letters of Credit)")
        st.checkbox("Register with GEPA as exporter (if exporting — free for SMEs)")
        st.checkbox("Obtain import/export license if required for chosen commodity")
        st.checkbox("Get Ghana Revenue Authority import/export clearance registration")

        st.markdown("#### Customs & Logistics")
        st.checkbox("Engage a licensed Customs House Broker in Tema")
        st.checkbox("Understand HS code and applicable duty rate for your commodity")
        st.checkbox("Get freight forwarder quotes (ask for CIF vs FOB comparison)")
        st.checkbox("Understand Incoterms (CIF = supplier ships; FOB = you arrange)")
        st.checkbox("Research marine insurance options for first shipment")

    with col2:
        st.markdown("#### Supplier Relationships")
        st.checkbox("Request product samples from top 2 suppliers")
        st.checkbox("Test samples for quality and specification compliance")
        st.checkbox("Negotiate payment terms (aim for 30% upfront, balance on delivery)")
        st.checkbox("Agree on inspection clause (3rd party inspection before shipment)")
        st.checkbox("Draft supplier agreement or purchase order template")

        st.markdown("#### Financial Readiness")
        st.checkbox("Set up Letter of Credit capability with your bank")
        st.checkbox("Understand bank's LC fees and timeline (typically 5-10 business days)")
        st.checkbox("Build foreign currency account if dealing with USD invoices")
        st.checkbox("Set budget allocation: 55% product, 25% buffer, 10% research, 7% customs, 3% emergency")

    st.markdown("**Key contacts to establish:**")
    cols = st.columns(3)
    with cols[0]:
        st.info("🏦 **Bank**\nRequest trade finance / LC services")
    with cols[1]:
        st.info("📦 **Freight Forwarder**\nGet quotes from 3 companies")
    with cols[2]:
        st.info("🛃 **Customs Broker**\nNeed them before goods arrive")

# Phase 3
if show_all or phase == "Phase 3: First Trade":
    st.markdown("---")
    st.subheader("🚢 Phase 3: First Shipment (Weeks 8–16)")
    st.markdown("**Goal:** Execute your first small test order. Learn the process. Don't over-invest.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Pre-Shipment")
        st.checkbox("Secure confirmed purchase order from buyer (written)")
        st.checkbox("Place order with supplier (small quantity — 1-5 MT to start)")
        st.checkbox("Arrange payment via LC or agreed terms")
        st.checkbox("Confirm shipping timeline with supplier (allow 2-4 week buffer)")
        st.checkbox("Arrange marine insurance before shipment leaves")
        st.checkbox("Brief customs broker with commodity, HS code, estimated value")

        st.markdown("#### During Shipping")
        st.checkbox("Track shipment via freight forwarder (get container/bill of lading number)")
        st.checkbox("Prepare import documentation: commercial invoice, packing list, CoO, phytosanitary cert if needed")
        st.checkbox("Pre-clear customs (submit docs before vessel arrives)")

    with col2:
        st.markdown("#### On Arrival")
        st.checkbox("Customs broker handles port clearance at Tema")
        st.checkbox("Inspect goods against specifications before accepting delivery")
        st.checkbox("Arrange inland transport from Tema to buyer/warehouse")
        st.checkbox("Deliver to buyer and collect payment per agreed terms")
        st.checkbox("Calculate actual vs projected margin (did it match?)")

        st.markdown("#### Post-Trade Review")
        st.checkbox("Document all costs: product, shipping, insurance, duties, broker, transport")
        st.checkbox("Calculate actual gross margin — was it ≥ 20%?")
        st.checkbox("Get buyer feedback — quality, quantity, timing OK?")
        st.checkbox("Decide: repeat same commodity or pivot based on learnings")
        st.checkbox("Reinvest profits into next order (do NOT withdraw all profit yet)")

# Phase 4
if show_all or phase == "Phase 4: Scale":
    st.markdown("---")
    st.subheader("🚀 Phase 4: Scale & Diversify (Month 4+)")
    st.markdown("**Goal:** Once first trade is profitable, reinvest and grow systematically.")

    st.markdown("""
    - **Repeat proven trades** before adding a second commodity
    - **Increase order size** by 25–50% each cycle as cash flow allows
    - **Add 1 new commodity every 3-4 months** once your first is running smoothly
    - **Build buyer network:** add 2-3 buyers per commodity for resilience
    - **Negotiate better terms** with suppliers after 3+ successful orders
    - **Consider value-added processing:** e.g. buy raw ginger → dry/process → higher export price
    - **Track via this dashboard** — if opportunity score drops, investigate market shifts early
    """)

    st.markdown("---")
    st.subheader("📞 Key Ghana Trade Contacts")
    contacts = [
        {"Organisation": "GEPA Ghana", "Purpose": "Export promotion, SME support, buyer leads", "Contact": "gepaghana.org"},
        {"Organisation": "Ghana Customs Authority", "Purpose": "Duty rates, import/export licensing", "Contact": "customs.gov.gh"},
        {"Organisation": "Ghana Standards Authority", "Purpose": "Product certification for export", "Contact": "gsa.gov.gh"},
        {"Organisation": "GIPC", "Purpose": "Investment promotion, incentives", "Contact": "gipcghana.com"},
        {"Organisation": "GRATIS Foundation", "Purpose": "SME technical support", "Contact": "gratisfoundation.com"},
        {"Organisation": "Tema Port (GPHA)", "Purpose": "Port operations, clearance", "Contact": "ghanaports.com.gh"},
    ]
    import pandas as pd
    st.dataframe(pd.DataFrame(contacts), use_container_width=True, hide_index=True)

st.markdown("---")
st.caption("Framework based on: Weiss, K.D. (2007). *Building an Import/Export Business*. Wiley. | Adapted for Ghana SME context.")
