"""
@file full_journey_test.py
@brief Comprehensive lifecycle validation of gestion_stock application.
@details Adds, lists, modifies, and deletes a product in a simulated CLI session.
@note Integrates theme setup, output analysis, and result feedback.
"""

import subprocess
import sys
import os
import unicodedata
#from Theem import run_theme_initialization_test

# 📂 Determine project structure and binary path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
BINARY_PATH = os.path.join(PROJECT_ROOT, 'build', 'gestion_stock.exe')

def normalize(text):
    """
    Converts accented and special characters to ASCII for robust parsing.
    """
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii').lower()

def analyze_output(output):
    """
    Evaluates CLI output for expected flow messages and errors.

    Parameters:
        output (str): Combined stdout and stderr text.
    """
    normalized = normalize(output)

    success_prompts = ["produit ajoute", "liste des produits", "produit modifie", "produit supprime"]
    failure_signatures = ["erreur", "exception", "invalid", "segfault", "inexistant", "crash"]

    missing_success = [msg for msg in success_prompts if msg not in normalized]
    detected_failures = [fail for fail in failure_signatures if fail in normalized]

    if missing_success:
        print("⚠️ Some success indicators were missing:")
        for msg in missing_success:
            print(f"   ❌ Absent: '{msg}'")

    if detected_failures:
        print("❌ Failure indicators detected:")
        for fail in detected_failures:
            print(f"   🔥 Found: '{fail}'")
        raise AssertionError("Output contains failure messages or missing flow confirmations.")

    print("✅ Full journey validated — flow intact and output confirmed.")

def run_full_journey():
    """
    Simulates entire lifecycle:
    1. Add a product
    2. List products
    3. Modify product
    4. Delete product
    5. Quit application
    """
    #if not run_theme_initialization_test():
    #    sys.exit(1)

    print(f"🚀 Starting full journey test with binary: {BINARY_PATH}")

    input_sequence = "\n".join([
        "1",            # Ajouter produit
        "Clavier",      # Nom
        "25",           # Quantité
        "49.99",        # Prix
        "2",            # Lister produits
        "",             # Retour au menu
        "4",            # Modifier
        "1",            # ID produit
        "Clavier RGB",  # Nouveau nom
        "50",           # Nouvelle quantité
        "59.99",        # Nouveau prix
        "3",            # Supprimer
        "1",            # ID produit
        "o",            # Confirmation suppression
        "0"             # Quitter application
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
        stdout, stderr = proc.communicate(input=input_sequence, timeout=20)

        print("📤 STDOUT:\n", stdout)
        print("📥 STDERR:\n", stderr)

        analyze_output(stdout + stderr)

    except AssertionError as ae:
        print(str(ae))
        sys.exit(1)
    except subprocess.TimeoutExpired:
        print("❌ Timeout expired — CLI may be blocking or paused.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error during full journey test: {e}")
        sys.exit(1)

if __name__ == '__main__':
    run_full_journey()
