# 🧪 Scenario Test: Ajouter un Produit & Quitter

## 📍 Type
Scenario Test

## 📦 Associated Script
`tests/add_product_test.py`

## 🔧 Preconditions
- The binary `gestion_stock.exe` is compiled and located at `./build/`.
- The application supports simulated CLI input via standard input.
- No manual interaction required.

## 🔄 Steps

1. Execute the scenario script:
   ```bash
   py add_product_test.py

2. The script provides automated input to simulate the following user actions:
   - Select the “Ajouter un produit” option from the menu (`1`)
   - Enter product details:
     - Name: `Clavier`
     - Quantity: `25`
     - Price: `49.99`
   - Choose the “Quitter” option to exit the application (`0`)

3. Monitor for exit code and timeout exceptions.

## ✅ Expected Result
- Binary should process simulated input without hanging.
- Product should be added successfully in silent mode.
- Application exits cleanly with return code `0`.

## ❌ Failure Scenarios
- Timeout exceeded → Indicates blocking read or infinite loop.
- Non-zero return code → Possible error in input handling.
- Exception raised → Misconfiguration or missing binary.

## 🧪 Notes
This scenario validates:
- Command-line input parsing
- Menu-driven control flow
- Core product addition logic
- Graceful application termination
