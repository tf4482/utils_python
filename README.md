# Utils Python

This project contains a collection of universal Python functions and scripts designed for reuse in various applications. The functions are modular and cover areas such as file management, directory traversal, text formatting, configuration handling, and more.

## Contents

### Files and Functions

- **[`colored_text.py`](colored_text.py)**
  - `check_type(input_data)`: Converts input data to a string, delegating to `convert_to_string` for complex types.
  - `output(color, text)`: Prints text in the specified color using ANSI escape codes.
  - `print_colored(color, input_data)`: Prints input data in the specified color.
  - **Supported colors:** `black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `lgrey`, `grey`, `lred`, `lgreen`, `lyellow`, `lblue`, `lmagenta`, `lcyan`, `white`
  - **CLI usage:** `python colored_text.py <color> <text>`

- **[`convert_to_string.py`](convert_to_string.py)**
  - `convert_to_string(input_data)`: Converts various data types (`dict`, `list`, `tuple`, `set`, or any other type) into a string representation. Dicts are formatted as `key:value` pairs; sequences as space-separated elements.

- **[`directory_traversal.py`](directory_traversal.py)**
  - `traverse_and_apply(base_dir, action, max_depth=None)`: Recursively traverses a directory and applies a callable `action` to each subdirectory path. Raises `NotADirectoryError` if `base_dir` does not exist.

- **[`list_files.py`](list_files.py)**
  - `list_files(target_dir, file_extension=None)`: Recursively lists all files in a directory, optionally filtered by file extension. Returns a list of file paths.
  - **CLI usage:** `python list_files.py <target_dir> [-e <extension>]`

- **[`select_file.py`](select_file.py)**
  - `select_file(directory, extension=None)`: Presents an interactive terminal menu to select a file from a directory. Navigate with `w`/`s`, confirm with `Enter`, cancel with `q`. Returns the absolute path of the selected file, or `None` if cancelled.
  - **CLI usage:** `python select_file.py <directory> [<extension>]`

- **[`copy_files.py`](copy_files.py)**
  - `copy_files(source_dir, target_dir, file_list)`: Copies specified files from a source directory to a target directory, creating the target directory if it does not exist.

- **[`filecheck.py`](filecheck.py)**
  - `filecheck(filepath)`: Returns `True` if the given path exists and is a regular file, `False` otherwise.
  - **CLI usage:** `python filecheck.py <path_to_file>`

- **[`dpkg_check.py`](dpkg_check.py)**
  - `is_package_installed(package_name)`: Checks whether a Debian package is installed using `dpkg`. Returns `True` if installed, `False` otherwise. Requires a Debian-based system.
  - **CLI usage:** `python dpkg_check.py <package-name>`

- **[`create_config.py`](create_config.py)**
  - `create_config(filename, settings)`: Creates a YAML (`.yml`) configuration file in `/etc/` from a list of `key=value` or bare `key` strings. Dot-separated keys create nested YAML structures. Returns the full path to the created file.
  - `parse_key_value_list(settings)`: Parses a list of `key=value` strings into a nested dictionary.
  - `deep_set(dic, path, value)`: Sets a value in a nested dictionary using a list of keys as a path.
  - **CLI usage:** `sudo python3 create_config.py <filename> [key[=value] ...]`

- **[`check_config.py`](check_config.py)**
  - `has_all_yaml_values(filename)`: Loads a YAML file from `/etc/` and returns `True` if all keys (recursively) contain non-empty values. Raises `FileNotFoundError` or `yaml.YAMLError` on failure.
  - `all_keys_have_values(data)`: Recursively checks that every key in a parsed YAML structure has a non-empty value.
  - `is_filled(value)`: Returns `True` if a value is not `None` and not a whitespace-only string.
  - **CLI usage:** `python3 check_config.py <filename>` (exits `0` if all filled, `2` if not, `1` on error)

- **[`config_loader.py`](config_loader.py)**
  - `load_config(app_name, config_filename, defaults, *, caller_file=None)`: Locates and loads a JSON configuration file for an application. Searches first next to the calling script, then in `~/.config/<app_name>/`. If no file is found, a placeholder is written to the user-level path and `SystemExit(1)` is raised.
  - **Search order:**
    1. `<directory of calling script>/<config_filename>`
    2. `~/.config/<app_name>/<config_filename>`

## Usage

Import any module directly into your project:

```python
from utils_python.colored_text import print_colored
from utils_python.list_files import list_files
from utils_python.config_loader import load_config
from utils_python.filecheck import filecheck
```

Most modules can also be run as standalone scripts from the command line — see the **CLI usage** note under each module above.

## License

This project is licensed under the [MIT License](LICENSE).
