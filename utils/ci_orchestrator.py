"""
@file ci_orchestrator.py
@brief CI pipeline coordinator for tests, versioning, and reporting.
@details
This script coordinates version extraction, test orchestration, and report generation
for both routine and weekly validations. It defers `weekly` logic to utils/run_weekly.py,
but captures its result and integrates it into the reports directory.
"""

import os
import json
import argparse
import subprocess
from datetime import datetime

from .version import extract_version_from_git
from .test_runner import *

# === CONFIGURATION ===
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REPORT_DIR = os.path.join(REPO_ROOT, "reports")
os.makedirs(REPORT_DIR, exist_ok=True)

def delete_db_after_tests(build_dir="build", db_name="stockt.db"):
    """Deletes the temporary database file after tests."""
    db_path = os.path.join(build_dir, db_name)
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f" Deleted temporary DB: {db_path}")

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
            f.write(f"| {r['script']} | {r['status']} | {r.get('duration', 'N/A')} |\n")
        total = len(results)
        passed = sum(1 for r in results if r["status"] == "PASSED")
        skipped = sum(1 for r in results if r["status"] == "SKIPPED")
        failed = sum(1 for r in results if r["status"] == "FAILED")
        f.write("\n---\n\n## 📊 Summary\n")
        f.write(f"- **Total**: {total}\n- **Passed**: {passed}\n- **Skipped**: {skipped}\n- **Failed**: {failed}\n")

def run_weekly_test(version, timestamp):
    """Runs weekly validation script and stores its result."""
    script_path = os.path.join(REPO_ROOT, "utils", "run_weekly.py")
    print("[Weekly Mode] Delegating to run_weekly.py...")
    result=subprocess.run([sys.executable, "-m", "utils.run_weekly"], capture_output=True, text=True)
    print(f"[ Weekly Mode] result it...{result}")
    weekly_result = {
        "script": "run_weekly.py",
        "status": "PASSED" if result.returncode == 0 else "FAILED",
        "duration": "N/A",
        "stdout": result.stdout[:300],
        "stderr": result.stderr[:300]
    }

    save_reports([weekly_result], version, timestamp)

    if result.returncode != 0:
        print(" Weekly test failed.")
        exit(result.returncode)
    else:
        print(" Weekly test passed.")

def main():
    parser = argparse.ArgumentParser(description="Run CI pipeline or weekly test.")
    parser.add_argument("--weekly", action="store_true", help="Run full_journey_test weekly mode")
    args = parser.parse_args()

    version = extract_version_from_git()
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")

    if args.weekly:
        run_weekly_test(version, timestamp)
    else:
        results = run_all_tests()
        save_reports(results, version, timestamp)

if __name__ == "__main__":
    main()
