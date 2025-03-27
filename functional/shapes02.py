"""
Shape without OO
"""

SCREENWIDTH = 50
SCREENHEIGHT = 30

screen = [['.' for _ in range(SCREENWIDTH)] for _ in range(SCREENHEIGHT)]



def draw_screen() -> None:
    for shape in shapes:
        name, x, y, color = shape[:4]
        print(f"Drawing shape: {name} at {x}, {y}")
        if shape[0] == 'SQUARE':
            side = shape[4]
            for j in range(side):
                for i in range(side):
                    if i == 0 or i == side - 1 or j == 0 or j == side - 1:
                        screen[y + j][x + i] = color
    for line in screen:
        print(''.join(line))

def get_area():
    area = 0
    for shape in shapes:
        name, x, y, color = shape[:4]
        print(f"Drawing shape: {name} at {x}, {y}")
        if shape[0] == 'SQUARE':
            side = shape[4]
            area += side * side
    return area

    #
    # def get_dots(self):
    #     ret = set()
    #     for angle in range(360):
    #         x = int(self.radius * math.cos(math.radians(angle)) + self.position.x)
    #         y = int(self.radius * math.sin(math.radians(angle)) + self.position.y)
    #         ret.add(Coordinate(x, y))
    #     return ret
    #
    # def center(self):
    #     return self.position
    #

# shape inner structure [name, x, y, color,  specific data]
# ['SQUARE', 2, 4, 'r', side =4
shapes =[  ['SQUARE', 20, 5, 'g', 10]
#         ['RECTANGLE', 10, 5, 'r', 10, 5],    ['CIRCLE', 15, 15, 'b', 10]
        ]

draw_screen()
print(get_area())



