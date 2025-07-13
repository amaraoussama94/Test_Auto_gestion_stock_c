import subprocess
import sys
import os

BINARY_PATH = os.path.join(os.path.dirname(__file__), 'build', 'gestion_stock')

def run_headless_test():
    try:
        print(f"🚦 Smoke test: launching {BINARY_PATH}")
        result = subprocess.run(
            [BINARY_PATH, "--test-mode"],
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
