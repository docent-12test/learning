"""
Math and statistics
"""
from decimal import Decimal
from typing import Union

from claar import constants

FLOAT_DELTA = Decimal('0.000001')

PERCENT = Decimal(constants.PERCENT)
DEFAULT_NUMBER_OF_DECIMALS = 2

L = ".1f"  # limited precision
N = f".{DEFAULT_NUMBER_OF_DECIMALS}f"  # normal precision
E = ".5f"  # extended precision

SL = f"+{L}"  # limited precision
SN = f"+{N}"  # normal precision
SE = f"+{E}"  # extended precision


def ratio(numerator: Union[int, float, Decimal],
          denominator: Union[int, float, Decimal],
          as_percentage: bool = False) -> Decimal:
    """
    Calculate the ratio of two numbers, optionally returning it as a percentage.

    The function computes the ratio of a numerator to a denominator. It allows the
    option to specify whether the result should be returned as a percentage or as
    a decimal value. If the denominator is zero, the function raises a
    `ZeroDivisionError`.

    :param numerator: The numerator of the fraction. It can be of type int, float,
        or Decimal.
    :param denominator: The denominator of the fraction. It can be of type int,
        float, or Decimal. Must not be zero.
    :param as_percentage: A boolean flag to indicate if the result should be
        returned as a percentage. Defaults to False.
    :return: The computed ratio of the numerator to the denominator as a Decimal.
    :raises ZeroDivisionError: If the denominator is zero.
    """

    if denominator == 0:
        raise ZeroDivisionError(f"Can not divide {numerator} by zero")
    ratio_result = Decimal(numerator) / Decimal(denominator)
    return ratio_result * PERCENT if as_percentage else ratio_result


def ratio_str(numerator: Union[int, float, Decimal],
              denominator: Union[int, float, Decimal],
              as_percentage: bool = False,
              decimals: int = DEFAULT_NUMBER_OF_DECIMALS) -> str:
    """
    Generate a formatted string representation of the ratio between
    a numerator and a denominator. Provides the option to display the
    ratio as a percentage and set the number of decimal places.

    :param numerator: The number representing the numerator of the ratio.
    :param denominator: The number representing the denominator of the ratio.
    :param as_percentage: A boolean flag indicating whether the ratio
                          should be formatted as a percentage. Defaults to False.
    :param decimals: An integer specifying the number of decimal places
                     of precision for the output string. Defaults to
                     the specified `DEFAULT_NUMBER_OF_DECIMALS`.
    :return: A string representing the formatted ratio, optionally as a
             percentage, rounded to the specified number of decimal places.
    """
    return f"{ratio(numerator, denominator, as_percentage):+.{decimals}f}"

def equal(value1: Union[float, int, Decimal],
          value2: Union[float, int, Decimal],
          margin: float = FLOAT_DELTA) -> bool:
    """
    Determines if two numerical values are equal within a specified margin.

    This function calculates the absolute difference between two input values and checks
    if it is less than or equal to the specified margin. The default margin is defined by
    the constant FLOAT_DELTA.

    :param value1: The first numerical value to compare.
    :type value1: Union[float, int, Decimal]
    :param value2: The second numerical value to compare.
    :type value2: Union[float, int, Decimal]
    :param margin: The acceptable difference threshold within which the two values
        are considered equal. Defaults to FLOAT_DELTA.
    :type margin: float
    :return: True if the absolute difference between the two values is less than or
        equal to the margin, otherwise False.
    :rtype: bool
    """
    return abs(value2 - value1) <= margin



def different(value1: Union[float, int, Decimal],
              value2: Union[float, int, Decimal],
              margin: float = FLOAT_DELTA) -> bool:
    """
    Compares two numerical values to determine if they are different within a given margin
    of error. This function uses the `equal` function internally to verify equality, and
    returns the negation of that result. The margin parameter allows for customization of
    precision when assessing the difference.

    :param value1: The first numeric value to compare.
    :type value1: Union[float, int, Decimal]
    :param value2: The second numeric value to compare.
    :type value2: Union[float, int, Decimal]
    :param margin: The allowable margin of difference between the two values. Defaults
        to `FLOAT_DELTA`.
    :type margin: float
    :return: Returns `True` if the two values are considered different within the given
        margin; otherwise returns `False`.
    :rtype: bool
    """
    return not equal(value1, value2, margin)


def sign(value: Union[float, int]) -> int:
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
