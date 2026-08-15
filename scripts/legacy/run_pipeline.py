"""
Master pipeline orchestrator for the TradeOps Intelligence System.
Run this script weekly (via Task Scheduler) or manually at any time.

Usage:
    python run_pipeline.py              # full run
    python run_pipeline.py --quick      # skip live API fetch, use cached data
"""
import argparse
import logging
import subprocess
import sys
import traceback
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from config import LOGS_DIR, REPORTS_DIR

LOGS_DIR.mkdir(parents=True, exist_ok=True)

_stdout_handler = logging.StreamHandler(sys.stdout)
_stdout_handler.stream.reconfigure(encoding="utf-8", errors="replace")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    handlers=[
        _stdout_handler,
        logging.FileHandler(LOGS_DIR / "pipeline.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)


def _git_push_reports(report_dir: Path):
    """Commit the new report folder and push to GitHub for Streamlit Cloud."""
    repo_root = Path(__file__).parent.parent
    try:
        # Check a remote exists before trying to push
        result = subprocess.run(
            ["git", "remote"], capture_output=True, text=True, cwd=repo_root
        )
        if not result.stdout.strip():
            logger.info("Git: no remote configured — skipping push. Add a GitHub remote to enable cloud sync.")
            return

        run_cmd = lambda args: subprocess.run(
            args, capture_output=True, text=True, cwd=repo_root, timeout=60
        )

        run_cmd(["git", "add", str(report_dir), "reports/"])
        commit = run_cmd([
            "git", "commit", "-m",
            f"Pipeline run {date.today()} — auto-update reports",
        ])
        if "nothing to commit" in commit.stdout:
            logger.info("Git: nothing new to commit.")
            return

        push = run_cmd(["git", "push"])
        if push.returncode == 0:
            logger.info("Git: reports pushed to GitHub -> Streamlit Cloud will update shortly.")
        else:
            logger.warning(f"Git push failed: {push.stderr.strip()}")
    except Exception as exc:
        logger.warning(f"Git sync skipped: {exc}")


def run(quick: bool = False):
    start = datetime.now()
    logger.info("=" * 60)
    logger.info(f"TradeOps Pipeline START — {date.today()}")
    logger.info("=" * 60)

    try:
        from fetch_ghana import fetch_ghana_data, save_ghana_data, get_latest_ghana_data
        from fetch_comtrade import fetch_comtrade_data, save_comtrade_data, get_latest_comtrade_data
        from fetch_prices import fetch_prices_data, save_prices_data, get_latest_prices_data
        from analyze_gaps import run_analysis
        from generate_report import generate_all_reports

        if quick:
            logger.info("Quick mode — loading cached data...")
            ghana_data = get_latest_ghana_data()
            comtrade_data = get_latest_comtrade_data()
            prices_data = get_latest_prices_data()
        else:
            logger.info("Step 1/5: Fetching Ghana macro trade data...")
            ghana_data = fetch_ghana_data()
            save_ghana_data(ghana_data)

            logger.info("Step 2/5: Fetching commodity trade data (Comtrade)...")
            comtrade_data = fetch_comtrade_data()
            save_comtrade_data(comtrade_data)

            logger.info("Step 3/5: Fetching commodity prices (FAOSTAT)...")
            prices_data = fetch_prices_data()
            save_prices_data(prices_data)

        logger.info("Step 4/5: Running gap analysis & opportunity scoring...")
        analysis = run_analysis(ghana_data, comtrade_data, prices_data)

        logger.info("Step 5/5: Generating reports...")
        report_dir = generate_all_reports(ghana_data, analysis)

        logger.info("Step 6/6: Exporting raw data to Excel...")
        try:
            from export_to_excel import export_report_to_excel
            excel_path = export_report_to_excel()
            if excel_path:
                logger.info(f"Excel workbook saved -> {excel_path}")
        except Exception as exc:
            logger.warning(f"Excel export skipped: {exc}")

        elapsed = (datetime.now() - start).seconds
        logger.info("=" * 60)
        logger.info(f"Pipeline COMPLETE in {elapsed}s")
        logger.info(f"Reports: {report_dir}")
        logger.info(f"Top opportunity: {analysis['top_5_overall'][0]['commodity'] if analysis['top_5_overall'] else 'N/A'}")
        logger.info("=" * 60)

        # Push updated reports to GitHub so Streamlit Cloud picks up the latest data
        _git_push_reports(report_dir)

        return True

    except Exception as e:
        logger.error(f"Pipeline FAILED: {e}")
        logger.error(traceback.format_exc())
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TradeOps weekly pipeline")
    parser.add_argument("--quick", action="store_true", help="Use cached data, skip API calls")
    args = parser.parse_args()
    success = run(quick=args.quick)
    sys.exit(0 if success else 1)
