#!/usr/bin/python3

import os
import sys
from collections.abc import Callable, Sequence
from typing import TextIO, TypeVar

try:
    from .colored_text import output
    from .list_files import list_files
except ImportError:  # Support direct script execution.
    from colored_text import output
    from list_files import list_files

T = TypeVar("T")


def select_option(
    options: Sequence[T],
    *,
    prompt: str = "Select an option",
    display: Callable[[T], str] = str,
    input_stream: TextIO | None = None,
    output_stream: TextIO | None = None,
) -> T | None:
    """Select one item through a deterministic numbered terminal menu."""
    source = input_stream or sys.stdin
    target = output_stream or sys.stdout
    if not options:
        return None
    while True:
        output("lcyan", prompt, stream=target)
        for index, option in enumerate(options, start=1):
            output("lblue", f"  {index}. {display(option)}", stream=target)
        output("lyellow", "  q. Cancel", stream=target)
        target.flush()
        answer = source.readline()
        if answer == "":
            return None
        value = answer.strip().casefold()
        if value == "q":
            return None
        try:
            selected = int(value) - 1
        except ValueError:
            output("lred", "❌ Invalid selection.", stream=target)
            continue
        if 0 <= selected < len(options):
            return options[selected]
        output("lred", "❌ Invalid selection.", stream=target)


def select_file(directory, extension=None):
    """
    Prompts the user to select a file from the specified directory.

    Args:
        directory (str): The directory to list files from.
        extension (str, optional): Filter files by extension. Defaults to None.

    Returns:
        str: The absolute path of the selected file, or None if cancelled or no files found.
    """

    def display_menu(files, selected_index):
        os.system('cls' if os.name == 'nt' else 'clear')
        for index, file in enumerate(files):
            display_name = os.path.relpath(file, directory)
            if index == selected_index:
                print(f"> {display_name}")
            else:
                print(f"  {display_name}")

    files = list_files(directory, extension)

    if not files:
        print(f"No files found in directory '{directory}'.")
        return None

    selected_index = 0
    while True:
        display_menu(files, selected_index)
        print("\nNavigate with w/s, select with Enter.")
        print("Cancel with q.")

        key = input("Input: ").lower()

        if key == 'w':
            selected_index = (selected_index - 1) % len(files)
        elif key == 's':
            selected_index = (selected_index + 1) % len(files)
        elif key == '':
            return os.path.abspath(files[selected_index])
        elif key == 'q':
            print("Selection cancelled.")
            return None


def main():
    """
    Main function to handle command line arguments and prompt file selection.

    Usage:
        python select_file.py <directory> [<extension>]
    """
    if len(sys.argv) < 2:
        print("Usage: python select_file.py <directory> [<extension>]")
        return

    directory = sys.argv[1]
    extension = sys.argv[2] if len(sys.argv) > 2 else None

    selected_file = select_file(directory, extension)
    if selected_file:
        print(f"Selected file: {selected_file}")


if __name__ == "__main__":
    main()
