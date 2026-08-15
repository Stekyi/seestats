"""
Pipeline Control — manually trigger the TradeOps data pipeline and watch live output.
"""
import subprocess
import sys
import time
import streamlit as st
from pathlib import Path
from datetime import datetime

SCRIPTS_DIR = Path(__file__).parent.parent.parent / "scripts"
PIPELINE_SCRIPT = SCRIPTS_DIR / "run_pipeline.py"
LOGS_DIR = Path(__file__).parent.parent.parent / "logs"
LOG_FILE = LOGS_DIR / "pipeline.log"

st.set_page_config(page_title="Pipeline Control", page_icon="⚙️", layout="wide")

st.title("⚙️ Pipeline Control")
st.caption("Manually trigger the weekly data pipeline — fetch live data, run analysis, generate reports.")

# ─── Status ──────────────────────────────────────────────────────────────────
col_status, col_schedule = st.columns(2)
with col_status:
    st.markdown("**Automated schedule:** Every Friday at 21:00 (Windows Task Scheduler)")
with col_schedule:
    if LOG_FILE.exists():
        mtime = datetime.fromtimestamp(LOG_FILE.stat().st_mtime)
        st.markdown(f"**Last pipeline run:** {mtime.strftime('%A %d %b %Y at %H:%M')}")
    else:
        st.markdown("**Last pipeline run:** Never")

st.markdown("---")

# ─── Run options ─────────────────────────────────────────────────────────────
st.subheader("Run Options")
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Full run** — fetches live data from World Bank, Comtrade, FAOSTAT, then runs full analysis and generates reports. Takes 1-3 minutes.")
    run_full = st.button("▶ Run Full Pipeline", type="primary", use_container_width=True)

with col2:
    st.markdown("**Quick run** — skips live API calls, uses cached data from the last full run. Regenerates analysis and reports. Takes ~5 seconds.")
    run_quick = st.button("⚡ Quick Run (cached data)", use_container_width=True)

st.markdown("---")

# ─── Execution ───────────────────────────────────────────────────────────────
def run_pipeline(quick: bool = False):
    cmd = [sys.executable, str(PIPELINE_SCRIPT)]
    if quick:
        cmd.append("--quick")

    st.markdown("#### Live Output")
    output_box = st.empty()
    status_box = st.empty()
    lines = []
    start = time.time()

    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=str(SCRIPTS_DIR),
        )

        status_box.info("Pipeline running… do not close this tab.")

        for line in proc.stdout:
            line = line.rstrip()
            if line:
                lines.append(line)
                output_box.code("\n".join(lines[-60:]), language=None)

        proc.wait()
        elapsed = round(time.time() - start)

        if proc.returncode == 0:
            status_box.success(f"Pipeline completed successfully in {elapsed}s. Reload the dashboard to see new data.")
            st.balloons()
        else:
            status_box.error(f"Pipeline failed after {elapsed}s. Check the output above for errors.")

    except Exception as e:
        status_box.error(f"Failed to start pipeline: {e}")


if run_full:
    run_pipeline(quick=False)
elif run_quick:
    run_pipeline(quick=True)

# ─── Last log viewer ─────────────────────────────────────────────────────────
st.markdown("---")
with st.expander("📄 View Last Pipeline Log", expanded=False):
    if LOG_FILE.exists():
        log_text = LOG_FILE.read_text(encoding="utf-8", errors="replace")
        # Show last 150 lines
        log_lines = log_text.strip().splitlines()[-150:]
        st.code("\n".join(log_lines), language=None)
    else:
        st.info("No log file found yet. Run the pipeline at least once.")
