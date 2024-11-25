import os
import subprocess

def rsync_to_subdirs(source_file, target_dir):
    """Verwendet rsync, um die Datei nur zu überschreiben, wenn sie neuer ist."""
    for root, dirs, _ in os.walk(target_dir):
        for subdir in dirs:
            subdir_path = os.path.join(root, subdir)
            command = ["rsync", "-u", source_file, subdir_path + "/"]
            subprocess.run(command, check=True)
        # Kopiert in das Zielverzeichnis selbst.
        command = ["rsync", "-u", source_file, target_dir + "/"]
        subprocess.run(command, check=True)
