#!/usr/bin/env python3

import os
import sys

import yaml

TARGET_DIR = "/etc"


def deep_set(dic: dict, path: list[str], value: str):
    """Sets a value in a nested dictionary given a path list."""
    for key in path[:-1]:
        dic = dic.setdefault(key, {})
    dic[path[-1]] = value


def parse_key_value_list(settings: list[str]) -> dict:
    """
    Parses a list of key=value or key strings into a nested dictionary.
    If no value is provided, the key is assigned an empty string.
    """
    result = {}
    for item in settings:
        if "=" in item:
            key_path, value = item.split("=", 1)
            key_parts = key_path.strip().split(".")
            deep_set(result, key_parts, value.strip())
        else:
            key_parts = item.strip().split(".")
            deep_set(result, key_parts, "")
    return result


def create_config(filename: str, settings: list[str]) -> str:
    """
    Creates a .yml configuration file in TARGET_DIR with structured YAML content.

    Args:
        filename (str): The name of the configuration file (with or without .yml).
        settings (list[str]): List of key=value or key strings. Dot-separated keys define nesting.

    Returns:
        str: Full path to the created file.
    """
    if "." not in os.path.basename(filename):
        filename += ".yml"

    path = os.path.join(TARGET_DIR, filename)
    config_data = parse_key_value_list(settings)

    try:
        with open(path, "w") as f:
            yaml.dump(config_data, f, sort_keys=False)
    except PermissionError:
        raise PermissionError(f"No write permission for {path}. Please run as root.")
    except Exception as e:
        raise RuntimeError(f"Failed to write YAML file: {e}")

    return path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: sudo python3 create_yaml.py <filename> [key[=value]] ...")
        sys.exit(1)

    filename = sys.argv[1]
    args = sys.argv[2:]

    try:
        path = create_config(filename, args)
        print(f"YAML configuration file created: {path}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
