"""Script to check for package updates in requirements.txt file."""

import subprocess
import sys
from pathlib import Path
from typing import List, Optional, Tuple


def get_latest_version(package_name: str) -> Optional[str]:
    """Get the latest version of a package from PyPI."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "index", "versions", package_name],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")
            for line in lines:
                if line.startswith(f"{package_name} ("):
                    # Extract version from "package_name (version)"
                    return line.split("(")[1].split(")")[0]
        return None
    except (subprocess.TimeoutExpired, subprocess.SubprocessError):
        return None


def parse_requirements() -> List[Tuple[str, str]]:
    """Parse requirements.txt and return list of (package, current_version) tuples."""
    requirements_file = Path("requirements.txt")
    if not requirements_file.exists():
        print("requirements.txt not found!")
        return []

    packages: List[Tuple[str, str]] = []
    with open(requirements_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                if "==" in line:
                    package, version = line.split("==", 1)
                    packages.append((package.strip(), version.strip()))
    return packages


def main() -> None:
    """Main function to check for package updates."""
    packages = parse_requirements()
    if not packages:
        print("No packages found in requirements.txt")
        return

    updates_needed: List[Tuple[str, str, str]] = []

    print("Checking packages for updates...")
    for package, current_version in packages:
        print(f"Checking {package}...", end=" ")
        latest_version = get_latest_version(package)

        if latest_version and latest_version != current_version:
            updates_needed.append((package, current_version, latest_version))
            print(f"UPDATE AVAILABLE: {current_version} -> {latest_version}")
        elif latest_version:
            print("OK")
        else:
            print("FAILED TO CHECK")

    if updates_needed:
        print(f"\n{len(updates_needed)} packages need updates:")
        for package, _, latest in updates_needed:
            print(f"{package}=={latest}")
    else:
        print("\nAll packages are up to date!")


if __name__ == "__main__":
    main()
