#!/usr/bin/env python3
"""Sync version across all project files."""

import re
import sys
from pathlib import Path


def read_version() -> str:
    """Read version from VERSION file."""
    version_file = Path(__file__).parent.parent / "VERSION"
    return version_file.read_text().strip()


def update_pyproject_toml(version: str) -> None:
    """Update version in pyproject.toml."""
    pyproject = Path(__file__).parent.parent / "python" / "pyproject.toml"
    content = pyproject.read_text()
    new_content = re.sub(
        r'version = "[^"]+"',
        f'version = "{version}"',
        content,
        count=1
    )
    pyproject.write_text(new_content)
    print(f"Updated python/pyproject.toml: {version}")


def update_package_json(version: str) -> None:
    """Update version in npm/package.json."""
    package_json = Path(__file__).parent.parent / "npm" / "package.json"
    content = package_json.read_text()
    new_content = re.sub(
        r'"version": "[^"]+"',
        f'"version": "{version}"',
        content,
        count=1
    )
    package_json.write_text(new_content)
    print(f"Updated npm/package.json: {version}")


def update_init_py(version: str) -> None:
    """Update version in __init__.py."""
    init_py = Path(__file__).parent.parent / "python" / "compass" / "__init__.py"
    content = init_py.read_text()
    new_content = re.sub(
        r'__version__ = "[^"]+"',
        f'__version__ = "{version}"',
        content
    )
    init_py.write_text(new_content)
    print(f"Updated python/compass/__init__.py: {version}")


def main():
    """Main entry point."""
    version = read_version()
    print(f"Syncing version: {version}")
    print()

    update_pyproject_toml(version)
    update_package_json(version)
    update_init_py(version)

    print()
    print("Version sync complete!")


if __name__ == "__main__":
    main()
