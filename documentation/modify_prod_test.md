# 🧪 Scenario Test: Modifier un Produit

## 📍 Type
Scenario Test

## 📦 Associated Script
`tests/modify_prod_test.py`

## 🔧 Preconditions
- The binary `gestion_stock.exe` is compiled and located at `./build/`.
- The application supports simulated CLI input via standard input.
- At least one product with a known ID (e.g., `1`) should exist for a successful modification path.
- No manual interaction required.

## 🔄 Steps

1. Execute the scenario script:

   ```bash
   py modify_prod_test.py
   ```

2. The script provides automated input to simulate the following user actions for each ID in the range `1–5`:

   - Select the “Modifier un produit” option from the menu (`4`)
   - Provide a product ID (`1` to `5`)
   - If the ID is **valid**:
     - Update product details:
       - **Name**: `SuperModif`
       - **Quantity**: `99999`
       - **Price**: `999999.99`
     - Exit the application with option (`0`)
   - If the ID is **invalid**:
     - Expect the message: `ID invalide ou produit inexistant`

3. Monitor console output to detect:
   - ✅ Confirmation of successful modification
   - ❌ Error message for nonexistent product ID
   - ⚠️ Any unexpected or malformed console behavior


## ✅ Expected Result
- At least one valid product ID leads to:
  - A successful update of product information
  - Console output confirming the modification (e.g., "Produit modifié avec succès")
  - Exit code `0` indicating clean termination
- If no IDs are valid:
  - Each attempt prints: `ID invalide ou produit inexistant`
  - Script confirms expected behavior and completes without errors

## ❌ Failure Scenarios
- ⏱ **Timeout exceeded**: Indicates a blocking read or an input prompt not handled by the script
- 🔴 **Unexpected exit code**: Suggests an issue in input processing or command flow
- 💥 **No output match**: Could mean UI text has changed, or encoding issues interfere with detection
- ⚠️ **Silent failure**: No error but product not updated

## 🧪 Notes
This scenario validates:
- Menu navigation via CLI input
- Product ID verification logic
- Update logic for product attributes
- Output feedback for both success and error paths
- Graceful handling of invalid operations
