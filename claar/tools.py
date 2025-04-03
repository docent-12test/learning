"""
General code tools
"""
import math
import subprocess
from typing import Union, List, Iterable

from claar import filesystem
from claar.exceptions import AppException


def safe_duplicate(return_size: int):
    """
    Decorator that adds safe handling functionality to a function. This decorator modifies
    the behavior of the function by introducing two alternatives: a normal execution (`normal_result`)
    and a safe execution (`safe`). The safe execution handles exceptions gracefully by replacing
    the result with a tuple of `None` values of length `param` followed by an error message.

    :param return_size: A positive integer indicating the number of `None` elements to prepend
                  in the tuple when the decorated function encounters an exception.
    :type return_size: int
    :return: A wrapper function that modifies the behavior of the original function by adding
             safe handling capabilities.
    :rtype: Callable
    """

    def decorator(func):
        """
        A decorator
        :param func: The number of `None` values to include in the result when an
                      exception is raised.
        :type func: Callable
        """

        def normal_result(*args, **kwargs):
            """
            Normal execution of the decorated function. This function simply calls the original
            :param args: args
            :param kwargs: kwargs
            :return: normal result
            """
            return func(*args, **kwargs)

        def safe(*args, **kwargs):
            """
            normal execution of the decorated function. This function simply calls the original, but adds an error
            message to the result if an exception is raised. The error message is None in case of
            """
            try:
                result = func(*args, **kwargs)
                return result + (None,)
            except Exception as e:
                return (None,) * return_size + (f"Error occurred: {e}",)

        func.normal_result = normal_result
        func.safe = safe
        return func

    return decorator


def run_command(command_parts: list,
                split_output: bool = True,
                input_string: str = None,
                input_file: str = None) -> (str, str, int):
    """
    Run a command on linux. If a server is provided it will be ssh
    :param input_string: String input for command
    :param input_file: File that contains input string
    :param command_parts: Command to run
    :param split_output: if true the output will be split in lines
    :return: output lines, error, OS returncode
    """
    if input_string is not None and input_file is not None:
        raise AppException(f"input_string '{input_string}' and "
                           f"input_file '{input_file}' can not both be "
                           f"filled in. At least one must be None")
    if input_file is not None:
        input_string = filesystem.file_contents(input_file)
    proc = subprocess.Popen(command_parts,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate(input=input_string)
    return_code = proc.returncode
    proc.stdout.close()
    proc.stderr.close()
    if split_output:
        stdout = stdout.split(b'\n')
    if stdout and stdout[-1] == '':
        stdout.pop()
    return stdout, stderr, return_code


def starts_with_from_list(string: str,
                          prefixes: list,
                          case_sensitive: bool = True) -> bool:
    """
    Check if a string starts with any
    :param string: value to check
    :param prefixes: list of strings
    :param case_sensitive: case modus
    :return: true if the string starts with any of the prefixes in the list
    """
    if string is None or not prefixes:
        raise AttributeError("Calling starts_with_from_list with None-values")
    for prefix in prefixes:
        temp_str = string if case_sensitive else string.upper()
        if temp_str.startswith(prefix):
            return True
    return False


def count_none_values(collection: Iterable) -> int:
    """
    Count the number of None values in the provided arguments.

    :param collection: Iterable of values to be checked.
    :return: Number of None values.
    """
    none_values = [_ for _ in collection if _ is None]
    return len(none_values)


def first_non_none(collection: Iterable, default=None) -> object:
    """
    Returns the first non-None value from the arguments.

    :param collection: Arguments to check.
    :param default: Value to return if all arguments are None.
    :return: The first non-None value or the default.
    """
    for value in collection:
        if value is not None:
            return value
    return default


def split_list(input_list: list,
               size: int,
               complete_last: bool = False,
               default_value=None) -> List[List]:
    """
    Split a list into parts of a specific size.

    :param input_list: List to split
    :param size: Size of the sub lists
    :param complete_last: If True, default values will be added to the last
                          part to match the required size
    :param default_value: Value to use when completing the last part
    :return: List of sub lists
    """
    if size < 1:
        raise ValueError(f"Size {size} must be strictly positive")

    if not input_list:
        return []

    num_chunks = math.ceil(len(input_list) / size)  # Number of chunks
    result = [input_list[i * size:(i + 1) * size] for i in range(num_chunks)]

    if complete_last and result:
        result[-1] = result[-1] + [default_value] * (size - len(result[-1]))
    return result


def add_to(value: object, target: Union[list, set]) -> None:
    """
    Add a value to a list or a set
    :param value: Value to add
    :param target: set or list to add value to
    """
    if isinstance(target, list):
        target.append(value)
    elif isinstance(target, set):
        target.add(value)
    else:
        raise NotImplementedError(f"add_to is not supporting target type {type(target)}")


def pop_keys(source_dict: dict,
             keys: Iterable,
             must_exist: bool = False,
             must_be_empty: bool = False) -> bool:
    """
    Remove one or more items from a dictionary.
    :param source_dict: The dictionary to remove keys from.
    :param keys: The keys that should be removed from the dictionary.
    :param must_exist: If True, raises KeyError if any key is missing.
    :param must_be_empty: If True, validates that the dictionary is empty after removals.
    :return: True if keys were removed (and the resulting dictionary is empty if required),
             False if the dictionary is not empty when it must be.
    """
    for key in keys:
        if must_exist:
            source_dict.pop(key)
        else:
            source_dict.pop(key, None)
    if must_be_empty and source_dict:
        return False
    return True


if __name__ == "__main__":
    raise NotImplementedError(f"This module is not meant to be run directly: {__file__}")
