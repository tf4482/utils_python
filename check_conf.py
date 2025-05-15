#!/usr/bin/env python3

import os
import sys

TARGET_DIR = "/etc"


def get_all_entries(conf_path: str) -> dict[str, str]:
    """
    Reads all key=value entries from a configuration file.

    Args:
        conf_path (str): Full path to the configuration file.

    Returns:
        dict[str, str]: Dictionary with keys and their corresponding values.
                        If a key has no value, value is empty string.
    """
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


def has_keys(
    filename: str, keys: list[str] | None = None
) -> dict[str, bool] | dict[str, str]:
    """
    Checks presence of specified keys in a config file in TARGET_DIR.
    If keys is None or empty, returns all key=value pairs.

    Args:
        filename (str): Config file name (with or without extension).
        keys (list[str] | None): Keys to check. If None or empty, return all entries.

    Returns:
        dict[str, bool]: Mapping of key -> True/False for presence of each key (if keys specified).
        dict[str, str]: All key=value pairs in the file (if no keys specified).

    Raises:
        FileNotFoundError: If config file not found.
        RuntimeError: For read/parse errors.
    """
    if "." not in os.path.basename(filename):
        filename += ".conf"

    conf_path = os.path.join(TARGET_DIR, filename)

    if not os.path.isfile(conf_path):
        raise FileNotFoundError(f"File does not exist: {conf_path}")

    entries = get_all_entries(conf_path)

    if not keys:
        return entries

    return {k: (k in entries) for k in keys}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python3 {sys.argv[0]} <filename> [key1] [key2] ...")
        sys.exit(1)

    filename = sys.argv[1]
    keys_to_check = sys.argv[2:]

    try:
        result = has_keys(filename, keys_to_check if keys_to_check else None)
        if isinstance(result, dict) and all(
            isinstance(v, str) for v in result.values()
        ):
            for key, value in result.items():
                print(f"{key}={value}")
            sys.exit(0)
        elif isinstance(result, dict):
            for key, present in result.items():
                print(f"{key}: {'True' if present else 'False'}")
            sys.exit(0 if all(result.values()) else 2)
        else:
            print(result)
            sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
