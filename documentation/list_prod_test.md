# 🧪 Scenario Test: Lister les Produits

## 📍 Type
Scenario Test

## 📦 Associated Script
`tests/list_prod_test.py`

## 🔧 Preconditions
- The binary `gestion_stock.exe` is compiled and located at `./build/`.
- The application supports simulated CLI input via standard input.
- At least one product should exist for the successful listing path.
- The system running the test (Windows or Linux) must support UTF-8 encoding in console output.
- No manual interaction required.

## 🔄 Steps

1. Execute the scenario script:

   ```bash
   py list_prod_test.py
   ```
   
2. The script provides automated input to simulate the following user actions:
   - Select the “Lister les produits” option from the menu (`2`)
   - Exit the application using option (`0`)

3. Monitor console output to verify:
   - The presence of the section header: `Liste des produits`
   - Inclusion of expected product fields:
     - **ID**
     - **Nom**
     - **Quantité**
     - **Prix**
   - Accuracy of character encoding on both Linux and Windows environments

## ✅ Expected Result
- The application should display the list of products in the expected format.
- All required fields (`ID`, `Nom`, `Quantité`, `Prix`) must be present and correctly encoded.
- The application should terminate cleanly with an exit code of `0`.

## ❌ Failure Scenarios
- ❌ Missing section header → possible navigation issue or empty product list
- ❌ One or more product fields missing or garbled → may indicate encoding or formatting issues
- ❌ Timeout exceeded → blocking read or improper prompt handling
- ❌ Non-zero exit code → signifies input handling failure or CLI crash

## 🧪 Notes
This scenario validates:
- Product listing logic and menu flow
- Structural integrity of product output
- Encoding compatibility across platforms
- Field-level verification and graceful error handling
