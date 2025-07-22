"""
@file regression_bug_test.py
@brief Executes regression scenarios to confirm bug fixes remain effective. 
@details Validates historical issues by replaying triggering sequences and analyzing output.
@note Extend input sequences and output signatures as new bugs are resolved.
"""

import subprocess
import sys
import os

# 🔍 Establish project root and locate compiled binary
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
BINARY_PATH = os.path.join(PROJECT_ROOT, 'build', 'gestion_stock.exe')

def analyze_output(output):
    """
    Scans output for regression indicators or incomplete fixes.

    Parameters:
        output (str): Combined stdout and stderr output of the tested binary.

    Raises:
        AssertionError: If known error pattern or incomplete fix is detected.
    """
    known_error_signatures = [
        "Segmentation fault",
        "Memory corruption",
        "Unhandled exception",
        "Invalid input",
        "freeze",
        "crash"
    ]

    for signature in known_error_signatures:
        if signature.lower() in output.lower():
            raise AssertionError(f"❌ Regression detected: {signature}")

    # Optional: Validate known-good behavior
    if "Produit:" in output:
        print("✅ Product listing appears in output — logic intact.")
    else:
        print("⚠️ Expected listing output not found — verify edge case handling.")

def run_regression_test():
    """
    Runs CLI-based regression scenario targeting known fragile flows.
    Inputs simulate problematic sequences from past bug reports.
    """
    print(f"🐞 Starting regression bug test: {BINARY_PATH}")

    input_sequence = "\n".join([
        "2",     # Simulates listing products — common trigger area
        "",      # Blank input to test return-to-menu edge case
        "0"      # Exit command
    ]) + "\n"

    try:
        # 🚀 Launch the binary with piped input
        proc = subprocess.Popen(
            [BINARY_PATH, "--test-mode"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8'  # Ensures UTF-8 compatibility across systems
        )

        # 📥 Communicate inputs and receive program output
        stdout, stderr = proc.communicate(input=input_sequence, timeout=10)

        print(f"📤 STDOUT:\n{stdout}")
        print(f"📥 STDERR:\n{stderr}")

        # 🔍 Analyze combined output for known regression signs
        analyze_output(stdout + stderr)
        print("🧪 Regression test passed. No anomalies detected.")

    except AssertionError as ae:
        # ❌ Logic triggered a known bug signature
        print(str(ae))
    except Exception as e:
        # 🔥 Unforeseen crash or environment issue
        print(f"❌ Regression test failed due to unexpected error: {e}")

if __name__ == "__main__":
    run_regression_test()
