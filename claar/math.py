"""
FILE_INFORMATION=Fluvius;Arvid Claassen;Core of ANM framework
(C) Copyright 2024, Fluvius

Math and statistics
"""
from typing import Union

PERCENT = 100.0
DEFAULT_NUMBER_OF_DECIMALS = 2
L = ".1f"  # limited precision
N = ".2f"  # normal precision
E = ".4f"  # extended precision

SL = f"+{L}"  # limited precision
SN = f"+{N}"  # normal precision
SE = f"+{E}"  # extended precision


def ratio(x: Union[int, float],
          y: Union[int, float],
          percentage: bool = False) -> float:
    """
    Calculate ratio between x and y
    :param x: first value
    :param y: second value
    :param percentage: if true result wil lbe expressed as percentage
    :return: Ratio in string format
    """
    if y == 0:
        raise ZeroDivisionError()
    if percentage:
        return x * PERCENT / y
    else:
        return x / y


def ratio_str(x: Union[int, float],
              y: Union[int, float],
              percentage: bool = False,
              decimals: int = DEFAULT_NUMBER_OF_DECIMALS) -> str:
    """
    Calculate ratio between x and y
    :param x: first value
    :param y: second value
    :param percentage: if true result wil lbe expressed as percentage
    :param decimals: number of decimals to be shown
    :return: Ratio in string format
    """
    return f"{ratio(x, y, percentage):0.{decimals}f}"


FLOAT_DELTA = 0.000001


# unittest OK
def float_equals(value1: Union[float, int],
                 value2: Union[float, int],
                 margin: float = FLOAT_DELTA) -> bool:
    """
    Determine whether two floats are "equal enough"
    :param value1: First value
    :param value2: Second value
    :param margin: Margin to determine equality
    :return: True if difference between values is less than FLOAT_DELTA
    """
    return abs(value2 - value1) <= margin


# unittest OK
def float_not_equals(value1: Union[float, int],
                     value2: Union[float, int],
                     margin: float = FLOAT_DELTA) -> bool:
    """
    Determine whether two floats are not "equal enough"
    :param value1: First value
    :param value2: Second value
    :param margin: Margin to determine equality
    :return: True if difference between values is greater than FLOAT_DELTA
    """
    return not float_equals(value1, value2, margin)


# Unittest OK
def sign(value: Union[float, int]) -> int:
    """
    Determine the sign of a number.
    :param value: number
    :return: 1 is positive, -1 if negative
    """
    return (1, -1)[value < 0]


# Unittest OK
def opposite_sign(value: Union[float, int]) -> int:
    """
    Determine the opposite sign of a number.
    :param value: number
    :return: -1 is positive, 1 if negative
    """
    return -1 * sign(value)


# Unittest OK
def same_sign(value1: Union[int, float], value2: Union[int, float]) -> bool:
    """
    Determine whether both values have the same sign
    :param value1: first value
    :param value2: second value
    :return: True if both values have the same sign
    """
    return sign(value1) == sign(value2)


# Unittest OK
def different_sign(value1: Union[int, float],
                   value2: Union[int, float]) -> bool:
    """
    Determine whether both values have a different sign
    :param value1: first value
    :param value2: second value
    :return: True if both values have a different sign
    """
    return not same_sign(value1, value2)



if __name__ == "__main__":
    raise NotImplementedError(f"This module is not meant to be run directly: {__file__}")
