#!/usr/bin/python3

import sys
from typing import Any


def convert_to_string(input_data: Any) -> str:
    """
    Convert various types of input data to a string representation.

    Args:
        input_data (Any): The input data to be converted. It can be of type dict, list, tuple, set, or any other type.

    Returns:
        str: A string representation of the input data. For dictionaries, it returns a string with key-value pairs separated by spaces.For lists, tuples, and sets, it returns a space-separated string of their elements. For other types, it returns the string representation of the input data.
    """
    try:
        if isinstance(input_data, dict):
            return " ".join([f"{key}:{value}" for key, value in input_data.items()])
        elif isinstance(input_data, (list, tuple, set)):
            return " ".join(map(str, input_data))
        else:
            return str(input_data)
    except Exception as e:
        return f"Error converting input to string: {e}"


def main(argv):
    """
    Main function to convert command line arguments to a string.

    Args:
        argv (list): List of command line arguments.
    """
    convert_to_string(sys.argv)


if __name__ == "__main__":
    main(sys.argv)
