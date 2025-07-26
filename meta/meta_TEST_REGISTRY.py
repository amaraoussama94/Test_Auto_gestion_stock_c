TEST_REGISTRY = {
    "Theem.py": {"run": False, "type": "non-test"},
    "smoke_test.py": {"run": True, "type": "ci"},
    "add_prod_test.py": {"run": True, "type": "ci"},
    "list_prod_test.py": {"run": True, "type": "ci"},
    "modify_prod_test.py": {"run": True, "type": "ci"},
    "delete_prod_test.py": {"run": True, "type": "ci"},
    "full_journey_test.py": {"run": False, "type": "weekly"},
    "regression_bug_test.py": {"run": True, "type": "ci"},
}
