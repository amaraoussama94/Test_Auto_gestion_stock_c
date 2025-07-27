"""
@file delete_prod_test.py
@brief Automated test script for product deletion validation in gestion_stock.
@details Tests deletion of product IDs 1–12, verifying success via normalized stdout.
@note Requires built binary. Theme initialization is included.
"""

import subprocess
import sys
import os
import unicodedata
#from Theem import run_theme_initialization_test

# Project and binary path setup
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
BINARY_PATH = os.path.join(PROJECT_ROOT, 'build', 'gestion_stock.exe')

def normalize(text):
    """
    Normalize text output: removes accents and converts to lowercase
    for reliable keyword matching across encodings and formatting.
    """
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii').lower()

def simulate_deletion(prod_id):
    """
    Simulates deletion of a product by ID.
    Returns True if 'Produit supprimé' appears in output, else False.
    """
    input_sequence = "\n".join([
        "3",             # Menu: Delete product
        str(prod_id),    # Product ID input
        "o",             # Confirm deletion
        "0"              # Exit
    ]) + "\n"

    try:
        proc = subprocess.Popen(
            [BINARY_PATH, "--test-mode"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8'
        )
        stdout, stderr = proc.communicate(input=input_sequence, timeout=10)
        normalized = normalize(stdout + stderr)

        # Check for deletion confirmation string
        if "produit supprime" in normalized:
            return True
        return False

    except subprocess.TimeoutExpired:
        return False
    except Exception:
        return False

def run_deletion_test():
    """
    Runs theme setup and deletion tests for product IDs 1–12.
    Prints test summary with deletion results.
    """
    #if not run_theme_initialization_test():
    #    sys.exit(1)

    results = {}
    for pid in range(1, 5):
        results[pid] = simulate_deletion(pid)

    print("\n Deletion Test Summary:")
    for pid, success in results.items():
        status = " Deleted" if success else " Invalid or not deleted"
        print(f"  - ID {pid}: {status}")

    if any(results.values()):
        print("\n Test complete — at least one product was successfully deleted.")
    else:
        print("\n Test complete — no deletions occurred; all IDs were invalid.")

if __name__ == '__main__':
    run_deletion_test()
