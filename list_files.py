import argparse
import os

try:
    from .directory_traversal import traverse_and_apply
    from .filecheck import filecheck
except ImportError:  # Support direct script execution.
    from directory_traversal import traverse_and_apply
    from filecheck import filecheck


def list_files(target_dir, file_extension=None):
    """
    Lists all files in the target directory, optionally filtering by file extension.

    Args:
        target_dir (str): The directory to search for files.
        file_extension (str, optional): The file extension to filter by. Defaults to None.

    Returns:
        list: A list of file paths matching the criteria.

    Raises:
        ValueError: If the provided path is not a valid directory.
    """
    if not os.path.isdir(target_dir):
        raise ValueError(f"The provided path {target_dir} is not a valid directory.")

    directories = [target_dir]
    traverse_and_apply(target_dir, directories.append)
    result_files = []

    for root in directories:
        for file in os.listdir(root):
            path = os.path.join(root, file)
            if filecheck(path):
                if file_extension:
                    if file.endswith(file_extension):
                        result_files.append(path)
                else:
                    result_files.append(path)

    return sorted(result_files)


def main():
    parser = argparse.ArgumentParser(description="List files in a directory.")
    parser.add_argument(
        "target_dir", type=str, help="The directory to search for files."
    )
    parser.add_argument(
        "-e",
        "--extension",
        type=str,
        help="The file extension to filter by.",
        default=None,
    )

    args = parser.parse_args()

    try:
        files = list_files(args.target_dir, args.extension)
        for file in files:
            print(file)
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
