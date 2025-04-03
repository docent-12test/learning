"""
General string functionality
"""
import random
from typing import Union, Optional

ARROW = " ==> "
EMPTY_STRING = ""


# unittest OK
def list_stringify(input_list: Optional[list],
                   none_value='None') -> Union[list, None]:
    """
    Return a list of values as  a list of strings
    :param none_value: value for None, default 'None'
    :param input_list: list of values
    :return: list of string values
    """
    if input_list is None:
        return None
    return [none_value if value is None else str(value) for value in input_list]


# unittest OK
def enclose(value,
            character: str = "'",
            none_value: str = 'None') -> Optional[str]:
    """
    Enclose a value between quotes, unless it is None
    :param none_value: value for None, default 'None'
    :param character: enclosing character, default '
    :param value: Value to enclose
    :return: Enclosed value or None
    """
    if value is None:
        return none_value
    return f"{character}{value}{character}"


# unittest OK
def convert_str_to_num(input_string: str) -> Union[int, float, None]:
    """
    Check if input string is numeric.
    Convert the variable to int, float or leave it as string.
    :param input_string: String value to convert
    :return: Value of the variable if everything checks out,
             otherwise an AttributeError will be raised.
    """
    try:
        return int(input_string)
    except ValueError:
        try:
            return float(input_string.replace(',', '.'))
        except ValueError:
            return None


# unittest OK
def validate_and_replace_char(string: str,
                              char_to_find: str = ';',
                              char_to_replace: str = ' ') -> (str, bool):
    """
    Verify if a char is part of an input string:
        If True replace the character by another provided one or space
        If False return the original string;
    :param string: string to verify
    :param char_to_find: char to find in input string, default ;
    :param char_to_replace: char to replace with, default is space
    :return: tuple(string, boolean) string with or without the changes,
             boolean to indicate if string was modified
    """
    new_string = string.replace(char_to_find, char_to_replace)
    return new_string, string != new_string


def scramble(string: str) -> Optional[str]:
    """
    Randomly mix the characters of a string
    """
    if string is None:
        return None
    char_list = list(string)
    # Shuffle the list in place
    random.shuffle(char_list)

    # Join the characters back into a string
    shuffled_string = ''.join(char_list)

    return shuffled_string


if __name__ == "__main__":
    raise NotImplementedError(f"This module is not meant to be run directly: {__file__}")
