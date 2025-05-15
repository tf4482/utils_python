#!/usr/bin/env python3

import os
import sys

# Directory where config files are stored
TARGET_DIR = "/etc"


def get_all_entries(filename: str) -> dict[str, str]:
    """
    Reads all key=value entries from a configuration file in TARGET_DIR.

    Args:
        filename (str): Filename (with or without extension).

    Returns:
        dict[str, str]: Dictionary with keys and their corresponding values.
                        If a key has no value, the value is an empty string.

    Raises:
        FileNotFoundError: If the file does not exist.
        RuntimeError: On read or parse error.
    """
    if "." not in os.path.basename(filename):
        filename += ".conf"

    conf_path = os.path.join(TARGET_DIR, filename)

    if not os.path.isfile(conf_path):
        raise FileNotFoundError(f"File does not exist: {conf_path}")

    entries = {}
    try:
        with open(conf_path, "r") as f:
            for line in f:
                stripped = line.strip()
                if not stripped or stripped.startswith("#"):
                    continue
                if "=" in stripped:
                    key, value = stripped.split("=", 1)
                    entries[key.strip()] = value.strip()
                else:
                    entries[stripped] = ""
    except Exception as e:
        raise RuntimeError(f"Failed to read or parse {conf_path}: {e}")

    return entries


def has_all_keys(filename: str, keys: list[str]) -> bool:
    """
    Checks whether all specified keys exist in the config file
    and have non-empty, non-whitespace values.

    Args:
        filename (str): Filename (with or without extension).
        keys (list[str]): Keys to validate.

    Returns:
        bool: True if all keys are present and valid, False otherwise.
    """
    entries = get_all_entries(filename)
    return all(k in entries and entries[k].strip() != "" for k in keys)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python3 {sys.argv[0]} <filename> [key1] [key2] ...")
        sys.exit(1)

    filename = sys.argv[1]
    keys_to_check = sys.argv[2:]

    try:
        result = has_all_keys(filename, keys_to_check)
        print(result)
        sys.exit(0 if result else 2)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
