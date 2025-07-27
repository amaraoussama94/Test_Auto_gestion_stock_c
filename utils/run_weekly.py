"""
@file ci_orchestrator.py
@brief Coordinates version tagging, test execution, and report generation.
@details
This script serves as the central orchestrator for the CI pipeline. It pulls version
information from `utils/version.py`, executes regular tests via `utils/test_runner.py`,
and defers weekly journey logic to `utils/run_weekly.py` for modularity.

Reports are saved under `reports/` (CI) or `weekly_test/` (weekly).
"""

import os
import json
import argparse
from datetime import datetime

from .version import extract_version_from_git
from .test_runner import (
    run_all_tests,
    write_report,
    write_log
)
from utils.run_weekly import run_weekly_test  # 🧪 Imported for clean orchestration

# === CONFIGURATION ===
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REPORT_DIR = os.path.join(REPO_ROOT, "reports")
os.makedirs(REPORT_DIR, exist_ok=True)

def delete_db_after_tests(build_dir="build", db_name="stockt.db"):
    """Deletes the temporary database file after tests."""
    db_path = os.path.join(build_dir, db_name)
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"🧹 Deleted temporary DB: {db_path}")

def save_reports(results, version, timestamp):
    """Saves results to JSON and Markdown files in `reports/`."""
    json_path = os.path.join(REPORT_DIR, f"{version}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "version": version,
            "timestamp": timestamp,
            "results": results
        }, f, indent=4, ensure_ascii=False)

    md_path = os.path.join(REPORT_DIR, f"{version}.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# 🧪 Test Report Summary – Version {version}\n")
        f.write(f"**Date**: {timestamp}\n\n---\n\n## ✅ Test Results\n\n")
        f.write("| Script | Status | Duration |\n|--------|--------|----------|\n")
        for r in results:
            f.write(f"| {r['script']} | {r['status']} | {r['duration']} |\n")
        total = len(results)
        passed = sum(1 for r in results if r["status"] == "PASSED")
        skipped = sum(1 for r in results if r["status"] == "SKIPPED")
        failed = sum(1 for r in results if r["status"] == "FAILED")
        f.write("\n---\n\n## 📊 Summary\n")
        f.write(f"- **Total**: {total}\n- **Passed**: {passed}\n- **Skipped**: {skipped}\n- **Failed**: {failed}\n")

def main():
    parser = argparse.ArgumentParser(description="Run CI pipeline or weekly test.")
    parser.add_argument("--weekly", action="store_true", help="Run full_journey_test weekly mode")
    args = parser.parse_args()

    if args.weekly:
        run_weekly_test()
    else:
        version = extract_version_from_git()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        results = run_all_tests()
        save_reports(results, version, timestamp)

if __name__ == "__main__":
    main()
