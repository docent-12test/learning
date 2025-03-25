"""
General functionality
"""

import math
import subprocess
from typing import Union


from framework.exceptions import FrameworkException, EXCEPTION_PREFIX
from lib import filesystem


# Unittest OK
def run_linux_command(command_parts: list,
                      server: str = None,
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
    # todo: shell
    if input_string is not None and input_file is not None:
        raise FrameworkException(f"input_string '{input_string}' and "
                                 f"input_file '{input_file}' can not both be "
                                 f"filled in. At least one must be None")
    if input_file is not None:
        input_string = filesystem.file_contents(input_file)

    if server is None:  # run on current server
        return_code = None
        output = None
        try:
            proc = subprocess.Popen(command_parts,
                                    stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    encoding=server_config.ENCODING)
            output, err = proc.communicate(input=input_string)
            return_code = proc.returncode
            proc.stdout.close()
            proc.stderr.close()
            if split_output:
                output = output.split("\n")
            if output and output[-1] == '':
                output.pop(-1)
            return output, err, return_code
        except Exception as e:
            return output, f"{EXCEPTION_PREFIX}run_linux_command() failed: {e}", return_code
    else:
        # todo: implement run on different server
        raise NotImplementedError()


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
        if case_sensitive:
            if string.startswith(prefix):
                return True
        else:
            if string.upper().startswith(prefix.upper()):
                return True
    return False


def count_nones(*args) -> int:
    """
    Count the number of None arguments
    :param args: list of arguments
    :return: Number of Nones
    """
    return len([_ for _ in args if _ is None])


def count_not_nones(*args) -> int:
    """
    Count the number of not None arguments
    :param args: list of arguments
    :return: Number of non None values
    """
    return len([_ for _ in args if _ is not None])


def get_first_non_none(*args) -> object:
    """
    Get the first non None value from the arguments
    :param args: list of arguments
    :return: First non None value
    """
    for value in args:
        if value is not None:
            return value
    raise FrameworkException("No not none value found in list {*args}")


def none_or_empty(value) -> bool:
    """
    Determine whether a value is None or empty
    :param value: Value to check
    :return: True is value is None or empty
    """
    if value is None:
        return True
    if isinstance(value, (list, dict, set, tuple, str)):
        return not value
    return False


def not_none_or_empty(value) -> bool:
    """
    Determine whether a value is None or empty
    :param value: Value to check
    :return: True is value is None or empty
    """
    return not none_or_empty(value)


def none_or_false(value) -> bool:
    """
    Determine whether a value is None or False
    :param value: Value to check
    :return: True is value is None or False
    """
    return value is None or not value


def none_or_true(value) -> bool:
    """
    Determine whether a value is None or True
    :param value: Value to check
    :return: True is value is None or True
    """
    return value is None or value


def split_list(input_list: list,
               size: int,
               complete_last: bool = False,
               default_value=None) -> list:
    """
    Split a list in parts of a specific size.
    :param input_list: list to split
    :param size: size of the sub lists
    :param complete_last: If true, default values will be added to the last
                          part in order to match the size
    :param default_value: Use this value in case complete_last is true,
                          otherwise ignore this parameter
    """
    if size < 1:
        raise ValueError(f"Size {size} must be strictly positive")

    ret = []
    if none_or_empty(input_list):
        return ret

    for i in range(math.ceil(len(input_list) / size)):
        start = i * size
        end = (i + 1) * size
        ret.append(input_list[start:end])

    if complete_last and ret:
        last_part = ret[-1]
        length = len(last_part)
        if length < size:
            last_part.extend([default_value] * (size - length))

    return ret


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
