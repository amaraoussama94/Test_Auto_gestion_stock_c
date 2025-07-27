"""
@brief Test script for adding a product in the gestion_stock application
@details This script simulates user input to add a product without an ID and then 
exits the application.    
@note Ensure the gestion_stock application is built and the binary path is correct.

"""
import subprocess
import sys
import os
#from Theem import run_theme_initialization_test

# 🔎 Resolve path to project root, assuming script is in tests/
import platform

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BUILD_DIR = os.path.join(PROJECT_ROOT, "build")

if platform.system() == "Windows":
    BINARY_PATH = os.path.join(BUILD_DIR, "gestion_stock.exe")
else:
    BINARY_PATH = os.path.join(BUILD_DIR, "gestion_stock_linux")


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

        #if not run_theme_initialization_test():
        #    print(" Smoke test failed. Aborting further tests. Can select Theem")
        #    sys.exit(1)
        print(f" Scenario: Ajouter un produit (sans ID) & quitter")
        proc = subprocess.Popen(
            [BINARY_PATH, "--test-mode"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = proc.communicate(simulated_input, timeout=10)
        print(stdout)  # ← observe si le menu s'affiche

        if proc.returncode == 0:
            print(" Test réussi : produit ajouté et fermeture sans erreur.")
        else:
            print(f" Code de sortie inattendu : {proc.returncode}")
            sys.exit(proc.returncode)
    except subprocess.TimeoutExpired:
        print(" Échec : délai dépassé — vérifiez les pauses ou les lectures bloquantes.")
        sys.exit(1)
    except Exception as e:
        print(f" Erreur inattendue : {e}")
        sys.exit(1)

if __name__ == '__main__':
    run_scenario_test()
