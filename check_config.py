#!/usr/bin/env python3

import os
import sys

import yaml

TARGET_DIR = "/etc"


def is_filled(value) -> bool:
    """
    Checks if a value is considered non-empty.
    Empty strings or whitespace-only strings are considered empty.
    """
    if isinstance(value, str):
        return value.strip() != ""
    return value is not None


def all_keys_have_values(data) -> bool:
    """
    Recursively checks if all keys in the given YAML dictionary have non-empty values.
    """
    if isinstance(data, dict):
        return all(all_keys_have_values(v) for v in data.values())
    elif isinstance(data, list):
        return all(all_keys_have_values(v) for v in data)
    else:
        return is_filled(data)


def has_all_yaml_values(filename: str) -> bool:
    """
    Loads a YAML file from TARGET_DIR and checks if all keys have non-empty values.

    Args:
        filename (str): Filename with or without .yml extension.

    Returns:
        bool: True if all keys have non-empty values, False otherwise.

    Raises:
        FileNotFoundError: If the YAML file does not exist.
        yaml.YAMLError: If the file cannot be parsed.
    """
    if "." not in os.path.basename(filename):
        filename += ".yml"

    yaml_path = os.path.join(TARGET_DIR, filename)

    if not os.path.isfile(yaml_path):
        raise FileNotFoundError(f"File not found: {yaml_path}")

    with open(yaml_path, "r") as f:
        content = yaml.safe_load(f)

    return all_keys_have_values(content)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} <filename>")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        result = has_all_yaml_values(filename)
        print("True" if result else "False")
        sys.exit(0 if result else 2)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
