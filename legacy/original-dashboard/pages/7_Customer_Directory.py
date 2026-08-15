"""
Customer Directory — real prospect contacts, approach strategies, and email templates
for each commodity opportunity.
"""
import sys
import streamlit as st
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import page_header, ensure_analysis

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))
from customer_data import CUSTOMERS

st.set_page_config(page_title="Customer Directory", page_icon="📞", layout="wide")
ensure_analysis()
st.title("📞 Customer & Prospect Directory")
st.caption("Real companies to contact, how to approach them, and email templates — per commodity")

st.warning("""
**Disclaimer:** Company details are based on publicly available trade research (2024-2025).
Always verify contact details independently before sending commercial proposals.
Prices and volumes are indicative — negotiate based on your specific product quality.
""")

available = list(CUSTOMERS.keys())
selected = st.selectbox("Select commodity:", available)
data = CUSTOMERS[selected]

direction = data.get("direction", "export")
st.markdown(f"**Direction:** {'EXPORT from Ghana → sell abroad' if direction == 'export' else 'IMPORT to Ghana → distribute locally'}")
st.markdown(f"**Overview:** {data.get('description', '')}")

st.markdown("---")

if direction == "export":
    target_markets = data.get("target_markets", [])
    if target_markets:
        market_names = [m["country"] for m in target_markets]
        selected_market = st.selectbox("Target market:", market_names)
        market = next(m for m in target_markets if m["country"] == selected_market)

        st.subheader(f"🌍 {selected_market} — {market.get('why', '')}")

        for cust in market.get("customers", []):
            with st.expander(f"🏢 {cust['name']} — {cust['type']}"):
                c1, c2 = st.columns([2, 1])
                with c1:
                    if cust.get("website"):
                        st.markdown(f"**Website:** [{cust['website']}]({cust['website']})")
                    if cust.get("linkedin"):
                        st.markdown(f"**LinkedIn:** [{cust['linkedin']}]({cust['linkedin']})")
                    if cust.get("address"):
                        st.markdown(f"**Address:** {cust['address']}")
                    st.markdown(f"**Contact role:** {cust.get('contact_role', 'Procurement')}")
                    st.markdown(f"**Buying volume:** {cust.get('buying_volume_mt', 'Enquire')} MT/year")
                    st.markdown(f"**Price range:** ${cust.get('price_range_usd_mt', 'TBD')}/MT")
                    if cust.get("payment_terms"):
                        st.markdown(f"**Payment terms:** {cust['payment_terms']}")
                with c2:
                    certs = cust.get("certifications_required", [])
                    if certs:
                        st.markdown("**Certifications required:**")
                        for c in certs:
                            st.markdown(f"- {c}")

                st.markdown("**How to approach:**")
                st.info(cust.get("approach", "Email procurement department with product spec and sample offer."))

    st.markdown("---")

    # Trade shows
    shows = data.get("trade_shows", [])
    if shows:
        st.subheader("🎪 Trade Shows to Attend")
        st.markdown("Trade shows are the #1 way to meet multiple buyers in 3 days. GEPA Ghana often co-funds SME participation.")
        for show in shows:
            with st.expander(f"📅 {show['name']} — {show['location']} ({show['timing']})"):
                st.markdown(f"**Why attend:** {show['why']}")
                st.markdown("**How to prepare:**")
                st.markdown("- Bring 50+ product samples in professional packaging")
                st.markdown("- Prepare a 1-page product data sheet (specs, origin, certifications, pricing)")
                st.markdown("- Have a price list ready (CIF destination port)")
                st.markdown("- Register 3–4 months in advance (GEPA may subsidise fees for SMEs)")

    # Certifications
    certs = data.get("certifications_needed", [])
    if certs:
        st.markdown("---")
        st.subheader("🏆 Certifications Required for Export")
        st.markdown("These certifications unlock higher prices and more buyers. Plan your roadmap:")
        cert_timeline = {"RSPO": "6–12 months", "Organic (ECOCERT)": "12–24 months",
                         "Fair Trade": "6–18 months", "USDA Organic": "12–18 months",
                         "EU Organic": "12–18 months", "HACCP": "3–6 months",
                         "ISO 22000": "6–12 months", "Phytosanitary certificate": "1–2 weeks per shipment",
                         "Certificate of Origin": "1 week per shipment", "COA": "2–4 weeks (lab testing)"}
        for cert in certs:
            timeline = cert_timeline.get(cert, "Enquire with Ghana Standards Authority")
            st.markdown(f"- **{cert}** — Est. time: {timeline}")

else:
    # Import — buyers in Ghana + suppliers abroad
    st.subheader("🇬🇭 Buyers in Ghana (Your Customers)")
    buyers = data.get("buyers_in_ghana", [])
    for buyer in buyers:
        with st.expander(f"🏪 {buyer['name']} — {buyer['type']}"):
            if buyer.get("website"):
                st.markdown(f"**Website:** [{buyer['website']}]({buyer['website']})")
            if buyer.get("address"):
                st.markdown(f"**Location:** {buyer['address']}")
            st.markdown(f"**Contact role:** {buyer.get('contact_role', 'Procurement')}")
            st.markdown(f"**Buying volume:** {buyer.get('buying_volume', 'Enquire')}")
            st.markdown(f"**Payment terms:** {buyer.get('payment_terms', 'Negotiate')}")
            st.markdown("**How to approach:**")
            st.info(buyer.get("approach", "Visit in person, introduce yourself and your product."))

    st.markdown("---")
    st.subheader("🌍 Overseas Suppliers (Your Source)")
    suppliers = data.get("suppliers", [])
    for sup in suppliers:
        with st.expander(f"🏭 {sup['name']} — {sup.get('country', '')}"):
            if sup.get("website"):
                st.markdown(f"**Website:** [{sup['website']}]({sup['website']})")
            st.info(sup.get("approach", "Contact procurement team."))

st.markdown("---")

# Email template
template = data.get("intro_email_template", "")
if template:
    st.subheader("✉️ First Contact Email Template")
    st.markdown("**How to use:** Fill in the bracketed fields `[like this]` with your details. Send via email or LinkedIn InMail. Follow up once after 5 business days if no reply.")
    st.code(template, language=None)
    if st.button("Copy template to clipboard (requires manual copy from above)"):
        st.info("Select the text above and press Ctrl+C / Cmd+C to copy.")

st.markdown("---")
st.subheader("📋 First Contact Tracker")
st.markdown("Track your outreach below (this resets each session — keep a separate spreadsheet):")
with st.form("contact_log"):
    col1, col2, col3 = st.columns(3)
    with col1: company = st.text_input("Company name")
    with col2: contact_name = st.text_input("Contact person")
    with col3: status = st.selectbox("Status", ["Email sent", "Awaiting reply", "Call scheduled", "Sample requested", "Deal in progress", "Declined"])
    notes = st.text_area("Notes", placeholder="e.g. Requested 1 kg sample, waiting for reply")
    submitted = st.form_submit_button("Log Contact")
    if submitted and company:
        if "contacts" not in st.session_state:
            st.session_state["contacts"] = []
        st.session_state["contacts"].append({"Company": company, "Contact": contact_name, "Status": status, "Notes": notes})
        st.success(f"Logged: {company}")

if st.session_state.get("contacts"):
    import pandas as pd
    st.markdown("**Your outreach log this session:**")
    st.dataframe(pd.DataFrame(st.session_state["contacts"]), use_container_width=True, hide_index=True)
