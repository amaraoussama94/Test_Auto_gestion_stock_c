# 🧪 Test_Auto_gestion_stock_c

Automated testing suite for the [gestion_stock_c](https://github.com/amaraoussama94/gestion_stock_c) project, focused on verifying SQLite-backed product management operations.

This project includes functional, behavioral, and smoke tests designed to validate core CRUD workflows and binary stability in a clean, modular fashion.

---

## 🧩 Test Matrix: Objectives, Types & Status

| Test Script             | Type             | Objective                                                                  | Status   |
|------------------------|------------------|----------------------------------------------------------------------------|----------|
| `add_prod_test.py`     | Behavioral Test  | Simulate user-driven product addition via stdin                            | ✅ Done   |
| `smoke_test.py`        | Smoke Test       | Launch binary with test flag, confirm clean startup/shutdown               | ✅ Done   |
| `test_modification.py` | Functional Test  | Ensure product updates are properly persisted without side effects         | ⏳ Planned |
| `test_suppression.py`  | Functional Test  | Validate product deletion and confirm absence in DB and listing            | ⏳ Planned |
| `test_liste.py`        | Functional Test  | Compare product listing output with known data                             | ⏳ Planned |
| `full_journey_test.py` | Scenario Test    | Run complete user flow: add → modify → delete → list → quit                | 📝 Designed |
| `regression_db_crash.py`| Regression Test | Ensure past DB corruption bug no longer appears when deleting product      | 🧪 To be added |

✅ = Functional  
⏳ = In progress  
📝 = Design completed, implementation pending  
🧪 = Identified as useful test, not yet designed

---

## 📁 Project Structure

```text
Test_Auto_gestion_stock_c/
├── tests/                   # Bash-based functional tests
│   ├──add_prod_test.py         # Behavioral test: add product through stdin simulation
│   ├──smoke_test.py            # Smoke test: launch binary in test mode
│   ├── test_modification.py
│   ├── test_suppression.py
│   ├── test_liste.py
│   ├── full_journey_test.py
│   ├── regression_db_crash.py
│   └── common.py            # Shared helpers (DB reset, paths, etc.)
├── expected/                # Reference outputs for listing comparison
│   └── liste_sample.txt
├── run_tests.py             # Central runner with test summary
└── README.md                # This file
```
## Running Python Tests

Make sure gestion_stock_c binary is compiled and available in build/.

python3 add_prod_test.py
python3 smoke_test.py

##🔧 Running Shell-Based Tests (Planned)

bash run_tests.sh

##💡 Test Type Glossary

Functional Test: Verifies correctness of isolated functions or features.

Behavioral Test: Validates user-like interactions and system responsiveness.

Smoke Test: Checks basic health (launches, exits, CLI parsing).

Scenario Test: Simulates real-world multi-step usage.

Regression Test: Guards against recurrence of previously fixed bugs.

#🏗️ Planned Enhancements

✅ Migrate all tests to pure Python for cross-platform support

⚙️ Add test_common.py for reusable DB setup, teardown, and binary invocation

📊 Implement structured test reporting inside run_tests.py

🔄 Expand regression test coverage based on future bug fixes

## 🤖 Continuous Integration (CI)

## 📋 Test Report Summary

🚦 smoke_test.py ....................... ✅ PASSED
🧪 add_prod_test.py .................... ✅ PASSED
🧩 modify_prod_test.py ................. ⏳ SKIPPED
🧼 delete_prod_test.py ................. ⏳ SKIPPED

✔️ Total: 2 Passed / 2 Skipped / 0 Failed
