"""
Parsing functions
"""

from decimal import Decimal
from typing import Union, Optional
from numbers import Real

from claar.exceptions import AppException


def validate_and_convert(value: Union[str, Real]) -> Real:
    """
    Validate the input and convert it to a numeric value if it's a string.
    :param value: The value to validate and convert.
    :param param_name: The name of the parameter (for error messages).
    :return: Numeric representation of the value.
    """
    if value is None:
        raise TypeError(f"{value} is None")
    if not isinstance(value, str) and not isinstance(value, Real):
        raise TypeError(f"({value}) is niet str noch numeriek")
    if isinstance(value, str):
        if len(value) == 0:
            raise TypeError(f"{value} is leeg")
        try:
            return float(value)
        except ValueError:
            raise TypeError(f"{value} kan niet omgezet worden naar een getal")
    return value


def add_int(value1: Union[str, Real], value2: Union[str, Real]) -> Optional[str]:
    """
    Add a value to a string value, e.g., '4' + 2 => '6'.
    :param value1: Value as str or numeric.
    :param value2: Value as str or numeric.
    :return: String format of the sum.
    """
    num1 = validate_and_convert(value1)
    num2 = validate_and_convert(value2)

    try:
        return f"{int(num1 + num2)}"
    except (ValueError, TypeError) as e:
        raise AppException(f"value1 ({num1}) en value2 ({num2}) zijn niet optelbaar") from e


def check_type(variable, target_type, allowed_empty: bool = True):
    """
    Verify the type and emptiness of a variable.
    :param variable: Variable under consideration
    :param target_type: type to check the variable against
    :param allowed_empty: true if a variable may be empty
    :return: Value of the variable  if everything checks out,
             otherwise an AttributeError will be raised.
    """
    if not isinstance(variable, target_type):
        if target_type == int:
            try:
                temp = int(variable)
                if str(temp) == str(variable):
                    return temp
                raise AttributeError(f"variable: {variable} must be of type {target_type}")
            except Exception as e:
                raise AttributeError(f"variable: {variable} must be of type {target_type} => {e}")
        elif target_type == float:
            try:
                temp = float(variable)
                return temp
            except Exception as e:
                raise AttributeError(f"variable: {variable} must be of type {target_type} => {e}")
        elif target_type == bool:
            temp = parse_boolean(variable)
            if temp is not None:
                return temp
        raise AttributeError(f"variable: {variable} must be of type {target_type}")
    if str(variable) == '' and not allowed_empty:
        raise AttributeError(f"variable must not be empty")
    return variable


def parse_boolean(text: str,
                  true_values=('1', 'ON', "JA", "J", "AAN", "YES", "Y", "TRUE", "WAAR"),
                  false_values=("0", "OFF", "NEEN", "NEE", "N", "UIT", "NO", "FALSE", "ONWAAR", "VALS"),
                  raise_exception: bool = False) -> Optional[bool]:
    """
    Parse a string representing a binary state
    :param text: string to parse
    :param true_values: list of possible ON values
    :param false_values: list of possible ON values
    :param  raise_exception: if False, an error will return None,
                             i.s.o. raising a ValueError exception
    :return: true, false or None (undecided)
    """
    if text is None:
        return None
    upper = str(text).upper()
    if upper in true_values:
        return True
    if upper in false_values:
        return False
    if raise_exception:
        raise ValueError(f"can not cast {text} to bool")
    return None


def parse_bits(value: int, number_of_bits: int) -> list[bool]:
    """
    Convert a number to a list of booleans. Element zero is the LSB
    parse_bits(11, 4) -> [1,1,0,1]
    parse_bits(11, 6) -> [1,1,0,1,0,0]
    :param value: number to convert
    :param number_of_bits: how many bits to consider
    :return: List of bits
    """
    try:
        check_type(value, int, False)
        check_type(number_of_bits, int, False)
    except AttributeError as e:
        raise NotImplementedError(f"parse_bits both parameters must be int => {e}")
    ret = []
    for _ in range(number_of_bits):
        ret.append(value & 1 == 1)
        value >>= 1
    return ret


def parse_bitstring(value: str) -> list:
    """
    Convert a string of bits to a list of booleans
    :param value: bits string, e.g. "00101"
    :return: List of bools
    """
    if not isinstance(value, str):
        raise AppException(f"{value} must be a string")
    ret = []
    for char in value:
        if char not in {'0', '1'}:
            raise ValueError(f"{value} is not a valid bitstring. It contains '{char}' which is not '0' or '1'.")
        ret.append(char == '1')

    return ret



def parse_float(value: str, raise_exception=False) -> Optional[float]:
    """
    Convert a string representation of a float with decimal comma (i.s.o. decimal point)
    :param value: float with decimal comma
    :param  raise_exception: if False, an error will return None, i.s.o. raising a ValueError exception
    :return: float value - None in case of failure
    """
    try:
        return float(str(value).replace(',', '.'))
    except ValueError as e:
        if raise_exception:
            raise e
        return None


def parse_float_to_poa_format(value) -> Optional[str]:
    """
    Convert a string representation of a float with decimal comma (i.s.o. decimal point)
    :param value: float with decimal comma
    :return: float value - None in case of failure
    """
    try:
        return str(value).replace('.', ',')
    except ValueError:
        return None


# todo: unit test
def get_numeric_part(value: str) -> Optional[int]:
    """
    Concatenate all the digits from a string and turn it into an integer.
    Can be used to sort strings in a basis order.
    :param value: input to get digits from
    :return: number extracted from value
    """
    try:
        digits = [ch for ch in value if ch.isdigit()]
        return int(''.join(digits))
    except Exception:
        return None



def cast_to_type(value, target_type) -> Union[str, float, int, bool, None]:
    """
    Cast a value to the specific type
    :param value: source value
    :param target_type: type to cast to
    :return: value in specific type or None in case of error
    """
    if target_type in (str, float, int, Decimal):
        if target_type == str:
            return str(value)
        if target_type == float:
            return parse_float(value)
        try:
            return target_type(parse_float(value))
        except (ValueError, TypeError):
            return None
    elif target_type == bool:
        return parse_boolean(value)
    else:
        raise NotImplementedError(f"Type {target_type} is not implemented")


def convert_value_to_base_unit(value: Union[int, float], unit_text: str, unit: str) -> float:
    """
    Convert a value to mega-unit based on the provided unit
    :param value: initial value
    :param unit_text: m-unit, k-unit, unit, eg. MW, kW, W, mW
    :param unit:
    :return: converted value
    """
    try:
        if unit_text[:].upper() == unit[:].upper():  # fails if either one is None
            return value * 1.0
        if unit_text[1:].upper() != unit.upper():
            raise FrameworkException(f"Can not interpret unit '{unit_text}'. "
                                     f"It is not expressed in G{unit}, "
                                     f"M{unit}, k{unit} or {unit}")
        letter = unit_text[0]
        if letter == "M":
            return value / 1000000.0
        elif letter == "k":
            return value / 1000.0
        elif letter == "m":
            return value * 1000.0
        else:
            raise FrameworkException(f"Can not interpret unit '{unit_text}'. "
                                     f"It is not expressed in G{unit}, M{unit}, k{unit}, {unit} or m{unit}")
    except Exception as e:
        raise FrameworkException(f"Can not interpret unit in convert_value_to_base_unit({value}, {unit_text}, {unit} ==> {e}")


def convert_string_to_list(value: str) -> Optional[list]:
    """
    Convert a string of the form '[X,Y,Z]' to a python list ['X','Y','Z']
    :param value: string of the form '[X,Y,Z]'
    :return: list of string
    """
    try:
        value = value.replace(' ', '')
        if len(value) < 2:
            raise FrameworkException(f"'{value}' is too short")
        if value[0] != '[' or value[-1] != ']':
            raise FrameworkException(f"'{value}' must start with [ and with ]")
        if value == '[]':
            return []
        value = value[1:-1]
        value = value.split(',')
        return value
    except Exception as e:
        SCRIPT_LOGGER.debug(f"Could not convert value  ==> {e}")
        return None



def match(value:str, regexps:List[str]) -> bool:
    """
    Try matching the value to the filter
    :param value: Value to match
    :param regexps: List of regular expression to match to
    """
    for regexp in regexps or []:
        if regexp.search(value):
            return True
    return False


if __name__ == "__main__":
    raise NotImplementedError(f"This module is not meant to be run directly: {__file__}")
