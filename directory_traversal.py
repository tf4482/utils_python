import os

def traverse_and_apply(base_dir, action, max_depth=None):
    """
    Recursively traverses all subdirectories of a given directory up to a specified depth and applies a specified action.

    Args:
        base_dir (str): The base directory to traverse.
        action (Callable[[str], None]): A function to apply to each subdirectory.
        max_depth (int, optional): The maximum depth to traverse. If None, traverses all depths.
    """
    if not os.path.isdir(base_dir):
        raise NotADirectoryError(f"The specified base directory '{base_dir}' does not exist.")

    base_depth = base_dir.rstrip(os.path.sep).count(os.path.sep)

    for root, dirs, _ in os.walk(base_dir):
        current_depth = root.rstrip(os.path.sep).count(os.path.sep) - base_depth
        if max_depth is not None and current_depth >= max_depth:
            dirs[:] = []
        for subdir in dirs:
            subdir_path = os.path.join(root, subdir)
            action(subdir_path)
