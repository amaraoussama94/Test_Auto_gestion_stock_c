TEST_REGISTRY = {
    "Theem.py": {"run": False, "type": "non-test"},
    "add_prod_test.py": {"run": True, "type": "ci"},
    "delete_prod_test.py": {"run": True, "type": "ci"},
    "full_journey_test.py": {"run": False, "type": "weekly"},
    "list_prod_test.py": {"run": True, "type": "ci"},
    "modify_prod_test.py": {"run": True, "type": "ci"},
    "regression_bug_test.py": {"run": True, "type": "ci"},
    "smoke_test.py": {"run": True, "type": "ci"},
}
