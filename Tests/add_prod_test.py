"""
@brief Test script for adding a product in the gestion_stock application
@details This script simulates user input to add a product without an ID and then 
exits the application.    
@note Ensure the gestion_stock application is built and the binary path is correct.

"""
import subprocess
import sys
import os


# 🔎 Resolve path to project root, assuming script is in tests/
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
BINARY_PATH = os.path.join(PROJECT_ROOT, 'build', 'gestion_stock.exe')

# Simulate input: choice 1 → nom → quantite → prix → then quit with option 0
simulated_input = "\n".join([
    "1",           # Menu: Ajouter un produit
    "Clavier",     # Produit.nom
    "25",          # Produit.quantite
    "49.99",       # Produit.prix
    "0"            # Menu: Quitter
]) + "\n"

def run_scenario_test():
    try:
        print(f"🧪 Scenario: Ajouter un produit (sans ID) & quitter")
        proc = subprocess.Popen(
            [BINARY_PATH],
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            text=True
        )
        proc.communicate(simulated_input, timeout=10)
        if proc.returncode == 0:
            print("✅ Test réussi : produit ajouté et fermeture sans erreur.")
        else:
            print(f"⚠️ Code de sortie inattendu : {proc.returncode}")
            sys.exit(proc.returncode)
    except subprocess.TimeoutExpired:
        print("❌ Échec : délai dépassé — vérifiez les pauses ou les lectures bloquantes.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur inattendue : {e}")
        sys.exit(1)

if __name__ == '__main__':
    run_scenario_test()
