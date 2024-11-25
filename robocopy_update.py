import os
import subprocess

def robocopy_update(source_file, target_dir):
    """
    Copies a file to a target directory using robocopy, only if the source file is newer.

    Args:
        source_file (str): The source file path.
        target_dir (str): The target directory path.
    """
    command = [
        "robocopy",
        os.path.dirname(source_file),
        target_dir,
        os.path.basename(source_file),
        "/XO", "/NJH", "/NJS", "/NP"
    ]
    subprocess.run(command, check=True)
