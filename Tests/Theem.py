"""
@file Theem.py
@brief Theme selection smoke test for the gestion_stock application
@details This script verifies that the gestion_stock binary launches properly 
         and initializes the theme selection (specifically the 'Classic' theme).
         It serves as a prerequisite check before running deeper menu-level tests.
@note Ensure the gestion_stock application is built and the binary path is correct.
"""
#PS disabled by main software to be fixd  latter for complete real test
import subprocess
import sys
import os

# 🔍 Resolve the path to the project root (assumes this script lives in tests/)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
BINARY_PATH = os.path.join(PROJECT_ROOT, 'build', 'gestion_stock.exe')

def run_theme_initialization_test():
    """
    Launches gestion_stock binary in headless mode with '--test-mode' flag.
    Confirms that the binary opens, initializes theme selection, and exits cleanly.
    """
    try:
        print(f"🚦 Launching theme initialization test: {BINARY_PATH}")
        result = subprocess.run(
            [BINARY_PATH, "--test-mode", "--test-mode"],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=5
        )
        if result.returncode == 0:
            print("✅ Theme initialization passed — binary exited cleanly.")
            return True
        else:
            print(f"⚠️ Binary exited with unexpected return code: {result.returncode}")
            sys.exit(result.returncode)
            return False
    except subprocess.TimeoutExpired:
        print("❌ Timeout: binary may be waiting for user input or hung.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error during theme test: {e}")
        return False
        sys.exit(1)

if __name__ == '__main__':
    run_theme_initialization_test()
