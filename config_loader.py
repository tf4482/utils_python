"""
config_loader.py – Generic JSON configuration loader.

Usage in any project
--------------------
    from utils_python.config_loader import load_config

    CFG_DEFAULTS = {
        "MY_KEY": "placeholder-value",
        ...
    }

    cfg = load_config(
        app_name="my-app",
        config_filename="my-app-config.json",
        defaults=CFG_DEFAULTS,
    )
    MY_KEY = cfg["MY_KEY"]

Search order
------------
When ``config_path`` is supplied, only that exact path is loaded. Otherwise:

1. ``local_dir/config_filename`` when ``local_dir`` is supplied, or
   ``<directory of the calling script>/config_filename``
2. ``~/.config/app_name/config_filename``

If no file is found a placeholder is written to location 2 and
``SystemExit(1)`` is raised so the user can fill it in before restarting.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

from .filecheck import filecheck


def find_config_path(
    app_name: str,
    config_filename: str,
    *,
    caller_file: str | None = None,
    config_path: str | Path | None = None,
    local_dir: str | Path | None = None,
) -> Path | None:
    """Return the selected configuration path without loading or creating it."""
    if config_path is not None:
        candidate = Path(config_path).expanduser()
        return candidate if filecheck(str(candidate)) else None

    if local_dir is not None:
        base_dir = Path(local_dir).expanduser()
    elif caller_file is not None:
        base_dir = Path(caller_file).resolve().parent
    else:
        base_dir = Path(__file__).resolve().parent

    candidates = (
        base_dir / config_filename,
        Path.home() / ".config" / app_name / config_filename,
    )
    return next((path for path in candidates if filecheck(str(path))), None)


def load_config(
    app_name: str,
    config_filename: str,
    defaults: dict[str, Any],
    *,
    caller_file: str | None = None,
    config_path: str | Path | None = None,
    local_dir: str | Path | None = None,
) -> dict[str, Any]:
    """Locate, load and return the JSON configuration for *app_name*.

    Parameters
    ----------
    app_name:
        Short identifier used to build the user-level config directory
        (``~/.config/<app_name>/``).
    config_filename:
        Name of the JSON file, e.g. ``"myapp-config.json"``.
    defaults:
        Mapping written as a pretty-printed placeholder when no config
        file is found.  Keys whose values start with ``"your-"`` signal
        to the user that they must be replaced.
    caller_file:
        Pass ``__file__`` from the calling module so that the local
        (next-to-script) config path can be resolved correctly.
        Defaults to the directory that contains *this* module when
        omitted. Prefer ``local_dir`` when the application's local search
        directory is not the calling script's directory.
    config_path:
        Exact configuration path to load. No fallback or placeholder is
        used when this path is supplied.
    local_dir:
        Directory to search before the user-level path. This takes precedence
        over ``caller_file`` when both are supplied.

    Returns
    -------
    dict
        The parsed JSON object from the located config file.

    Raises
    ------
    SystemExit(1)
        When no config file exists.  A placeholder is created at the
        user-level path before exiting.
    """
    if config_path is not None:
        cfg_path = Path(config_path).expanduser()
        if not filecheck(str(cfg_path)):
            raise FileNotFoundError(f"Configuration file not found: {cfg_path}")
        with cfg_path.open(encoding="utf-8") as file:
            return json.load(file)

    if local_dir is not None:
        base_dir = Path(local_dir).expanduser()
    elif caller_file is not None:
        base_dir = Path(caller_file).resolve().parent
    else:
        base_dir = Path(__file__).resolve().parent

    user_cfg = Path.home() / ".config" / app_name / config_filename
    cfg_path = find_config_path(
        app_name,
        config_filename,
        caller_file=caller_file,
        local_dir=base_dir,
    )

    if cfg_path is None:
        user_cfg.parent.mkdir(parents=True, exist_ok=True)
        descriptor = os.open(user_cfg, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(descriptor, "w", encoding="utf-8") as file:
            json.dump(defaults, file, indent=2)
            file.write("\n")
        print(
            f"⚙️  No config file found. A placeholder has been created at:\n"
            f"   {user_cfg}\n"
            f"Please fill it in and restart the script."
        )
        sys.exit(1)

    with cfg_path.open(encoding="utf-8") as file:
        return json.load(file)
