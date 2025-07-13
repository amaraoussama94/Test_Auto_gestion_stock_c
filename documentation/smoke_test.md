# 🚦 Smoke Test: Binary Launch

## 📍 Type
Smoke Test

## 📦 Associated Script
`tests/smoke_test.py`

## 🔧 Preconditions
- The binary `gestion_stock` is compiled and located in `./build/`.
- The binary supports the `--test-mode` argument for a non-interactive dry run.
- No manual input is required for this test.

## 🔄 Steps

1. Execute the binary using:
   ```bash
   python3 smoke_test.py

2.  The process runs for up to 5 seconds with no user interaction.

3.  Monitor the return code to determine success.

## ✅ Expected Result
Binary should start and exit cleanly within the timeout period.

No crashes, hangs, or unexpected return codes.

Return code should be 0 indicating success.

## ❌ Failure Scenarios
Timeout exceeded (indicative of blocking input call or infinite loop)

Non-zero return code (may suggest error during startup)

## 🧪 Notes
This test helps confirm:

Basic CLI stability

Compatibility across platforms

That the binary is executable and responds to arguments properly

