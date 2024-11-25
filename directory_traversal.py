import os

def traverse_and_apply(base_dir, action):
    """
    Recursively traverses all subdirectories of a given directory and applies a specified action.

    Args:
        base_dir (str): The base directory to traverse.
        action (Callable[[str], None]): A function to apply to each subdirectory.
    """
    if not os.path.isdir(base_dir):
        raise NotADirectoryError(f"The specified base directory '{base_dir}' does not exist.")

    for root, dirs, _ in os.walk(base_dir):
        for subdir in dirs:
            subdir_path = os.path.join(root, subdir)
            action(subdir_path)
