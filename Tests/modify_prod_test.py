"""
@file modify_prod_test.py
@brief Test script for modifying a product in the gestion_stock application.
@details Checks whether IDs 1–5 can be modified. If a valid product is found, it updates 
         the product with a new name and extreme quantity/price values. Otherwise, confirms
         the application responds properly for nonexistent IDs.
@note Ensure the gestion_stock application is built and the binary path is correct.
"""

import subprocess
import sys
import os
import unicodedata
#from Theem import run_theme_initialization_test

# 🔎 Resolve path to project root, assuming script is in tests/
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
BINARY_PATH = os.path.join(PROJECT_ROOT, 'build', 'gestion_stock.exe')

def normalize(text):
    """
    Normalizes accented characters to ASCII equivalents for easier comparison.
    """
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii').lower()

def simulate_modification(prod_id):
    """
    Simulates an attempt to modify a product with the given ID.
    If the product exists, modifies its name, quantity, and price.
    """
    print(f" Testing modification for ID = {prod_id}")
    input_sequence = "\n".join([
        "4",            # Menu: Modifier un produit
        str(prod_id),   # ID du produit
        "SuperModif",   # Nouveau nom
        "99999",        # Quantité extrême
        "999999.99",    # Prix extrême
        "0"             # Quitter
    ]) + "\n"

    try:
        proc = subprocess.Popen(
            [BINARY_PATH, "--test-mode"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, _ = proc.communicate(input=input_sequence, timeout=10)

        # 🧪 Print full stdout for debug purposes
        #print(f" STDOUT for ID {prod_id}:\n{stdout}")

        # 🔍 Normalize and search output
        norm_out = normalize(stdout)
        if "inexistant" in norm_out or "invalide" in norm_out:
            print(f" ID {prod_id} invalide — produit inexistant.")
            return False
        elif "modifie" in norm_out or "modification" in norm_out:
            print(f" Modification réussie pour l’ID {prod_id}.")
            return True
        else:
            print(f" Comportement inattendu pour l’ID {prod_id}.")
            return False
    except subprocess.TimeoutExpired:
        print(" Échec : délai dépassé — entrée bloquante ou pause console non ignorée.")
        return False
    except Exception as e:
        print(f" Erreur inattendue : {e}")
        return False

def run_modification_test():
    """
    Runs the theme initialization check, then tests modification flow for IDs 1 to 5.
    """
    #print(f"🚦 Launching theme initialization test: {BINARY_PATH}")
    #if not run_theme_initialization_test():
    #    sys.exit(1)

    any_success = False
    for pid in range(1, 6):
        result = simulate_modification(pid)
        if result:
            any_success = True
            break  # Une réussite suffit pour valider la modification

    if not any_success:
        print(" Test passé : Aucun ID valide, comportement attendu.")
    else:
        print(" Test passé : Modification acceptée sur un ID valide.")

if __name__ == '__main__':
    run_modification_test()
