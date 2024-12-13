#!/usr/bin/python3

import os
import sys


def select_file(directory, extension=None):
    """
    Prompts the user to select a file from the specified directory.

    Args:
        directory (str): The directory to list files from.
        extension (str, optional): Filter files by extension. Defaults to None.

    Returns:
        str: The absolute path of the selected file, or None if cancelled or no files found.
    """

    def list_files(directory, extension):
        if extension:
            return [f for f in os.listdir(directory) if f.endswith(extension)]
        else:
            return os.listdir(directory)

    def display_menu(files, selected_index):
        os.system('cls' if os.name == 'nt' else 'clear')
        for index, file in enumerate(files):
            if index == selected_index:
                print(f"> {file}")
            else:
                print(f"  {file}")

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
            return os.path.abspath(os.path.join(directory, files[selected_index]))
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
