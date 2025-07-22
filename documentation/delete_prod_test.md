# 🧪 Scenario: Supprimer un Produit

## 📄 Description
Tests the product deletion workflow in the `gestion_stock.exe` CLI application using simulated input. Validates error handling for nonexistent product IDs and confirms successful deletion feedback.

---

## 📍 Type
Scenario Test

## 🗂️ Script Location
`tests/delete_prod_test.py`

## 🧾 Preconditions
- ✅ The binary `gestion_stock.exe` is compiled and available at `./build/`
- ✅ CLI accepts simulated `stdin` input
- ✅ At least one valid product (e.g., `ID 10`) exists for successful deletion
- ✅ No manual interaction required

---

## 🛠️ Execution Steps

```bash
py delete_prod_test.py
```
For each product ID in `1–5`, the script performs:

1. **Accesses the main application menu** by launching the compiled binary.
2. **Navigates to menu option `3`** — _Supprimer un produit_.
3. **Inputs the product ID**, iterating through IDs `1` to `5`.
4. **Sends confirmation input (`o`)** when prompted to approve deletion.
5. **Chooses option `0`** to quit the application.

During execution, output is monitored and normalized to detect:

- ✅ `"Produit supprimé"` → confirms successful deletion
- ❌ `"ID invalide ou produit inexistant"` → confirms rejection of nonexistent product ID
- ⚠️ Unexpected or malformed output that may indicate an error or parsing issue

The script summarizes the results after all ID tests are complete.

---

## ✅ Expected Outcome

| Condition                      | Result                                                   |
|-------------------------------|-----------------------------------------------------------|
| Valid product found            | Output contains `"Produit supprimé"`                      |
| Invalid product ID             | Output contains `"ID invalide ou produit inexistant"`     |
| Binary exits cleanly           | Exit code `0`                                             |

---

## ❌ Failure Conditions

- ⏱ Timeout due to blocking prompt or unread input
- 🔴 Non-zero exit code from the binary
- 💥 Output not containing expected phrases
- ⚠️ No output or ambiguous feedback

---

## 📌 Test Coverage

✔ Menu navigation via CLI  
✔ Product ID input validation  
✔ Confirmation prompt detection  
✔ Deletion confirmation handling  
✔ Output normalization and parsing

---

## 📎 Notes

This scenario ensures that the application:
- Successfully deletes products when valid IDs are provided
- Gracefully handles attempts to delete nonexistent products
- Provides clear and parseable feedback via console output
