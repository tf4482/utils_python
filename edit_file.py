"""Open a file in an available terminal text editor."""

from __future__ import annotations

import os
import shlex
import shutil
import subprocess
from pathlib import Path


class EditorError(RuntimeError):
    """Raised when no suitable editor can be started."""


def preferred_editor() -> tuple[str, ...]:
    configured = os.environ.get("VISUAL") or os.environ.get("EDITOR")
    candidates = (configured, "nano", "vim", "vi")
    for candidate in candidates:
        if not candidate:
            continue
        command = tuple(shlex.split(candidate))
        if command and shutil.which(command[0]):
            return command
    raise EditorError("no terminal editor found; install nano, vim, or vi")


def edit_file(path: Path) -> None:
    """Open *path* in VISUAL, EDITOR, or the first available standard editor."""
    try:
        subprocess.run([*preferred_editor(), str(path)], check=True)
    except subprocess.CalledProcessError as error:
        raise EditorError(f"editor exited with status {error.returncode}") from error
