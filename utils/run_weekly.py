"""
@file utils/run_weekly.py
@brief Runs the full journey test suite and generates structured reports.
@details
This script is executed by the CI orchestrator to validate weekly application health.
It invokes the full journey tests using CLI arguments, captures output, logs results,
and generates structured reports in both TXT and JSON formats for traceability.
"""

import os
import sys
import json
import datetime
import subprocess

# 📍 Resolve repo root (parent of utils/)
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# 🗂️ Create weekly_test folder at root level
WEEKLY_DIR = os.path.join(REPO_ROOT, "weekly_test")
os.makedirs(WEEKLY_DIR, exist_ok=True)

# 📁 Get test folder path
test_dir = os.path.join(REPO_ROOT, "Tests")

# 🕒 Timestamp for report files
timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
log_path = os.path.join(WEEKLY_DIR, f"report_{timestamp}.txt")
json_path = os.path.join(WEEKLY_DIR, f"result_{timestamp}.json")

# 🧪 Run the weekly test command (customize if needed)
try:
    result = subprocess.run(
        ["python", os.path.join(test_dir, "full_journey_test.py")],
        capture_output=True,
        text=True,
        check=True
    )
    status = "success"

    # 📢 Echo live output to console
    print("\n STDOUT:")
    print(result.stdout)
    print("\n STDERR:")
    print(result.stderr)

except subprocess.CalledProcessError as e:
    result = e
    status = "fail"

    # 📢 Echo failure output to console
    print("\n STDOUT:")
    print(e.stdout)
    print("\n STDERR:")
    print(e.stderr)

# 📄 Save log output
with open(log_path, "w", encoding="utf-8") as log_file:
    log_file.write(result.stdout)
    log_file.write("\n--- STDERR ---\n")
    log_file.write(result.stderr)

# 📊 Save result metadata as JSON
metadata = {
    "status": status,
    "timestamp": timestamp,
    "command": result.args,
    "returncode": result.returncode,
    "stdout_summary": result.stdout[:300],  # Optional: truncate for overview
    "stderr_summary": result.stderr[:300]
}

with open(json_path, "w", encoding="utf-8") as json_file:
    json.dump(metadata, json_file, indent=2)

# 🔔 Exit code propagation (for CI feedback)
sys.exit(result.returncode)
