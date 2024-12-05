import os

def list_files(target_dir, file_extension=None):

    if not os.path.isdir(target_dir):
        raise ValueError(f"The provided path {target_dir} is not a valid directory.")

    result_files = []

    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if file_extension:
                if file.endswith(file_extension):
                    result_files.append(os.path.join(root, file))
            else:
                result_files.append(os.path.join(root, file))

    return result_files
