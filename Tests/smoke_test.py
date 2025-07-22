"""
@brief Smoke test for the gestion_stock application
@details This script runs a basic scenario to ensure the application starts and can handle user input.
@note Ensure the gestion_stock application is built and the binary path is correct.
"""
import subprocess
import sys
import os
from Theem import run_theme_initialization_test

# 🔎 Resolve path to project root, assuming script is in tests/
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
BINARY_PATH = os.path.join(PROJECT_ROOT, 'build', 'gestion_stock.exe')

def run_headless_test():
    try:
        print(f"🚦 Smoke test: launching {BINARY_PATH}")
        if not run_theme_initialization_test():
            print("🚫 Smoke test failed. Aborting further tests. Can select Theem")
            sys.exit(1)
        result = subprocess.run(
            [BINARY_PATH, "--test-mode", "--test-mode"],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=5
        )
        if result.returncode == 0:
            print("✅ Binary opened and exited cleanly.")
        else:
            print(f"⚠️ Binary exited with return code {result.returncode}")
            sys.exit(result.returncode)
    except subprocess.TimeoutExpired:
        print("❌ Binary launch timed out — possible hang or input prompt.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    run_headless_test()
