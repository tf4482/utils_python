# Utils Python

This project contains a collection of universal Python functions and scripts designed for reuse in various applications. The functions are modular and cover areas such as file management, directory traversal, text formatting, and more.

## Contents

### Files and Functions

- **`colored_text.py`**
  - `check_type(input_data)`: Converts input data to a string.
  - `output(color, text)`: Outputs text in the specified color using ANSI color codes.
  - `print_colored(color, input_data)`: Prints input data in the specified color.
  - **Usage:** For printing colored text in the console.

- **`convert_to_string.py`**
  - `convert_to_string(input_data)`: Converts various data types (e.g., dict, list, tuple) into a string representation.
  - **Usage:** For formatting and displaying data as a string.

- **`directory_traversal.py`**
  - `traverse_and_apply(base_dir, action, max_depth=None)`: Recursively traverses a directory and applies an action to each subdirectory.
  - **Usage:** For processing directories and their subdirectories.

- **`list_files.py`**
  - `list_files(target_dir, file_extension=None)`: Lists all files in a directory, optionally filtered by file extension.
  - **Usage:** For listing files in a directory.

- **`select_file.py`**
  - `select_file(directory, extension=None)`: Allows interactive selection of a file from a directory.
  - **Usage:** For interactively selecting files.

- **`copy_files.py`**
  - `copy_files(source_dir, target_dir, file_list)`: Copies specified files from a source directory to a target directory.
  - **Usage:** For copying files between directories.

- **`dpkg_check.py`**
  - `check_dpkg_installed(package_name)`: Checks if a specified package is installed using `dpkg`.
  - **Usage:** For checking package installation status.

- **`create_conf.py`**
  - `create_conf_file(file_path, content)`: Creates a configuration file with specified content.
  - **Usage:** For creating configuration files.

### Additional Files

- **`.gitignore`**: Contains rules to exclude certain files and directories from Git tracking.
- **`LICENSE`**: The project is licensed under the MIT License.
- **`__init__.py`**: Enables the directory to be used as a Python package.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
