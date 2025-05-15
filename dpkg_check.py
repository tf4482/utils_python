#!/usr/bin/env python3
import subprocess
import sys


def is_package_installed(package_name: str) -> bool:
    """
    Checks whether a Debian package is installed.
    Returns True if installed, False otherwise.

    Args:
        package_name (str): The name of the package to check.

    Returns:
        bool: True if the package is installed, False otherwise.
    """
    try:
        result = subprocess.run(
            ["dpkg", "-s", package_name],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return result.returncode == 0
    except FileNotFoundError:
        print("Error: 'dpkg' not found. Is this a Debian-based system?")
        return False


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <package-name>")
        sys.exit(1)

    package_name = sys.argv[1]
    if is_package_installed(package_name):
        print(f"Package '{package_name}' is installed.")
    else:
        print(f"Package '{package_name}' is NOT installed.")


if __name__ == "__main__":
    main()
