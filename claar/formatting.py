"""
Formatting functionality to represent data in a more readable form
"""

import os
from typing import Iterable


def list_str(input_list: Iterable, label: str = None) -> str:
    """
    Printable version of a list
    :param input_list: dictionary to print.
    :param label: optional prefix
    :return: string version of the dictionary
    """
    label = "" if label is None else f"{label}: "
    ret = f"{os.linesep}{label}=== {type(input_list).__name__} start  ==="
    for row in input_list:
        ret += f"{os.linesep}{row}"

    ret += f"{os.linesep}=== end ==={os.linesep}"
    return ret


def dict_str(dictionary: dict,
             label: str = "",
             align_keys: bool = True) -> str:
    """
    Printable version of a dictionary.
    :param dictionary: dictionary to print.
    :param label: optional prefix
    :param align_keys: if True, the keys will be right aligned
    :return: string version of the dictionary
    """
    if dictionary is None:
        return "None"
    ret = [f"{os.linesep}{label}==="]
    if len(dictionary) == 0:
        ret.append("dict is leeg")
    else:
        align = max(len(f'{key}') for key in dictionary.keys()) if align_keys else 0
        ret += [f"\t{f_str(key, align + 1)} ==> {value}" for key, value in dictionary.items()]
    ret.append(f"==={os.linesep}")
    return f"{os.linesep}".join(ret)


def short_bool(value: bool, lang: str = "default") -> str:
    """
    Short string representation for a bool
    :param value: boolean to format
    :param lang: language to be used
    :return: 'T'/'F'/'N', or alternatives
    """
    translation = {"default": ['N', 'F', 'T'],
                   "NL": ['-', 'N', 'J'],
                   "EN": ['-', 'N', 'Y']}

    if value is None:
        return translation.get(lang, ['N', 'F', 'T'])[0]
    if value:
        return translation.get(lang, ['N', 'F', 'T'])[2]
    return translation.get(lang, ['N', 'F', 'T'])[1]


def f_str(value, indent) -> str:
    """
    format a value as string, even if it is None
    """
    ret = f"{value}"
    return f"{ret:{indent}}"


def n_str(value, char: str = '-') -> str:
    """
    format a value as string, even if it is None
    """
    return f"{value}" if value is not None else char


def tab(value: int = 1) -> str:
    """
    return a number of tabs
    """
    return "\t" * value


FONT = {
    'A': [14, 17, 17, 31, 17, 17, 17],
    'B': [30, 17, 17, 30, 17, 17, 30],
    'C': [14, 17, 16, 16, 16, 17, 14],
    'D': [30, 17, 17, 17, 17, 17, 30],
    'E': [31, 16, 16, 30, 16, 16, 31],
    'F': [31, 16, 16, 28, 16, 16, 16],
    'G': [14, 17, 16, 16, 19, 17, 14],
    'H': [17, 17, 17, 31, 17, 17, 17],
    'I': [14, 4, 4, 4, 4, 4, 14],
    'J': [1, 1, 1, 1, 1, 17, 14],
    'K': [17, 18, 20, 24, 20, 18, 17],
    'L': [16, 16, 16, 16, 16, 16, 31],
    'M': [17, 27, 21, 17, 17, 17, 17],
    'N': [17, 25, 21, 19, 17, 17, 17],
    'O': [14, 17, 17, 17, 17, 17, 14],
    'P': [30, 17, 17, 30, 16, 16, 16],
    'Q': [14, 17, 17, 17, 17, 19, 15],
    'R': [30, 17, 17, 30, 20, 18, 17],
    'S': [14, 17, 16, 14, 1, 17, 14],
    'T': [31, 4, 4, 4, 4, 4, 4],
    'U': [17, 17, 17, 17, 17, 17, 14],
    'V': [17, 17, 17, 17, 17, 10, 4],
    'W': [17, 17, 17, 17, 17, 21, 10],
    'X': [17, 17, 10, 4, 10, 17, 17],
    'Y': [17, 17, 10, 4, 4, 4, 4],
    'Z': [31, 1, 2, 4, 8, 16, 31],
    ' ': [0, 0, 0, 0, 0, 0, 0],
    '0': [14, 17, 17, 17, 17, 17, 14],
    '1': [4, 4, 4, 4, 4, 4, 4],
    '2': [31, 1, 1, 31, 16, 16, 31],
    '3': [31, 1, 1, 31, 1, 1, 31],
    '4': [17, 17, 17, 31, 1, 1, 1],
    '5': [31, 16, 16, 31, 1, 1, 31],
    '6': [31, 16, 16, 31, 17, 17, 31],
    '7': [31, 1, 1, 1, 1, 1, 1],
    '8': [31, 17, 17, 31, 17, 17, 31],
    '9': [31, 17, 17, 31, 1, 1, 31],
    '_': [0, 0, 0, 0, 0, 0, 31],
    '-': [0, 0, 0, 31, 0, 0, 0],
    '.': [0, 0, 0, 0, 0, 0, 8],
    '|': [8, 8, 8, 8, 8, 8, 8],
    '\'': [0, 0, 0, 8, 0, 0, 0],
    '"': [20, 20, 0, 0, 8, 8],
    
}


def big_font(text: str) -> str:
    """
    Transform a string into large letters
    The text 'RULE' becomes
         ### # # #   ###
         # # # # #   #
         ### # # #   ###
         ##  # # #   #
         # # ### ### ###
    :return: one string including newlines
    """
    buf = ['\n', '', '\n', '', '\n', '', '\n', '', '\n', '', '\n', '', '\n', '', '\n']
    for ch in text:
        rows = FONT.get(ch.upper(), [31] * 7)
        for i in range(7):
            for j in range(4, -1, -1):
                buf[i * 2 + 1] += 'O' if rows[i] & (1 << j) else ' '
        for i in range(7):
            buf[i * 2 + 1] += '  '
    return "".join(buf)


if __name__ == "__main__":
    raise NotImplementedError(f"This module is not meant to be run directly: {__file__}")
