# 🧪 Test_Auto_gestion_stock_c

Automated testing suite for the [gestion_stock_c](https://github.com/amaraoussama94/gestion_stock_c) project, focused on verifying SQLite-backed product management operations.

This project includes functional, behavioral, and smoke tests designed to validate core CRUD workflows and binary stability in a clean, modular fashion.

---

## 🧩 Test Matrix: Objectives, Types & Status

| Test Script             | Type             | Objective                                                                  | Status   |
|------------------------|------------------|----------------------------------------------------------------------------|----------|
| `add_prod_test.py`     | Behavioral Test  | Simulate user-driven product addition via stdin                            | ✅ Done   |
| `smoke_test.py`        | Smoke Test       | Launch binary with test flag, confirm clean startup/shutdown               | ✅ Done   |
| `test_modification.py` | Functional Test  | Ensure product updates are properly persisted without side effects         | ✅ Done  |
| `test_suppression.py`  | Functional Test  | Validate product deletion and confirm absence in DB and listing            | ✅ Done |
| `test_liste.py`        | Functional Test  | Compare product listing output with known data                             | ✅ Done |
| `full_journey_test.py` | Scenario Test    | Run complete user flow: add → modify → delete → list → quit                | ✅ Done|
| `regression_db_crash.py`| Regression Test | Ensure past DB corruption bug no longer appears when deleting product      | ✅ Done|

✅ = Functional  
⏳ = In progress  
📝 = Design completed, implementation pending  
🧪 = Identified as useful test, not yet designed

---

## 📁 Project Structure

```text
Test_Auto_gestion_stock_c/
├── build/                       # Compiled gestion_stock_c binary output
├── expected/                    # Reference outputs for output comparison
│   └── liste_sample.txt         # Expected product listing sample
├── reports/                     # JSON + Markdown reports auto-generated by CI orchestrator
│   ├── v1.3.2.json              # Structured machine-readable report
│   └── v1.3.2.md                # Human-readable summary
├── utils/                       # Reusable test and CI coordination modules
│   ├── __init__.py              # Module initializer for relative imports
│   ├── test_runner.py           # Executes tests and collects structured results
│   ├── version.py               # Extracts Git version/tag info
│   └── ci_orchestrator.py       # Orchestrates testing and report generation
├── tests/                       # Python test scripts simulating CLI behavior
│   ├── add_prod_test.py         # Behavioral test: Add product via stdin
│   ├── smoke_test.py            # Smoke test: launch + exit
│   ├── test_modification.py     # Functional test: modify product
│   ├── test_suppression.py      # Functional test: delete product
│   ├── test_liste.py            # Functional test: list products
│   ├── full_journey_test.py     # Scenario test: full user flow
│   ├── regression_db_crash.py   # Regression test: past DB crash
│   └── common.py                # Shared utilities: DB setup, binary invocation
├── docs/                        # Markdown documents describing each test scenario
│   ├── add_prod_test.md
│   ├── smoke_test.md
│   ├── modify_prod_test.md
│   ├── delete_prod_test.md
│   ├── list_prod_test.md
│   ├── full_journey_test.md
│   └── regression_bug_test.md
├── run_tests.py                 # (Planned) Unified runner for shell-based scripts
└── README.md                    # Project overview and instructions

```
## Running Python Tests

Make sure gestion_stock_c binary is compiled and available in build/.

python3 add_prod_test.py
python3 smoke_test.py

##  🔧 Running Shell-Based Tests (Planned)

bash run_tests.sh

##  💡 Test Type Glossary

Functional Test: Verifies correctness of isolated functions or features.

Behavioral Test: Validates user-like interactions and system responsiveness.

Smoke Test: Checks basic health (launches, exits, CLI parsing).

Scenario Test: Simulates real-world multi-step usage.

Regression Test: Guards against recurrence of previously fixed bugs.

#  🏗️ Planned Enhancements

✅ Migrate all tests to pure Python for cross-platform support

⚙️ Add test_common.py for reusable DB setup, teardown, and binary invocation

📊 Implement structured test reporting inside run_tests.py

🔄 Expand regression test coverage based on future bug fixes

## 🧪 Running Tests via CLI

### 🔹 Prerequisites
- Ensure the `gestion_stock_c` binary is compiled and available in the `build/` directory.
- Python 3.8+ installed.
- All test scripts are located in the `tests/` directory.
- Reports will be saved in `reports/` with Git version tagging.

---

### 🚀 Run Individual Tests

Use this for debugging or focused validation:

---

⚠️ Windows Encoding Notice

If you're running tests on Windows and see garbled output or `UnicodeDecodeError` exceptions, set the Python environment encoding to UTF-8 before executing any scripts:

```powershell
$env:PYTHONIOENCODING = "utf-8"
```


```bash
py  tests/add_prod_test.py
py tests/test_modification.py
```

### 🧩 Run All Tests with CI Orchestrator

This command runs all Python tests and generates structured reports:

```bash
py utils/ci_orchestrator.py
```
It will:

- 📦 Extract the current Git version from your repository history.

- 🧪 Automatically discover and execute all Python test scripts located in `tests/`.

- 🧾 Collect results including pass/fail status, duration, and logs (stdout/stderr).

- 📋 Generate structured reports and save them to:

  - `reports/<version>.json` → machine-readable output for CI systems or analytics.

  - `reports/<version>.md` → human-readable Markdown summary for contributors and reviews.

- 💠 Use UTF-8 encoding for reliable cross-platform compatibility.

- 🕒 Timestamp each run to ensure traceability across versions and environments.

## 📋 Test Report Summary

🚦 smoke_test.py ....................... ✅ PASSED

🧪 add_prod_test.py .................... ✅ PASSED

🧩 modify_prod_test.py ................. ⏳ SKIPPED

🧼 delete_prod_test.py ................. ⏳ SKIPPED

✔️ Total: 2 Passed / 2 Skipped / 0 Failed
---
