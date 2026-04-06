"""
config_loader.py – Generic JSON configuration loader.

Usage in any project
--------------------
    from config_loader import load_config

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
1. ``<directory of the calling script>/config_filename``
2. ``~/.config/app_name/config_filename``

If no file is found a placeholder is written to location 2 and
``SystemExit(1)`` is raised so the user can fill it in before restarting.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


def load_config(
    app_name: str,
    config_filename: str,
    defaults: dict[str, Any],
    *,
    caller_file: str | None = None,
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
        omitted, which is usually wrong – always pass ``__file__``.

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
    base_dir   = Path(caller_file).parent if caller_file else Path(__file__).parent
    local_cfg  = base_dir / config_filename
    user_cfg   = Path.home() / ".config" / app_name / config_filename

    cfg_path = next((p for p in (local_cfg, user_cfg) if p.exists()), None)

    if cfg_path is None:
        user_cfg.parent.mkdir(parents=True, exist_ok=True)
        with open(user_cfg, "w", encoding="utf-8") as fh:
            json.dump(defaults, fh, indent=4)
        print(
            f"⚙️  No config file found. A placeholder has been created at:\n"
            f"   {user_cfg}\n"
            f"Please fill it in and restart the script."
        )
        sys.exit(1)

    with open(cfg_path, encoding="utf-8") as fh:
        return json.load(fh)
