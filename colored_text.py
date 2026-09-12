#!/usr/bin/python3

from __future__ import annotations

import os
import sys
from typing import TextIO

from .convert_to_string import convert_to_string

COLOR_CODES = {
    "black": "\033[0;30m",
    "red": "\033[0;31m",
    "green": "\033[0;32m",
    "yellow": "\033[0;33m",
    "blue": "\033[0;34m",
    "magenta": "\033[0;35m",
    "cyan": "\033[0;36m",
    "lgrey": "\033[0;37m",
    "grey": "\033[1;90m",
    "lred": "\033[1;91m",
    "lgreen": "\033[1;92m",
    "lyellow": "\033[1;93m",
    "lblue": "\033[1;94m",
    "lmagenta": "\033[1;95m",
    "lcyan": "\033[1;96m",
    "white": "\033[1;97m",
}
RESET = "\033[0m"


def check_type(input_data):
    """
    Convert input data to a string.

    Args:
        input_data: The data to convert.

    Returns:
        str: String representation of the input data.
    """

    if isinstance(input_data, (dict, list, tuple, set)):
        return convert_to_string(input_data)
    return str(input_data)


def supports_color(stream: TextIO | None = None) -> bool:
    """Return whether *stream* supports ANSI colors and colors are enabled."""
    target = stream or sys.stdout
    return (
        "NO_COLOR" not in os.environ
        and os.environ.get("TERM") != "dumb"
        and target.isatty()
    )


def colorize(
    input_data,
    color: str,
    *,
    enabled: bool | None = None,
    stream: TextIO | None = None,
) -> str:
    """Return input data wrapped in an ANSI color when color is enabled."""
    text = check_type(input_data)
    use_color = supports_color(stream) if enabled is None else enabled
    code = COLOR_CODES.get(color)
    return f"{code}{text}{RESET}" if use_color and code else text


def output(
    color: str,
    text: str,
    *,
    stream: TextIO | None = None,
    enabled: bool | None = None,
):
    """
    Print the text in the specified color using ANSI escape codes.

    Args:
        color (str): The color to print the text in.
        text (str): The text to print.
    """
    target = stream or sys.stdout
    print(colorize(text, color, enabled=enabled, stream=target), file=target)


def print_colored(
    color: str,
    input_data,
    *,
    stream: TextIO | None = None,
    enabled: bool | None = None,
):
    """
    Print the input data in the specified color.

    Args:
        color (str): The color to print the text in.
        input_data: The data to print.
    """
    output(color, check_type(input_data), stream=stream, enabled=enabled)


def main():
    """
    Main function to handle command line arguments and print colored text.

    Usage:
        python colored_text.py <color> <text>
    """
    if len(sys.argv) < 3:
        print("Usage: python colored_text.py <color> <text>")
        return
    print_colored(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()
