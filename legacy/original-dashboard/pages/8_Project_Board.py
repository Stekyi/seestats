"""
Project Board — one project per commodity with full task list, deliverables, timeline,
and business milestones. Based on Weiss 90-day framework + Bade documentation methodology.
"""
import sys
import streamlit as st
import pandas as pd
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import page_header

st.set_page_config(page_title="Project Board", page_icon="📌", layout="wide")
analysis = page_header("📌 Project Board", "Your commodity projects — tasks, deliverables, and milestones")

today = date.today()

PROJECTS = {
    "Shea butter (EXPORT)": {
        "commodity": "Shea butter",
        "direction": "export",
        "one_liner": "Source raw/refined shea butter from Northern Ghana women cooperatives and sell to European cosmetics ingredient buyers.",
        "target_market": "Netherlands / France",
        "target_revenue_usd": 10_000,
        "starting_budget_ghc": 55_000,
        "phases": [
            {
                "name": "Phase 1 — Market Research & Buyer Outreach",
                "duration_weeks": 3,
                "deliverables": [
                    "List of 10+ shea butter buyers in Netherlands/France (from Customer Directory)",
                    "3 email enquiries sent to European buyers",
                    "1 sample request received from at least 1 buyer",
                    "Visit 3 shea processing centres in Northern Ghana (prices, quality, availability)",
                    "Landed cost calculation spreadsheet (sourcing + processing + freight + certificates)",
                    "Gross margin confirmed ≥ 30% at target buyer price",
                ],
                "tasks": [
                    ("Send intro emails to AAK Netherlands, Olvea, De Wildt Schiedam", "high", 7),
                    ("Visit Northern Ghana shea production zones (Tamale, Bolgatanga)", "high", 14),
                    ("Get 3 shea processor quotes (price/MT, available volume, processing time)", "high", 14),
                    ("Calculate full landed cost (source + processing + freight + docs)", "high", 14),
                    ("Follow up with European buyers on sample request", "medium", 21),
                    ("Research RSPO and Organic certification roadmap + cost", "medium", 21),
                ],
            },
            {
                "name": "Phase 2 — Business Setup & Sample Preparation",
                "duration_weeks": 4,
                "deliverables": [
                    "Business registered at Registrar General's Department",
                    "GRA Tax ID obtained",
                    "Business bank account opened (with forex capability)",
                    "Registered with GEPA Ghana as an exporter",
                    "1 kg shea butter sample prepared and packaged",
                    "Product data sheet created (FFA%, moisture, IV, colour, origin)",
                    "Sample shipped to at least 1 European buyer (air freight)",
                    "Freight forwarder identified and briefed",
                ],
                "tasks": [
                    ("Register business at Registrar General (GHC 500-2,000)", "high", 7),
                    ("Get GRA TIN online at gra.gov.gh", "high", 7),
                    ("Open business bank account — bring: certificate, GRA TIN, Ghana Card", "high", 10),
                    ("Register with GEPA Ghana as exporter (free for SMEs)", "high", 14),
                    ("Prepare 10 x 1 kg shea butter samples (proper labelling)", "high", 14),
                    ("Create product specification sheet (1-page PDF)", "high", 14),
                    ("Get 3 freight forwarder quotes for air freight sample to Rotterdam", "medium", 14),
                    ("Ship sample to top 2 European buyers", "high", 21),
                    ("Email buyer with tracking number and full product spec", "high", 21),
                ],
            },
            {
                "name": "Phase 3 — First Commercial Shipment",
                "duration_weeks": 6,
                "deliverables": [
                    "Signed purchase order / Letter of Intent from European buyer",
                    "30% deposit received from buyer",
                    "3-5 MT of shea butter sourced and quality checked",
                    "All export documents obtained (phytosanitary, CoO, commercial invoice)",
                    "Cargo shipped (LCL or FCL sea freight to Rotterdam/Le Havre)",
                    "Balance payment received on delivery",
                    "First trade profit/loss statement prepared",
                ],
                "tasks": [
                    ("Receive sample feedback from buyer — confirm they want to proceed", "high", 7),
                    ("Negotiate price and issue a Proforma Invoice to buyer", "high", 10),
                    ("Collect 30% deposit (via bank wire) before sourcing", "high", 14),
                    ("Source and process 3-5 MT shea butter — photograph all steps", "high", 21),
                    ("Get phytosanitary certificate (Ministry of Food & Agriculture)", "high", 21),
                    ("Get Certificate of Origin from Ghana Chamber of Commerce or GEPA", "high", 21),
                    ("Book LCL/FCL sea freight with freight forwarder (CIF Rotterdam)", "high", 25),
                    ("Ship cargo, send buyer all shipping documents (BL, invoice, packing list)", "high", 28),
                    ("Follow up with buyer on receipt and collect final payment", "high", 42),
                    ("Calculate actual vs. projected margin — document lessons", "medium", 45),
                ],
            },
            {
                "name": "Phase 4 — Scale & Certification",
                "duration_weeks": 12,
                "deliverables": [
                    "2nd and 3rd successful trade completed",
                    "Second European buyer relationship initiated",
                    "RSPO certification application submitted",
                    "Volume increased to 10+ MT per shipment",
                    "Supplier contract signed with top shea processor",
                ],
                "tasks": [
                    ("Re-order from same buyer and negotiate better price for larger volume", "high", 7),
                    ("Approach second buyer from Customer Directory", "medium", 14),
                    ("Begin RSPO certification process (contact RSPO Ghana office)", "medium", 21),
                    ("Negotiate exclusive supply agreement with best shea processor", "medium", 30),
                    ("Scale order to 10 MT — aim for full container (FCL)", "high", 60),
                    ("Explore value-added refining to increase price by $300-500/MT", "low", 84),
                ],
            },
        ],
        "kpis": [
            {"KPI": "Buyers contacted", "Target": "10 in 3 weeks", "Status": "Not started"},
            {"KPI": "Samples sent", "Target": "3 samples in 6 weeks", "Status": "Not started"},
            {"KPI": "First purchase order", "Target": "By week 8", "Status": "Not started"},
            {"KPI": "First shipment", "Target": "By week 14", "Status": "Not started"},
            {"KPI": "Gross margin", "Target": "≥ 30%", "Status": "Not started"},
            {"KPI": "First profit", "Target": "GHC 15,000+ from first trade", "Status": "Not started"},
        ],
        "budget_breakdown": {
            "Sourcing (3-5 MT shea)": 40_000,
            "Processing & grading": 5_000,
            "Export docs & certs": 3_000,
            "Freight forwarder": 4_000,
            "Business registration": 2_000,
            "Market research & travel": 6_000,
            "Emergency reserve": 3_000,
        },
        "risks": [
            ("Quality inconsistency from rural processors", "High", "Source from GEPA-listed processors, inspect before purchase"),
            ("European buyer rejects sample", "Medium", "Contact 5+ buyers simultaneously so one rejection doesn't stall progress"),
            ("Currency fluctuation (GHC/USD)", "Medium", "Invoice in USD, convert to GHC only when needed"),
            ("Payment delay from buyer", "Low", "Require 30% deposit before shipping, balance against shipping docs"),
        ],
    },
    "Moringa powder (EXPORT)": {
        "commodity": "Moringa powder",
        "direction": "export",
        "one_liner": "Process shade-dried moringa leaves into export-grade powder for the US/EU health supplement market.",
        "target_market": "USA / Germany",
        "target_revenue_usd": 8_000,
        "starting_budget_ghc": 50_000,
        "phases": [
            {
                "name": "Phase 1 — Product Development & Buyer Outreach",
                "duration_weeks": 3,
                "deliverables": [
                    "500g moringa powder sample prepared and lab-tested",
                    "Certificate of Analysis (COA) from accredited lab",
                    "Heavy metals and pesticide residue test results",
                    "Product specification sheet (1-page PDF)",
                    "5 US/EU buyers contacted with sample offer",
                ],
                "tasks": [
                    ("Source 5 kg of moringa leaves from local farmers for test processing", "high", 7),
                    ("Process, dry, and mill first test batch — document steps with photos", "high", 7),
                    ("Send 200g to accredited lab for COA (moisture, protein, microbiology)", "high", 10),
                    ("Send 100g for heavy metals and pesticide residue test", "high", 10),
                    ("Create product spec sheet (1 A4 page: specs, origin, certs available, price)", "medium", 14),
                    ("Email Sunfood, Frontier Co-op, Starwest Botanicals (Customer Directory)", "high", 14),
                    ("Follow up on sample requests", "medium", 21),
                ],
            },
            {
                "name": "Phase 2 — Setup & First Order",
                "duration_weeks": 5,
                "deliverables": [
                    "Business registered + GRA TIN",
                    "GEPA exporter registration",
                    "100-500g samples shipped to 3 US/EU buyers",
                    "First purchase order received (minimum 100 kg)",
                    "Commercial shipment prepared and shipped",
                ],
                "tasks": [
                    ("Register business + open forex bank account", "high", 7),
                    ("Prepare 20 x 200g sample packs (professional labelling)", "high", 7),
                    ("Ship samples via DHL/FedEx to 3 US buyers + 2 EU buyers", "high", 10),
                    ("Follow up with buyers post-sample — collect feedback", "high", 21),
                    ("Negotiate price and issue Proforma Invoice to first buyer", "high", 28),
                    ("Collect deposit, source and process commercial quantity", "high", 35),
                    ("Book air freight or sea freight depending on quantity", "medium", 35),
                ],
            },
        ],
        "kpis": [
            {"KPI": "COA test completed", "Target": "Week 2", "Status": "Not started"},
            {"KPI": "Samples shipped", "Target": "5 buyers, week 4", "Status": "Not started"},
            {"KPI": "First purchase order", "Target": "100 kg min, week 7", "Status": "Not started"},
            {"KPI": "Gross margin", "Target": "≥ 50%", "Status": "Not started"},
        ],
        "budget_breakdown": {
            "Sourcing raw moringa leaves": 10_000,
            "Processing equipment / facility": 15_000,
            "Lab testing (COA + safety)": 5_000,
            "Samples + DHL shipping": 5_000,
            "Business registration": 2_000,
            "Freight (first commercial)": 8_000,
            "Emergency reserve": 5_000,
        },
        "risks": [
            ("Lab test failure (microbiology)", "Medium", "Use clean processing facility, test before shipping any commercial order"),
            ("US buyers require USDA Organic", "High", "Start with conventional — organic certification added in Phase 3"),
            ("Small initial volumes make sea freight uneconomical", "Medium", "Use air freight for first 3 orders under 100 kg"),
        ],
    },
    "Rice (IMPORT)": {
        "commodity": "Rice",
        "direction": "import",
        "one_liner": "Import parboiled rice from India (cheapest source) and distribute to wholesalers and retailers in Ghana.",
        "target_market": "Accra / Kumasi wholesale markets",
        "target_revenue_ghc": 75_000,
        "starting_budget_ghc": 60_000,
        "phases": [
            {
                "name": "Phase 1 — Buyer Identification & Market Testing",
                "duration_weeks": 2,
                "deliverables": [
                    "5 Ghana wholesalers / retailers visited and purchase interest confirmed",
                    "Target price established (what price will buyers pay per bag?)",
                    "Landed cost calculation completed (import price + duty + broker + transport)",
                    "Gross margin confirmed ≥ 20% at market price",
                ],
                "tasks": [
                    ("Visit Agbogbloshie market grain section — talk to 5+ traders", "high", 3),
                    ("Visit Kumasi Kejetia market grain section — confirm demand and price", "high", 5),
                    ("Get current market price for 50 kg parboiled rice in Accra (3 sources)", "high", 3),
                    ("Calculate landed cost: India CIF Tema ($290/MT) + 10% duty + $50 broker = ?", "high", 7),
                    ("Confirm margin ≥ 20% — if not, check Vietnam rice (lower quality, lower price)", "high", 7),
                    ("Get soft purchase commitment from 2 wholesalers", "medium", 10),
                ],
            },
            {
                "name": "Phase 2 — Import Setup & First Shipment",
                "duration_weeks": 8,
                "deliverables": [
                    "Business registered + GRA importer TIN",
                    "Licensed Customs House Broker engaged at Tema",
                    "Freight forwarder quote obtained (India → Tema)",
                    "Supplier order placed (minimum 1 x 20ft container = ~18 MT)",
                    "Goods cleared at Tema and delivered to buyers",
                    "Payment collected from buyers",
                ],
                "tasks": [
                    ("Register business + GRA TIN", "high", 5),
                    ("Find licensed Customs Broker at Tema (ask GEPA for referrals)", "high", 7),
                    ("Contact India Rice Exporters Council (IREC) for supplier list", "high", 7),
                    ("Get 3 supplier quotes from India (CIF Tema, 18 MT minimum)", "high", 14),
                    ("Place order + arrange 30% payment via bank wire", "high", 18),
                    ("Arrange marine cargo insurance for shipment", "medium", 18),
                    ("Track shipment — ETA to Tema port approx. 20-25 days from India", "medium", 25),
                    ("Brief customs broker 5 days before vessel arrival (pre-clearance)", "high", 35),
                    ("Clear customs, arrange truck from Tema to Accra", "high", 40),
                    ("Deliver to buyers and collect payment", "high", 42),
                    ("Calculate actual margin vs projected — document differences", "medium", 45),
                ],
            },
        ],
        "kpis": [
            {"KPI": "Wholesalers committed", "Target": "2 buyers with soft order, week 2", "Status": "Not started"},
            {"KPI": "Supplier confirmed", "Target": "Week 3", "Status": "Not started"},
            {"KPI": "First container arrived", "Target": "Week 8-10", "Status": "Not started"},
            {"KPI": "Gross margin", "Target": "≥ 20%", "Status": "Not started"},
        ],
        "budget_breakdown": {
            "Product (18 MT rice from India, $290/MT)": 40_000,
            "Customs duty + VAT (est. 15%)": 8_000,
            "Customs broker fee": 2_000,
            "Inland transport Tema → Accra": 1_500,
            "Marine insurance": 1_000,
            "Business registration": 2_000,
            "Emergency reserve": 5_500,
        },
        "risks": [
            ("Global rice price spike (India export restrictions)", "High", "Lock in price with supplier via forward contract or pre-pay"),
            ("GHC depreciation making imports more expensive", "Medium", "Price goods in GHC including a 5% currency buffer"),
            ("Buyers delay payment", "Medium", "Collect 50% upfront for first 3 deliveries"),
        ],
    },
}

all_projects = list(PROJECTS.keys())
selected_project = st.selectbox("Select a project:", all_projects)
proj = PROJECTS[selected_project]

c1, c2, c3 = st.columns(3)
with c1: st.metric("Target Market", proj["target_market"])
with c2: st.metric("Starting Budget", f"GHC {proj['starting_budget_ghc']:,}")
rev_key = "target_revenue_usd" if "target_revenue_usd" in proj else "target_revenue_ghc"
rev_val = proj.get(rev_key, 0)
rev_label = f"${rev_val:,} USD" if "usd" in rev_key else f"GHC {rev_val:,}"
with c3: st.metric("Target Revenue (first trade)", rev_label)

st.markdown(f"> {proj['one_liner']}")
st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["📋 Task Plan", "💰 Budget", "⚠️ Risk Register", "📊 KPIs"])

with tab1:
    st.subheader("Project Phases & Tasks")
    start_date = today
    for phase in proj["phases"]:
        phase_end = start_date + timedelta(weeks=phase["duration_weeks"])
        st.markdown(f"### {phase['name']}")
        st.caption(f"Start: {start_date} | End: {phase_end} ({phase['duration_weeks']} weeks)")

        st.markdown("**Deliverables (what you must produce):**")
        for d in phase["deliverables"]:
            st.checkbox(d, key=f"del_{hash(d)}")

        st.markdown("**Tasks:**")
        task_rows = []
        for (task, priority, day_offset) in phase["tasks"]:
            due = start_date + timedelta(days=day_offset)
            task_rows.append({"Task": task, "Priority": priority, "Due Date": str(due)})
        df_tasks = pd.DataFrame(task_rows)
        priority_colors = {"high": "🔴", "medium": "🟡", "low": "🟢"}
        df_tasks["Priority"] = df_tasks["Priority"].map(lambda x: f"{priority_colors.get(x, '')} {x.upper()}")
        st.dataframe(df_tasks, use_container_width=True, hide_index=True)

        start_date = phase_end
        st.markdown("")

with tab2:
    st.subheader("Budget Breakdown")
    budget_items = proj.get("budget_breakdown", {})
    total = sum(budget_items.values())
    rows = [{"Category": k, "Amount (GHC)": v, "% of Budget": f"{v/total*100:.0f}%"}
            for k, v in budget_items.items()]
    rows.append({"Category": "TOTAL", "Amount (GHC)": total, "% of Budget": "100%"})
    df_budget = pd.DataFrame(rows)
    st.dataframe(df_budget, use_container_width=True, hide_index=True)

    import plotly.express as px
    items = {k: v for k, v in budget_items.items()}
    fig = px.pie(values=list(items.values()), names=list(items.keys()),
                  title=f"Budget Allocation — {selected_project}",
                  color_discrete_sequence=px.colors.sequential.Blues_r)
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Risk Register")
    risks = proj.get("risks", [])
    if risks:
        risk_rows = [{"Risk": r[0], "Likelihood": r[1], "Mitigation": r[2]} for r in risks]
        df_risks = pd.DataFrame(risk_rows)
        st.dataframe(df_risks, use_container_width=True, hide_index=True)
    else:
        st.info("No risks logged yet.")

with tab4:
    st.subheader("Key Performance Indicators")
    kpis = proj.get("kpis", [])
    if kpis:
        df_kpis = pd.DataFrame(kpis)
        st.dataframe(df_kpis, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("### Update Your Progress")
    with st.form("kpi_update"):
        kpi_name = st.selectbox("KPI", [k["KPI"] for k in kpis] if kpis else ["N/A"])
        new_status = st.selectbox("New Status", ["Not started", "In progress", "Completed", "Blocked"])
        kpi_note = st.text_input("Notes")
        if st.form_submit_button("Update"):
            st.success(f"Status updated: {kpi_name} → {new_status}")

st.markdown("---")
st.caption("Projects generated from TradeOps analysis. Methodology: Weiss (2007) 90-day framework adapted for Ghana SME context.")
