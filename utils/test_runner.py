"""
@file utils/test_runner.py
@brief Utility to run and manage test scripts for the gestion_stock application.

@details
Executes test scripts listed in TEST_REGISTRY in defined order, captures output,
verifies expected behavior, logs test-specific details, and returns structured results.

@note
Ensure all test scripts follow the '*.py' naming convention and reside in the 'Tests' directory.
Test runner logs stdout, stderr, execution time, database status, and environment diagnostics.
"""

import subprocess
import os
import time
import sys
import datetime

# Extend path to resolve package imports from repo root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from meta.meta_TEST_REGISTRY import TEST_REGISTRY

def get_repo_root():
    """
    Returns the absolute path to the repository root.
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def run_test_script(script_path, db_filename="stockt.db", expected_output="Produit ajouté"):
    """
    Executes a single test script, validates output, and logs diagnostic info.

    Args:
        script_path (str): Full path to the test script.
        db_filename (str): Name of the expected database file.
        expected_output (str): Message expected to confirm success.

    Returns:
        dict: Result summary including script name, status, duration, output path, and errors.
    """
    start_time = time.time()
    script_name = os.path.basename(script_path)
    build_dir = os.path.join(get_repo_root(), "build")
    logs_dir = os.path.join(build_dir, "logs")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_path = os.path.join(logs_dir, f"{script_name.replace('.py','')}_{timestamp}.log")

    os.makedirs(logs_dir, exist_ok=True)

    try:
        completed = subprocess.run(
            ["python", script_path],
            cwd=build_dir,
            capture_output=True,
            text=True,
            encoding="utf-8",  # 👈 force decoding
            timeout=300
        )

        stdout = completed.stdout.strip()
        stderr = completed.stderr.strip()
        db_path = os.path.join(build_dir, db_filename)
        db_exists = os.path.exists(db_path)

        # Diagnostic logging
        with open(log_path, "w", encoding="utf-8") as log_file:
            log_file.write(f"[{timestamp}] Running: {script_name}\n")
            log_file.write(f"📁 Working Directory: {build_dir}\n")
            log_file.write(f"📦 DB File: {db_filename} | Exists: {db_exists}\n\n")
            log_file.write("📤 STDOUT:\n" + stdout + "\n\n")
            log_file.write("❌ STDERR:\n" + stderr + "\n\n")
            log_file.write(f"🔚 Exit Code: {completed.returncode}\n")
            log_file.write(f"🔎 Output Check: {'✓ Found' if expected_output in stdout else '✗ Not Found'}\n")

        # Status evaluation
        if completed.returncode == 0 and expected_output in stdout and db_exists:
            status = "✅ Passed"
        else:
            status = "❌ Failed"

        return {
            "script": script_name,
            "status": status,
            "duration": round(time.time() - start_time, 2),
            "log": log_path
        }

    except Exception as e:
        return {
            "script": script_name,
            "status": "⚠️ Error",
            "duration": round(time.time() - start_time, 2),
            "log": log_path,
            "error": str(e)
        }

def run_all_tests():
    """
    Executes all test scripts defined in TEST_REGISTRY and logs results per test.

    Returns:
        list: A list of result dictionaries including logs for each test case.
    """
    results = []
    test_dir = os.path.join(get_repo_root(), "Tests")

    if not os.path.isdir(test_dir):
        raise FileNotFoundError(f"Tests directory not found: {test_dir}")

    for script_name, meta in TEST_REGISTRY.items():
        if not meta["run"]:
            print(f"⏭️ Skipping: {script_name} [{meta['type']}]")
            continue

        full_path = os.path.join(test_dir, script_name)
        if not os.path.isfile(full_path):
            print(f"⚠️ Missing test script: {script_name}")
            continue

        result = run_test_script(full_path, expected_output=meta.get("expected_output"))
        results.append(result)

    return results

def main():
    """
    Entry point for executing all registered tests and printing detailed results.
    """
    results = run_all_tests()
    for test in results:
        print(f"{test['script']}: {test['status']} ({test['duration']}s)")
        print(f"↪ Log file: {test['log']}\n")
        if test.get("error"):
            print(f"⚠️ Error: {test['error']}\n")

if __name__ == "__main__":
    main()
