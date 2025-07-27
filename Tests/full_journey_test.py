"""
@file full_journey_test.py
@brief Comprehensive lifecycle validation of gestion_stock application.
@details Adds, lists, modifies, and deletes a product in a simulated CLI session.
@note Split into two main functions for clarity and modularity.
"""

import subprocess
import sys
import os
import unicodedata
from datetime import datetime
import platform
import stat

# 📂 Determine project structure and binary path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BUILD_DIR = os.path.join(PROJECT_ROOT, "build")

if platform.system() == "Windows":
    BINARY_PATH = os.path.join(BUILD_DIR, "gestion_stock.exe")
else:
    BINARY_PATH = os.path.join(BUILD_DIR, "gestion_stock_linux")
    st = os.stat(BINARY_PATH)
    os.chmod(BINARY_PATH, st.st_mode | stat.S_IEXEC)

def normalize(text):
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii').lower()

def log_event(tag, message):
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"[{timestamp}] [{tag}] {message}")

def extract_first_product_id(output):
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
    normalized = normalize(output)
    success_prompts = ["produit ajoute", "liste des produits", "produit modifie", "produit supprime"]
    failure_signatures = ["erreur", "exception", "segfault", "inexistant", "crash"]
    allowed_invalid_contexts = ["entree invalide. veuillez entrer un entier non negatif"]

    for msg in success_prompts:
        if msg in normalized:
            log_event("CONFIRM", f"Detected: '{msg}'")

    missing_success = [msg for msg in success_prompts if msg not in normalized]
    detected_failures = [fail for fail in failure_signatures if fail in normalized]

    if "invalid" in normalized:
        for context in allowed_invalid_contexts:
            if context in normalized:
                log_event("INFO", f"Ignored benign validation prompt: '{context}'")
                detected_failures = [f for f in detected_failures if f != "invalid"]

    if missing_success:
        log_event("WARN", "Missing expected success indicators:")
        for msg in missing_success:
            log_event("WARN", f"    Absent: '{msg}'")

    if detected_failures:
        log_event("ERROR", "Failure indicators detected:")
        for fail in detected_failures:
            log_event("ERROR", f"    Found: '{fail}'")
        raise AssertionError("Test failed due to output anomalies.")

    log_event("PASS", " Full journey validated successfully.")

def add_and_list_product():
    """
    Adds a product and lists products to extract a valid ID.
    """
    log_event("START", f"Launching gestion_stock binary: {BINARY_PATH} (Add & List)")

    input_sequence = "\n".join([
        "1", "Clavier", "25", "49.99",  # Add product
        "2",                            # List products
        "0"                             # Quit
    ]) + "\n"

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

    product_id = extract_first_product_id(stdout)
    if product_id is None:
        log_event("FAIL", "No valid product found in range 1–5 to modify/delete.")
        sys.exit(1)

    log_event("INFO", f"Using dynamic product ID: {product_id}")
    return stdout + stderr, product_id

def modify_and_delete_product(product_id):
    """
    Modifies and deletes the product using the extracted ID.
    """
    log_event("START", f"Launching gestion_stock binary: {BINARY_PATH} (Modify & Delete)")

    input_sequence = "\n".join([
        "4", str(product_id), "Clavier RGB", "50", "59.99",  # Modify
        "3", str(product_id), "o",                           # Delete
        "0"                                                  # Quit
    ]) + "\n"

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

    return stdout + stderr

def run_full_journey():
    """
    Executes the full lifecycle in two stages.
    """
    try:
        output1, product_id = add_and_list_product()
        output2 = modify_and_delete_product(product_id)
        log_event("ANALYSIS", "Beginning output analysis...")
        analyze_output(output1 + output2)
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
