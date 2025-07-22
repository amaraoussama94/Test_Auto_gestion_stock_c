"""
@file list_prod_test.py
@brief Test script for listing products in gestion_stock application.
@details Simulates the “Lister les produits” option. Verifies that listed items include expected fields and reports any missing data.
@note Ensure the gestion_stock application is built and at least one product has been added for a full test.
"""

import subprocess
import sys
import os
import unicodedata
from Theem import run_theme_initialization_test

# 🔎 Resolve path to project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
BINARY_PATH = os.path.join(PROJECT_ROOT, 'build', 'gestion_stock.exe')

def normalize(text):
    """
    Normalizes accented characters and converts to lowercase for reliable comparison.
    """
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii').lower()

def run_listing_test():
    """
    Runs theme initialization, simulates option 2 (Lister les produits),
    and checks for presence of product field keywords.
    Prints which fields are missing if validation fails.
    """
    print(f"🚦 Launching theme initialization test: {BINARY_PATH}")
    if not run_theme_initialization_test():
        print("🚫 Échec lors de l'initialisation du thème.")
        sys.exit(1)

    # Simulate listing products and quitting
    input_sequence = "\n".join([
        "2",  # Menu: Lister les produits
        "0"   # Menu: Quitter
    ]) + "\n"

    try:
        proc = subprocess.Popen(
            [BINARY_PATH, "--test-mode"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8'  # ✅ Cross-platform UTF-8 decoding
        )
        stdout, _ = proc.communicate(input=input_sequence, timeout=10)
        print(f"📤 STDOUT:\n{stdout}")

        normalized = normalize(stdout)

        required_fields = ["liste des produits", "id", "nom", "quantite", "prix"]
        missing_fields = [field for field in required_fields if field not in normalized]

        if "liste des produits" in normalized:
            if not missing_fields:
                print("✅ Test réussi : tous les champs du produit sont présents dans la sortie.")
            else:
                print("⚠️ Test partiellement réussi : les champs suivants sont manquants ou mal encodés →")
                for field in missing_fields:
                    print(f"   ❌ Champ absent : {field}")
                sys.exit(1)
        else:
            print("❌ Aucun produit trouvé — pensez à en ajouter avant de relancer ce test.")
            sys.exit(1)

    except subprocess.TimeoutExpired:
        print("❌ Délai dépassé — vérifiez les blocages d'entrée ou pauses inattendues.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur inattendue : {e}")
        sys.exit(1)

if __name__ == '__main__':
    run_listing_test()
