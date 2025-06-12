#!/usr/bin/env python3
"""
Simple syntax check for model files.
"""

import ast
import os
import sys
from typing import Optional, Tuple


def check_syntax(file_path: str) -> Tuple[bool, Optional[str]]:
    """Check if a Python file has valid syntax."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Try to parse the file
        ast.parse(content)
        return True, None
    except SyntaxError as e:
        return False, f"Syntax error in {file_path}: {e}"
    except (OSError, IOError, UnicodeDecodeError) as e:
        return False, f"Error reading {file_path}: {e}"


def main() -> int:
    """Check syntax of all model files."""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Files to check
    model_files = [
        "recruit_models/accounts.py",
        "recruit_models/candidates.py",
        "recruit_models/employers.py",
        "recruit_models/interviews.py",
        "recruit_models/jobs.py",
        "recruit_models/recruiters.py",
        "recruit_models/sendgrid.py",
        "accounts/models.py",
        "candidates/models.py",
        "employers/models.py",
        "interviews/models.py",
        "jobs/models.py",
        "recruiters/models.py",
        "sendgrid/models.py",
    ]

    print("Checking syntax of model files...")
    all_good = True

    for file_path in model_files:
        full_path = os.path.join(project_root, file_path)
        if os.path.exists(full_path):
            success, error = check_syntax(full_path)
            if success:
                print(f"✓ {file_path}")
            else:
                print(f"❌ {error}")
                all_good = False
        else:
            print(f"⚠️  {file_path} not found")

    if all_good:
        print("\n🎉 All model files have valid syntax!")
        return 0

    print("\n❌ Some files have syntax errors.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
