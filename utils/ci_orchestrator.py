"""
@file ci_orchestrator.py
@brief Coordinates version tagging, test execution, and report generation.
@details
This script serves as the central orchestrator for the CI pipeline. It pulls version
information from `utils/version.py`, executes all test scripts via `utils/test_runner.py`,
and formats the results into structured JSON and Markdown reports.

It ensures UTF-8 encoding, timestamped output, and modular separation of concerns.
Designed for automation and traceability in software testing workflows.

@note
- Requires `utils/version.py` to expose `extract_version_from_git()`.
- Requires `utils/test_runner.py` to expose `run_all_tests()`.
- Reports are saved in the `reports/` directory at the repository root.
"""

import os
import json
from datetime import datetime

# === IMPORT MODULES ===
from .version import extract_version_from_git
from .test_runner import run_all_tests

# === CONFIGURATION ===
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REPORT_DIR = os.path.join(REPO_ROOT, "reports")
os.makedirs(REPORT_DIR, exist_ok=True)

# === METADATA ===
version = extract_version_from_git()
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def delete_db_after_tests(build_dir="build", db_name="stockt.db"):
    """Deletes the temporary database file after tests.

    Args:
        build_dir (str): Directory where the database is located.
        db_name (str): Name of the database file to delete.
    """
    db_path = os.path.join(build_dir, db_name)
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"🧹 Deleted temporary DB: {db_path}")


def save_reports(results):
    """
    Saves test results to JSON and Markdown files.

    Args:
        results (list): List of test result dictionaries.
    """
    # JSON Report
    json_path = os.path.join(REPORT_DIR, f"{version}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "version": version,
            "timestamp": timestamp,
            "results": results
        }, f, indent=4, ensure_ascii=False)

    # Markdown Report
    md_path = os.path.join(REPORT_DIR, f"{version}.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# 🧪 Test Report Summary – Version {version}\n")
        f.write(f"**Date**: {timestamp}\n\n---\n\n## ✅ Test Results\n\n")
        f.write("| Script | Status | Duration |\n|--------|--------|----------|\n")
        for r in results:
            f.write(f"| {r['script']} | {r['status']} | {r['duration']} |\n")
        f.write("\n---\n\n## 📊 Summary\n")
        total = len(results)
        passed = sum(1 for r in results if r["status"] == "PASSED")
        skipped = sum(1 for r in results if r["status"] == "SKIPPED")
        failed = sum(1 for r in results if r["status"] == "FAILED")
        f.write(f"- **Total**: {total}\n- **Passed**: {passed}\n- **Skipped**: {skipped}\n- **Failed**: {failed}\n")

def main():
    """
    Main entry point for orchestrating CI workflow.
    """
    results = run_all_tests()
    save_reports(results)

if __name__ == "__main__":
    main()
