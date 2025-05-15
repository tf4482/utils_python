#!/usr/bin/env python3

import os
import sys


def create_conf(filename: str, settings: list[str]) -> str:
    """
    Creates a .conf configuration file in the TARGET_DIR directory on Debian-based systems.

    This function writes configuration entries to a file. Each entry can be either a key (flag-style)
    or a key=value pair. If the filename does not end with ".conf", the extension will be added automatically.

    Args:
        filename (str): The name of the configuration file to create (with or without .conf).
        settings (list[str]): A list of configuration entries. Each entry can be:
            - a standalone key (e.g., "debug") → will be written as "debug="
            - a key-value pair (e.g., "port=8080")

    Returns:
        str: The full path to the created configuration file.

    Raises:
        ValueError: If an entry contains an '=' but no key before it.
        PermissionError: If the process lacks write permission to the target directory.
        RuntimeError: If writing the file fails for any other reason.
    """

    TARGET_DIR = "/etc"

    if not filename.endswith(".conf"):
        filename += ".conf"

    conf_path = os.path.join(TARGET_DIR, filename)
    print(f"Writing configuration to: {conf_path}")

    try:
        with open(conf_path, "w") as f:
            for setting in settings:
                line = setting.strip()
                if not line:
                    continue
                if "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip()
                    if not key:
                        raise ValueError(f"Invalid configuration entry: '{setting}'")
                    f.write(f"{key}={value}\n")
                else:
                    f.write(f"{line}=\n")
    except PermissionError:
        raise PermissionError(
            f"No write permission for {conf_path}. Please run as root."
        )
    except Exception as e:
        raise RuntimeError(f"Failed to write configuration file: {e}")

    return conf_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage: sudo python3 create_conf.py <Filename> [KEY=VALUE]... or just [KEY]..."
        )
        sys.exit(1)

    filename = sys.argv[1]
    settings = sys.argv[2:]

    try:
        path = create_conf(filename, settings)
        print(f"Configuration file created: {path}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
