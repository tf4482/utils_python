#!/usr/bin/env python3

import sys
from pathlib import Path


def filecheck(filepath: str) -> bool:
    """
    Check if the given path exists and is a file.

    Args:
        filepath (str): The full path to the file.

    Returns:
        bool: True if the file exists and is a file, False otherwise.
    """
    return Path(filepath).is_file()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python filecheck.py <path_to_file>")
        sys.exit(1)
    print(filecheck(sys.argv[1]))
