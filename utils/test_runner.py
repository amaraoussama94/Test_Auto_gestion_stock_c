"""
@file utils/test_runner.py
@brief Utility to run and manage test scripts for the gestion_stock application.
@details
This script scans the 'Tests' directory for Python test scripts, executes each one,
captures its output, and returns a structured summary of results including status,
duration, and any output or errors.

It is designed to be run from the command line or imported as a module for integration
into larger CI workflows. The output can be redirected to JSON or Markdown reports
for traceability and analysis.

@note
Ensure all test scripts follow the naming convention '*.py' and reside in the 'Tests' directory.
"""

import subprocess
import os
import time
import sys
#to resolve uknowin package issue 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from meta.meta_TEST_REGISTRY import TEST_REGISTRY

from meta.meta_TEST_REGISTRY import TEST_REGISTRY

def run_test_script(script_path):
    """
    Executes a single test script and captures its output.

    Args:
        script_path (str): Full path to the test script.

    Returns:
        dict: A dictionary containing script name, status, duration, stdout, and stderr.
    """
    start = time.time()
    try:
        result = subprocess.run(
            ["python", script_path],
            capture_output=True,
            text=True,
            encoding="utf-8",  # 💡 Prevent UnicodeDecodeError on Windows
            timeout=10
        )
        duration = round(time.time() - start, 2)
        if "SKIP" in result.stdout:
            status = "SKIPPED"
        elif result.returncode == 0:
            status = "PASSED"
        else:
            status = "FAILED"
        stdout = result.stdout
        stderr = result.stderr
    except subprocess.TimeoutExpired:
        status = "TIMEOUT"
        duration = round(time.time() - start, 2)
        stdout = "Timeout"
        stderr = ""
    except Exception as e:
        status = "ERROR"
        duration = round(time.time() - start, 2)
        stdout = ""
        stderr = str(e)

    return {
        "script": os.path.basename(script_path),
        "status": status,
        "duration": f"{duration}s",
        "stdout": stdout,
        "stderr": stderr
    }

def get_repo_root():
    """
    Returns the absolute path to the repository root.

    Returns:
        str: Path to the root directory.
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def run_all_tests():
    """
    Discovers and runs all test scripts in the 'Tests' directory.

    Returns:
        list: A list of dictionaries containing results for each test script.
    """
    results = []
    test_dir = os.path.join(get_repo_root(), "Tests")

    if not os.path.isdir(test_dir):
        raise FileNotFoundError(f"Tests directory not found: {test_dir}")

    for script in sorted(os.listdir(test_dir)):
        if script.endswith(".py"):
            meta = TEST_REGISTRY.get(script, {"run": True, "type": "unknown"})
            if not meta["run"]:
                print(f"⏭️ Skipping: {script} [{meta['type']}]")
                continue
            full_path = os.path.join(test_dir, script)
            result = run_test_script(full_path)
            results.append(result)
    return results

def main():
    """
    Main entry point for executing all tests and printing results.
    """
    results = run_all_tests()
    for test in results:
        print(test)

if __name__ == '__main__':
    main()
