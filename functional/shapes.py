"""
Shapes without OO
"""

SCREENWIDTH = 50
SCREENHEIGHT = 30

screen = [['.' for _ in range(SCREENWIDTH)] for _ in range(SCREENHEIGHT)]


def check_type(value, type_) -> bool:
    """
    Checks if the given value is of the specified type.

    This function validates whether a given value is an instance
    of a provided type. If the value does not match the type,
    a ValueError is raised.

    :param value: The value to check.
    :param type_: The expected type of the value.
    :return: True if the value is of the specified type.
    :rtype: bool
    :raises ValueError: If the value is not of the specified type.
    """
    if not isinstance(value, type_):
        raise ValueError(f"Value {value} must be of type {type_}")
    return True


def check_types(*args):
    """
    Checks the types of given arguments in pairs to ensure correctness.

    This function takes an even number of arguments where each pair consists of
    an item and its corresponding expected type. It verifies if items match the
    expected types and raises an error for mismatches.

    :param args: A sequence of elements where each pair is (item, expected_type).
    :type args: tuple
    :raises ValueError: If the number of arguments passed is not even.
    """
    if len(args) % 2 != 0:
        raise ValueError("Must be an even number of arguments")
    for i in range(0, len(args), 2):
        check_type(args[i], args[i + 1])


def draw_squares() -> None:
    """
    Draws squares on a predefined 2D screen based on the provided shape data.

    For each square descriptor in the `shapes` list, the function will:
    1. Validate that each attribute of the square is of the correct type.
    2. Draw the square on the predefined `screen` filled with the specified color at
       the given coordinates (`x`, `y`) and of the specified side length.

    Attributes:
        screen (list[list[str]]): A 2D array representing the drawing canvas where
            each character in the array corresponds to a pixel.
        shapes (list[tuple[int, int, str, int]]): A list of square descriptors,
            where each descriptor is a tuple containing the x-coordinate (int),
            y-coordinate (int), color (str), and side length (int).

    :raises TypeError:
        If any attribute of a square descriptor in `shapes` does not match its
        expected type.

    :returns:
        This function does not return any value as it directly modifies the
        `screen` and outputs to the console.
    """
    for shape in shapes:
        x, y, color, side = shape
        check_types(x, int, y, int, color, str, side, int)

        print(f"Drawing square at {x}, {y}")
        for j in range(side):
            for i in range(side):
                screen[y + j][x + i] = color
    for line in screen:
        print(''.join(line))


def get_area() -> int:
    """
    Calculate the total area of given square shapes.

    This function iterates over a collection of shapes, which are assumed
    to be squares, and calculates their total area by summing the area of
    each square. Each shape is represented by a sequence where the fourth
    element is the length of the side of the square. The function returns
    the cumulative area of all squares in the collection.

    :raises IndexError: If any `shape` does not contain sufficient elements
        for side length retrieval.
    :return: The total calculated area of all squares.
    :rtype: int
    """
    return sum(shape[3] ** 2 for shape in shapes)


# shape inner structure [x, y, color,  side]
# [2, 4, 'r', side =4

shapes = [[20, 5, 'g', 10]]

draw_squares()
print(f"Oppervlakte {get_area()}")

"""
Disadvantages:
1. The shape attributes (e.g., x, y, color, size) are represented as indices of a list, 
   which reduces readability and leads to potential errors. 
   Use named constants or dictionaries to represent shape properties.
   
2. Avoid using non-local variables to store data.
   Instead, use class attributes or instance variables to store data.
   
   
2. **Extract Functions**:
    - The logic for drawing squares could be split into smaller helper functions to improve clarity and reduce complexity.

3. **Introduce Type Checking**:
    - Add type hints and enforce better validation using Python's type annotations.



The refactored code incorporates all these improvements:
### Refactored Code
"""

def a(*args, **kwargs):
    print(type(args))
    print(type(kwargs))

a()