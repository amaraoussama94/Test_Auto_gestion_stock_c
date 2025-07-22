"""
@file full_journey_test.py
@brief End-to-end flow test for the gestion_stock application.
@details Validates full interaction path from product creation to deletion.
@note Useful for detecting integration failures across modules.
"""

import subprocess
import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
BINARY_PATH = os.path.join(PROJECT_ROOT, 'build', 'gestion_stock.exe')

def run_full_journey():
    """
    Simulates complete user journey in the CLI.
    Covers: Add → List → Modify → Delete → Quit
    """
    print(f"🚀 Launching full journey test: {BINARY_PATH}")

    input_sequence = "\n".join([
        "1",            # Ajouter
        "Souris",       # Nom
        "15",           # Quantité
        "29.99",        # Prix
        "2",            # Lister produits
        "",             # Return
        "4",            # Modifier
        "1",            # ID
        "Souris Pro",   # Nouveau nom
        "20",           # Nouvelle quantité
        "39.99",        # Nouveau prix
        "3",            # Supprimer
        "1",            # ID
        "o",            # Confirmation
        "0"             # Quitter
    ]) + "\n"

    try:
        proc = subprocess.Popen(
            [BINARY_PATH],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8'
        )
        stdout, _ = proc.communicate(input=input_sequence, timeout=15)
        print(f"📤 FULL JOURNEY OUTPUT:\n{stdout}")
    except Exception as e:
        print(f"❌ Full journey test encountered error: {e}")

if __name__ == "__main__":
    run_full_journey()
