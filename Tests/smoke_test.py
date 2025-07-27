"""
@brief Smoke test for the gestion_stock application
@details This script runs a basic scenario to ensure the application starts and can handle user input.
@note Ensure the gestion_stock application is built and the binary path is correct.
"""
import subprocess
import sys
import os
#from Theem import run_theme_initialization_test

# 🔎 Resolve path to project root, assuming script is in tests/
import platform
import stat

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BUILD_DIR = os.path.join(PROJECT_ROOT, "build")

if platform.system() == "Windows":
    BINARY_PATH = os.path.join(BUILD_DIR, "gestion_stock.exe")
else:
    BINARY_PATH = os.path.join(BUILD_DIR, "gestion_stock_linux")
    #change permissions to make it executable ;chmod +x build/gestion_stock_linux
    st = os.stat(binary_path)
    os.chmod(binary_path, st.st_mode | stat.S_IEXEC)

def run_headless_test():
    try:
        print(f" Smoke test: launching {BINARY_PATH}")
        #if not run_theme_initialization_test():
        #    print(" Smoke test failed. Aborting further tests. Can select Theem")
        #    sys.exit(1)
        result = subprocess.run(
            [BINARY_PATH, "--test-smoke"],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=5
        )
        if result.returncode == 0:
            print(" Binary opened and exited cleanly.")
        else:
            print(f" Binary exited with return code {result.returncode}")
            sys.exit(result.returncode)
    except subprocess.TimeoutExpired:
        print(" Binary launch timed out — possible hang or input prompt.")
        sys.exit(1)
    except Exception as e:
        print(f" Unexpected error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    run_headless_test()
