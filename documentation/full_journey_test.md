# 🚀 Scenario Test: Full Application Journey

## 📍 Type
End-to-End Test

## 📦 Associated Script
`tests/full_journey_test.py`

## 🔧 Preconditions
- Binary `gestion_stock.exe` must be compiled and located at `./build/`.
- Application must support simulated input for all menu options.
- Environment supports UTF-8 decoding across platforms.

## 🔄 Steps

1. Run the full journey test:

   ```bash
   py full_journey_test.py
   ```
2. The script simulates a full end-to-end journey through the CLI application:
   - Adds a new product (`Nom`, `Quantité`, `Prix`)
   - Lists current products to verify successful addition
   - Modifies the product by ID and confirms field updates
   - Deletes the product with confirmation
   - Exits the application cleanly

3. Watch the console output to ensure:
   - All prompts follow logical flow
   - Each operation gives correct feedback
   - Transitions between menu options function without error

## ✅ Expected Result
- Full product lifecycle completes without failure
- UI messages match expected language (e.g., "Produit modifié", "Produit supprimé")
- App terminates with a clean exit code and no dangling prompts

## ❌ Failure Scenarios
- ❌ Product not added, not listed, or not found during modification
- ❌ Deletion skipped or confirmation ignored
- ❌ Application enters invalid state or loops
- ❌ Incorrect output encoding or missing text

## 🧪 Notes
This test acts as:
- A sanity check for overall CLI integration
- A foundational smoke test for future automation pipelines
- A full demonstration of correct user workflow across core features
