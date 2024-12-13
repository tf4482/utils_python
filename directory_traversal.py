import os

def traverse_and_apply(base_dir, action, max_depth=None):
    """
    Traverse directories starting from base_dir and apply an action to each subdirectory.

    Args:
        base_dir (str): The base directory to start traversal.
        action (function): A function to apply to each subdirectory path.
        max_depth (int, optional): Maximum depth to traverse. Defaults to None.

    Raises:
        NotADirectoryError: If the specified base directory does not exist.
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
