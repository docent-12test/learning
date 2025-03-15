import os
from typing import Optional, Iterable, Any
from lib.framework import MustBeTested

NL = os.linesep




@MustBeTested
def same_type(collection:Optional[Iterable[Any]]) -> bool:
    """
    Checks if all elements in the given collection are of the same type.

    This function evaluates the types of all elements in a collection to
    determine whether they are the same. If the collection is empty, it
    returns False. Otherwise, it maps the type of each element in the
    returns False. Otherwise, it maps the type of each element in the
    collection, constructs a set to identify unique types, and checks
    if there is only one type present.

    :param collection: The collection of elements to evaluate.
                       It can be any iterable containing elements.
    :type collection: Iterable[Any]
    :return: True if all elements in the collection are of the same type,
             False otherwise, or if the collection is empty.
    :rtype: bool
    """
    if not collection:
        return False
    return len(set(map(type, collection))) == 1


def print_dict(dict_:dict, text:str = "", debug: bool = False)->None:
    """
    Prints the dictionary in a readable format to the console and provides detailed
    debug information if the debug flag is enabled.

    :param dict_: Dictionary to be printed.
       :type dict_: dict
    :param text: Optional label or name for the dictionary, default is an empty
       string.
       :type text: str
    :param debug: Flag to enable debug output, default is False.
       :type debug: bool
    :return: None
    """
    if debug:
        print("################")
    print(f"Dict '{text}' {{")
    for k, v in dict_.items():
        print(f"  {k.__repr__()} : {v.__repr__()}")
    print("}")
    if debug:
        print(f"info of dict ({text}) : {len(dict_)} items")
        if same_type(dict_.keys()):
            print("keys are type consistent")
        else:
            print("keys are not type consistent")

        if same_type(dict_.keys()):
            print("values are type consistent")
        else:
            print("values  are not type  consistent")
        print("################")


def info(var, text:str="", debug: bool = False):
    if isinstance(var, dict):
        print_dict(var, text, debug)
