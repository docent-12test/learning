"""
Inheritance example with shape
"""
from abc import ABC, abstractmethod
import math


class Coordinate:
    """
    Represents a two-dimensional coordinate with x and y values.

    The Coordinate class allows for handling and manipulating coordinates in a
    2D space. It supports common operations like addition, subtraction, equality
    checks, inequality checks, and allows for usage in hashed data structures 
    like sets.

    :ivar x: The x-coordinate value.
    :type x: int
    :ivar y: The y-coordinate value.
    :type y: int
    """

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"(x={self.x}, y={self.y})"

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        return Coordinate(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Coordinate(self.x - other.x, self.y - other.y)

    def __hash__(self):
        return hash((self.x, self.y))


class Shape(ABC):
    """
    Represents an abstract base class for geometric shapes.

    This class serves as a blueprint for various geometric shapes. It 
    defines attributes such as position and color, and declares abstract 
    methods that must be implemented by subclasses. These abstract methods 
    include functionality for representing the shape as a string, calculating 
    its area, perimeter, finding the shape's central point, and obtaining its 
    defining dots/vertices.

    :ivar position: The coordinate position of the shape in a 2D space.
    :type position: Coordinate
    :ivar color: The color representation of the shape.
    :type color: str or any compatible type
    """

    def __init__(self, position: Coordinate, color: str):
        self.color = color
        self.position = position
        if not isinstance(position, Coordinate):
            raise ValueError("Position must be an instance of Coordinate")
        if not isinstance(color, str) or len(color) != 1:
            raise ValueError("Color must be a single character string")

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def area(self):
        """
        """
        pass

    @abstractmethod
    def perimeter(self):
        pass

    @abstractmethod
    def get_dots(self):
        pass

    @abstractmethod
    def center(self):
        pass


class Rectangle(Shape):
    def __init__(self,
                 position: Coordinate,
                 color: str,
                 width: int,
                 height: int):
        Shape.__init__(self, position, color)
        self.width = width
        self.height = height

    def __repr__(self):
        return f"Rectangle(position={self.position}, color={self.color}, width={self.width}, height={self.height})"

    def area(self)  :
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

    def get_dots(self):
        ret = set()
        for x in range(self.width):
            for y in range(self.height):
                if x == 0 or x == self.width - 1 or y == 0 or y == self.height - 1:
                    ret.add(Coordinate(x, y) + self.position)
        return ret

    def center(self):
        return Coordinate(self.position.x + self.width // 2, self.position.y + self.height // 2)


class Circle(Shape):
    def __init__(self, position: Coordinate, color, radius):
        self.radius = radius
        Shape.__init__(self, position, color)

    def __repr__(self):
        return f"Circle(position={self.position}, color={self.color}, radius={self.radius})"

    def area(self):
        return 3.14 * self.radius ** 2

    def perimeter(self):
        return 2 * 3.14 * self.radius

    def get_dots(self):
        ret = set()
        for angle in range(360):
            x = int(self.radius * math.cos(math.radians(angle)) + self.position.x)
            y = int(self.radius * math.sin(math.radians(angle)) + self.position.y)
            ret.add(Coordinate(x, y))
        return ret

    def center(self):
        return self.position


class Square(Rectangle):
    def __init__(self, position: Coordinate, color, side):
        Rectangle.__init__(self, position, color, side, side)

    def __repr__(self):
        return f"Square(position={self.position}, color={self.color}, side={self.width})"


SCREENWIDTH = 50
SCREENHEIGHT = 50

screen = [['.' for _ in range(SCREENWIDTH)] for _ in range(SCREENHEIGHT)]


def draw(shape:Shape) -> None:
    """
    Draws a given shape on the screen by updating the screen array based on the
    shape's dots and color.

    :param shape: Shape object that contains the list of dots to be painted
        on the screen and the color to fill in those positions.
    :type shape: Shape
    :return: None
    """
    for dot in shape.get_dots():
        screen[dot.y][dot.x] = shape.color
    for line in screen:
        print(''.join(line))


r = Rectangle(Coordinate(10, 5), 'r', 10, 5)

shapes = [
    Rectangle(Coordinate(10, 5), 'r', 10, 5),
    Square(Coordinate(20, 5), 'g', 10),
    Circle(Coordinate(15, 15), 'b', 10)
]

for sh in shapes:
    print(f"Drawing shape: {sh}")
    draw(sh)
