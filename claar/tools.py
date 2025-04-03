"""
General functionality
"""
import math

iimport subprocess
from typing import Union

from claar import filesystem
from claar.exceptions import AppException


def safe_call(return_count: int=1) :
    """
    Function to create a decorator that applies error handling and wraps the output
    of a callable in a consistent tuple-based structure.

    This function generates a decorator that enhances the resilience of a callable by:
    - Wrapping it in a try-except block to handle exceptions gracefully.
    - Ensuring a tuple is returned with a predictable number of slots,
      each corresponding to either an output value of the callable, `None`, or an error message.

    This utility is particularly useful for cases where robust error handling and consistent
    output structure are required by the caller, facilitating robust downstream processing.

    :param return_count: Number of expected return slots in the tuple. The decorated
        function's output values will populate the first slots, followed by `None`
        or an error message in case of failure.
        Defaults to 1.
    :type return_count: int
    :return: A decorator that applies the tuple-based error handling structure to the
        given function.
    :rtype: Callable
    """

    def decorator(func):
        """
        Decorator that wraps a function with error handling and ensures a consistent tuple-based result.
        """
        def wrapper(*args, **kwargs):
            """
            Decorator to wrap a function with error handling and return a consistent tuple-based result.
            """
            try:
                res = func(*args, **kwargs)
                return res, None
            except Exception as e:
                return (None,) * return_count + (f"Error occurred: {e}",)
        return wrapper
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
    :param server: Server to run the command on
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
        stdout = stdout.split('\n')
    if stdout and stdout[-1] == '':
        stdout.pop(-1)
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


def count_none_values(*values: object) -> int:
    """
    Count the number of None values in the provided arguments.

    :param values: Iterable of values to be checked.
    :return: Number of None values.
    """
    none_values = [_ for _ in values if _ is None]
    return len(none_values)

def first_non_none(*args, default=None) -> object:
    """
    Returns the first non-None value from the arguments.

    :param args: Arguments to check.
    :param default: Value to return if all arguments are None.
    :return: The first non-None value or the default.
    """
    for value in args:
        if value is not None:
            return value
    return default


def split_list(input_list: list,
               size: int,
               complete_last: bool = False,
               default_value=None) -> list:
    """
    Split a list into parts of a specific size.

    :param input_list: List to split
    :param size: Size of the sublists
    :param complete_last: If True, default values will be added to the last
                          part to match the required size
    :param default_value: Value to use when completing the last part
    :return: List of sublists
    """
    if size < 1:
        raise ValueError(f"Size {size} must be strictly positive")

    if not input_list:
        return []

    num_chunks = math.ceil(len(input_list) / size)  # Number of chunks
    result = [input_list[i * size:(i + 1) * size] for i in range(num_chunks)]

    if complete_last and result:
        result[-1] = complete_last_part(result[-1], size, default_value)

    return result


def add_to_collection(value: object, target: Union[list, set]) -> None:
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
        raise NotImplementedError(f"add_to_collection is not supporting target type {type(target)}")


def pop_keys(dict_: dict, must_be_empty: bool, *keys) -> bool:
    """
    Remove one or more items from a dict
    :param dict_: source dict
    :param must_be_empty: if True
    :param keys: all keys to be removed from the dict
    :return: True if keys were removed.
             False if dict is still not empty and it must be empty
    """
    for key in keys:
        dict_.pop(key)
    if must_be_empty and len(dict_):
        return False
    return True


if __name__ == "__main__":
    raise NotImplementedError(f"This module is not meant to be run directly: {__file__}")
