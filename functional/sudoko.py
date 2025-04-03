"""
Solve a sudoku
"""
import copy

from typing import List

GIVEN = [
    [1, 0, 2, 0, 7, 0, 0, 3, 6],
    [0, 8, 7, 0, 0, 6, 2, 5, 0],
    [0, 0, 0, 8, 3, 0, 0, 0, 0],
    [4, 0, 0, 7, 0, 0, 6, 0, 0],
    [0, 7, 5, 0, 4, 0, 0, 0, 8],
    [0, 6, 0, 0, 9, 1, 7, 0, 5],
    [0, 0, 0, 3, 0, 0, 1, 6, 0],
    [0, 3, 4, 0, 0, 8, 0, 9, 0],
    [0, 5, 1, 0, 6, 4, 3, 0, 0]]

current = copy.deepcopy(GIVEN)


def consistent9(data: List[int]) -> bool:
    """
    Determines if a given list of integers contains no duplicate values strictly
    between 1 and 9 (inclusive), excluding non-positive numbers and numbers
    greater than or equal to 10.

    :param data: A list of integers to be checked for duplicates in the range 1 to 9.
    :type data: List[int]
    :return: A boolean value indicating whether the list is consistent (i.e., no
        duplicates in the range from 1 to 9).
    :rtype: bool
    """
    # print(f"testing {data}")
    temp = sorted([x for x in data if 0 < x < 10])
    for i in range(len(temp) - 1):
        if temp[i] == temp[i + 1]:
            return False
    return True


def get_block(x, y):
    """
    Retrieve a 3x3 block from a 9x9 grid based on the specified block coordinates.

    The function extracts a sub-block of the larger grid given the block's
    position in the grid. It utilizes a nested list comprehension to gather
    the values within the specified 3x3 block.

    :param x: Horizontal index of the block within the 9x9 grid.
              Valid range is 0 to 2 (representing the three blocks).
    :type x: int
    :param y: Vertical index of the block within the 9x9 grid.
              Valid range is 0 to 2 (representing the three blocks).
    :type y: int
    :return: List containing the elements of the 3x3 block extracted from
             the grid.
    :rtype: list
    """
    return [current[y * 3 + u][x * 3 + v] for u in range(3) for v in range(3)]


def get_coordinates(pos):
    """
    Calculate the row and column coordinates on a 9x9 grid based on a linear position.

    This utility function converts a single linear index (``pos``) into a tuple
    representing the 2D coordinates (row, column) on a 9x9 grid. The grid is
    considered zero-indexed. The row index is calculated via integer division,
    and the column index is determined using the modulo operation.

    :param pos: Linear position on the grid (0 to 80)
    :type pos: int
    :return: A tuple containing the row and column coordinates
    :rtype: tuple[int, int]
    """
    return pos // 9, pos % 9


def get_value(pos):
    """
    Retrieves the value from a two-dimensional structure at a specified position.

    This function first computes the coordinates of the specified position within
    a two-dimensional structure, then retrieves the corresponding value using
    those coordinates. The function assumes existence of helper functions and
    variables like `get_coordinates` to perform intermediate computations and access
    a global or scoped two-dimensional structure `current`.

    :param pos: An integer or other valid representation of the position whose
        value will be retrieved within the two-dimensional structure.
    :return: The value found at the position specified by the given coordinates.
    """
    y,x = get_coordinates(pos)
    return current[y][x]


def consistent() -> bool:
    for x in range(9):
        # print(f"checking row {x}")
        if not consistent9(current[x]):
            return False
        # print(f"checking column {x}")
        if not consistent9([current[i][x] for i in range(9)]):
            return False

        i = x % 3
        j = x // 3
        # print(f"checking block {j + 1},{i + 1}")
        blok = get_block(j, i)

        if not consistent9(blok):
            return False
    return True


def print_current():
    print("################")
    for row in current:
        for col in row:
            if col == 0:
                print(".", end="")
            else:
                print(col, end="")
        print()
    print("################")


def solve(pos):
    y, x = get_coordinates(pos)
    print(f"\rsolving {pos} or  {y},{x}")

    # Hebben we het einde bereikt?
    if pos == 81:
        if consistent():
            print("End reached")
            print_current()
            exit(-1)
        return



    for i in range(9):
        current[y][x] = i + 1
        solve(pos + 1)
def solve_(pos):
    for a in range(pos, 81):
        for v in range(9):
            if current[a//9][a%9] == 0:
                current[a//9][a%9] = v+1
                solve_(a+1)
                current[a//9][a%9] = 0
                return



print_current()
solve(0)
print_current()
# print(consistent())
