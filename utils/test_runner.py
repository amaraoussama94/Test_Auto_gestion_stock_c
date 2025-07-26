"""
@file utils/test_runner.py
@brief Utility to run and manage test scripts for the gestion_stock application.
@details
Executes test scripts listed in TEST_REGISTRY in defined order, captures output,
and returns structured results including status, duration, and errors.

@note
Ensure all test scripts follow the '*.py' naming convention and reside in the 'Tests' directory.
"""

import subprocess
import os
import time
import sys

# Resolve unknown package issue
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from meta.meta_TEST_REGISTRY import TEST_REGISTRY

def get_repo_root():
    """
    Returns the absolute path to the repository root.
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def run_test_script(script_path):
    """
    Executes a single test script and captures its output.

    Args:
        script_path (str): Full path to the test script.

    Returns:
        dict: Result summary including script name, status, duration, and output.
    """
    start_time = time.time()
    script_name = os.path.basename(script_path)

    try:
        completed = subprocess.run(
            ["python", script_path],
            capture_output=True,
            text=True,
            timeout=300
        )
        status = "✅ Passed" if completed.returncode == 0 else "❌ Failed"
        output = completed.stdout + completed.stderr
    except Exception as e:
        status = "⚠️ Error"
        output = str(e)

    return {
        "script": script_name,
        "status": status,
        "duration": round(time.time() - start_time, 2),
        "output": output.strip()
    }

def run_all_tests():
    """
    Executes test scripts in the exact order defined in TEST_REGISTRY.

    Returns:
        list: A list of dictionaries containing results for each test script.
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

        result = run_test_script(full_path)
        results.append(result)

    return results

def main():
    """
    Main entry point for executing all tests and printing results.
    """
    results = run_all_tests()
    for test in results:
        print(f"{test['script']}: {test['status']} ({test['duration']}s)")
        if test['status'] != "✅ Passed":
            print(f"↪ Output:\n{test['output']}\n")

if __name__ == "__main__":
    main()
