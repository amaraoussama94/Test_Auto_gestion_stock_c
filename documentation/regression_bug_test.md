# 🐞 Scenario Test: Regression Bug Validation

## 📍 Type
Regression Test

## 📦 Associated Script
`tests/regression_bug_test.py`

## 🔧 Preconditions
- Binary `gestion_stock.exe` must be compiled and located at `./build/`.
- Any known bugs being tested should have clear reproduction steps documented.
- The CLI must accept standard input automation.
- Environment must support UTF-8 decoding across platforms.

## 🔄 Steps

1. Execute the regression script:

   ```bash
   py regression_bug_test.py
   ```


2. The script provides automated input to simulate actions known to have triggered bugs:
   - Use edge cases such as invalid IDs, empty fields, or rapid menu switching
   - Reproduce exact sequences from historical bug reports
   - Include specific test payloads to challenge previously fragile logic

3. Observe output and verify:
   - No recurrence of previous error messages or crashes
   - Input handling and UI feedback behave as expected
   - Error messages are informative, if triggered

## ✅ Expected Result
- Application no longer reproduces previously reported issues
- All relevant fixes remain effective
- No new regressions introduced

## ❌ Failure Scenarios
- ❌ Message like "Segmentation fault" or corrupted memory
- ❌ Broken prompts, frozen input, or silent failure
- ❌ Reappearance of known bugs or incomplete fixes

## 🧪 Notes
This regression test helps ensure:
- Long-term reliability across releases
- Verification of bug fixes from prior issues
- Confidence in changes introduced in refactoring or optimization

    