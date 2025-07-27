TEST_REGISTRY = {
    "Theem.py": {"run": False, "type": "non-test"},
    "smoke_test.py": {
        "run": True,
        "type": "smoke",
        "expected_output": "Binary opened and exited cleanly"
    },
    "add_prod_test.py": {"run": True, "type": "ci", "expected_output": "Produit ajouté"},
    "list_prod_test.py": {"run": True, "type": "ci", "expected_output": "Liste des produits"},
    "modify_prod_test.py": {"run": True, "type": "ci", "expected_output": "Produit modifié"},
    "delete_prod_test.py": {"run": True, "type": "ci", "expected_output": "Produit supprimé"},
    "full_journey_test.py": {"run": False, "type": "weekly"},
    "regression_bug_test.py": {"run": True, "type": "ci", "expected_output": "Cas de bug résolu"},
}
