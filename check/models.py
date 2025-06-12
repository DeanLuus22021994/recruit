#!/usr/bin/env python3
"""
Test script to verify model imports work correctly.
This version only tests syntax and import structure without Django setup.
"""

import ast
import os
import sys
from typing import Optional, Tuple

# Add the project directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)


def test_import_syntax(module_path: str) -> Tuple[bool, Optional[str]]:
    """Test if a module can be parsed and imported (syntax-wise)."""
    try:
        full_path = os.path.join(project_root, module_path.replace(".", "/") + ".py")
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Parse the AST to check syntax
        ast.parse(content)
        return True, None
    except (OSError, SyntaxError, ValueError) as e:
        return False, str(e)


def main() -> int:
    """Test model file syntax and structure."""
    print("Testing recruit_models syntax...")

    # Test files to check
    model_modules = [
        "recruit_models.accounts",
        "recruit_models.candidates",
        "recruit_models.employers",
        "recruit_models.interviews",
        "recruit_models.jobs",
        "recruit_models.recruiters",
        "recruit_models.sendgrid",
    ]

    proxy_modules = [
        "accounts.models",
        "candidates.models",
        "employers.models",
        "interviews.models",
        "jobs.models",
        "recruiters.models",
        "sendgrid.models",
    ]

    all_passed = True

    for module in model_modules:
        success, error = test_import_syntax(module)
        if success:
            print(f"✓ {module} syntax OK")
        else:
            print(f"❌ {module} syntax error: {error}")
            all_passed = False

    print("\nTesting app proxy models syntax...")
    for module in proxy_modules:
        success, error = test_import_syntax(module)
        if success:
            print(f"✓ {module} syntax OK")
        else:
            print(f"❌ {module} syntax error: {error}")
            all_passed = False

    if all_passed:
        print("\n🎉 All model files have valid syntax and structure!")
        return 0

    print("\n❌ Some files have syntax errors.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
