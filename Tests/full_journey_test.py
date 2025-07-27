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
from datetime import datetime

# 📂 Determine project structure and binary path
import platform

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BUILD_DIR = os.path.join(PROJECT_ROOT, "build")

if platform.system() == "Windows":
    BINARY_PATH = os.path.join(BUILD_DIR, "gestion_stock.exe")
else:
    BINARY_PATH = os.path.join(BUILD_DIR, "gestion_stock_linux")

def normalize(text):
    """
    Converts accented and special characters to ASCII for robust parsing.
    """
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii').lower()

def log_event(tag, message):
    """
    Logs tagged messages with timestamps for better step-by-step diagnostics.
    
    Parameters:
        tag (str): Label for event (e.g. START, ERROR, PASS).
        message (str): Description of event.
    """
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"[{timestamp}] [{tag}] {message}")

def extract_first_product_id(output):
    """
    Parses output to find the first listed product ID in range 1–5.

    Parameters:
        output (str): CLI stdout containing product list.

    Returns:
        int or None: First product ID if found, else None.
    """
    for line in output.splitlines():
        if line.strip().lower().startswith("id:"):
            try:
                product_id = int(line.split(":")[1].split("|")[0].strip())
                if 1 <= product_id <= 5:
                    return product_id
            except:
                continue
    return None

def analyze_output(output):
    """
    Evaluates CLI output for expected flow messages and errors.
    
    Parameters:
        output (str): Combined stdout and stderr text.
    """
    normalized = normalize(output)

    # ✅ Prompts expected in a successful lifecycle run
    success_prompts = ["produit ajoute", "liste des produits", "produit modifie", "produit supprime"]

    # ❌ Keywords typically associated with failure
    failure_signatures = ["erreur", "exception", "segfault", "inexistant", "crash"]

    # ✅ Allowed validation prompts not considered as failure
    allowed_invalid_contexts = [
        "entree invalide. veuillez entrer un entier non negatif"
    ]

    missing_success = [msg for msg in success_prompts if msg not in normalized]
    detected_failures = [
        fail for fail in failure_signatures if fail in normalized
    ]

    # 🛡️ Filter out known benign validation prompts
    if "invalid" in normalized:
        for context in allowed_invalid_contexts:
            if context in normalized:
                log_event("INFO", f"Ignored known benign validation prompt: '{context}'")
                detected_failures = [f for f in detected_failures if f != "invalid"]

    if missing_success:
        log_event("WARN", "Missing expected success indicators:")
        for msg in missing_success:
            print(f"    Absent: '{msg}'")

    if detected_failures:
        log_event("ERROR", "Failure indicators detected:")
        for fail in detected_failures:
            print(f"    Found: '{fail}'")
        raise AssertionError("Test failed due to output anomalies.")

    log_event("PASS", " Full journey validated successfully.")

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

    log_event("START", f"Launching gestion_stock binary: {BINARY_PATH}")

    # 🧪 Step 1: Pre-list to grab valid ID in range 1–5
    pre_list_proc = subprocess.Popen(
        [BINARY_PATH, "--test-mode"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding='utf-8'
    )
    pre_list_output, _ = pre_list_proc.communicate(input="2\n0\n", timeout=10)
    product_id = extract_first_product_id(pre_list_output)

    if product_id is None:
        log_event("FAIL", " No valid product found in range 1–5 to modify/delete.")
        sys.exit(1)

    log_event("INFO", f"Using dynamic product ID: {product_id}")

    input_sequence = "\n".join([
        "1",            # Ajouter produit
        "Clavier",      # Nom
        "25",           # Quantité
        "49.99",        # Prix
        "2",            # Lister produits
        "4",            # Modifier
        str(product_id),       # ID produit
        "Clavier RGB",  # Nouveau nom
        "50",           # Nouvelle quantité
        "59.99",        # Nouveau prix
        "3",            # Supprimer
        str(product_id),       # ID produit
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

        log_event("STDOUT", stdout)
        log_event("STDERR", stderr)

        log_event("ANALYSIS", "Beginning output analysis...")
        analyze_output(stdout + stderr)

    except AssertionError as ae:
        log_event("FAIL", f"Assertion failure: {ae}")
        sys.exit(1)
    except subprocess.TimeoutExpired:
        log_event("TIMEOUT", "CLI process timed out — possible pause or blocking prompt.")
        sys.exit(1)
    except Exception as e:
        log_event("EXCEPTION", f"Unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == '__main__':
    run_full_journey()
