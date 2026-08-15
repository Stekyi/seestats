"""Shared helpers for all dashboard pages."""
import json
from pathlib import Path
import streamlit as st

REPORTS_DIR = Path(__file__).parent.parent / "reports"


def get_report_dates() -> list:
    if not REPORTS_DIR.exists():
        return []
    return sorted([d.name for d in REPORTS_DIR.iterdir() if d.is_dir()], reverse=True)


def load_analysis(report_date: str) -> dict:
    path = REPORTS_DIR / report_date / "analysis.json"
    if path.exists():
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return {}


def ensure_analysis() -> dict:
    """Load analysis into session_state from the latest report if not already present."""
    if st.session_state.get("analysis"):
        return st.session_state["analysis"]
    dates = get_report_dates()
    if not dates:
        return {}
    date = st.session_state.get("report_date", dates[0])
    st.session_state["report_date"] = date
    analysis = load_analysis(date)
    st.session_state["analysis"] = analysis
    return analysis


def page_header(title: str, caption: str = ""):
    st.title(title)
    analysis = ensure_analysis()
    report_date = st.session_state.get("report_date", "N/A")
    budget_ghc = analysis.get("budget_ghc", 100_000)
    st.caption(f"Report: {report_date} | Budget: GHC {budget_ghc:,} (~$6,500 USD){' | ' + caption if caption else ''}")
    if not analysis:
        st.warning("No report data found. Run the pipeline first: `python scripts/run_pipeline.py`")
        st.stop()
    return analysis
