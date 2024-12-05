import os
import shutil

def copy_files(source_dir, target_dir, file_list):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    for file in file_list:
        source_path = os.path.join(source_dir, file)
        target_path = os.path.join(target_dir, file)
        shutil.copy2(source_path, target_path)
