"""
Ansi console styling module
"""

# Reset code
RESET = "\033[0m"

# Styles
BOLD = "\033[1m"
ITALIC = "\033[3m"
UNDERLINE = "\033[4m"
INVERT = "\033[7m"

# Foreground colours
BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"

# Bright foreground colours
BRIGHT_BLACK = "\033[90m"
BRIGHT_RED = "\033[91m"
BRIGHT_GREEN = "\033[92m"
BRIGHT_YELLOW = "\033[93m"
BRIGHT_BLUE = "\033[94m"
BRIGHT_MAGENTA = "\033[95m"
BRIGHT_CYAN = "\033[96m"
BRIGHT_WHITE = "\033[97m"

# Background colours
BG_BLACK = "\033[40m"
BG_RED = "\033[41m"
BG_GREEN = "\033[42m"
BG_YELLOW = "\033[43m"
BG_BLUE = "\033[44m"
BG_MAGENTA = "\033[45m"
BG_CYAN = "\033[46m"
BG_WHITE = "\033[47m"

# Bright background colours
BG_BRIGHT_BLACK = "\033[100m"
BG_BRIGHT_RED = "\033[101m"
BG_BRIGHT_GREEN = "\033[102m"
BG_BRIGHT_YELLOW = "\033[103m"
BG_BRIGHT_BLUE = "\033[104m"
BG_BRIGHT_MAGENTA = "\033[105m"
BG_BRIGHT_CYAN = "\033[106m"
BG_BRIGHT_WHITE = "\033[107m"


def reset():
    """
    Resets the terminal display to its default settings.

    This function outputs the ANSI escape sequence
    stored in the global `RESET` variable. It is intended
    to restore the terminal's visual appearance after it
    has been modified by other terminal-based styling
    or formatting commands. It does not return any value.
   """
    print(RESET, end='')


def _generic_set_colour(colour: str) -> None:
    """
    Sets the terminal text color to the specified color.

    This function is used to change the text color for terminal output. It resets
    the terminal settings before applying the new color setting and ensures the
    color is immediately applied via print.

    :param colour: The name of the color to set the terminal text to.
    """
    reset()
    print(colour, end='')


def black():
    """
    Provides a function to reset the terminal color and set it to black.
    :return:
    """
    _generic_set_colour(BLACK)


def red():
    """
    Provides a function to reset the terminal color and set it to red.
    """
    _generic_set_colour(RED)


def green():
    """
    Provides a function to reset the terminal color and set it to green
    """
    _generic_set_colour(GREEN)


def yellow():
    """
    Provides a function to reset the terminal color and set it to yellow.
    """
    _generic_set_colour(YELLOW)


def blue():
    """
    Provides a function to reset the terminal color and set it to blue.
    """
    _generic_set_colour(BLUE)


def cyan():
    """
    Provides a function to reset the terminal color and set it to cyan.
    """
    _generic_set_colour(MAGENTA)


def magenta():
    """
    Provides a function to reset the terminal color and set it to magenta.
    """
    _generic_set_colour(MAGENTA)


def _print_generic(color_function: callable, text: str) -> None:
    """
    This function prints a styled text using a provided color formatting function.
    The `color_function` is applied before the text is printed, and a reset operation
    is performed thereafter. It ensures the text is displayed in the intended style
    while resetting formatting for subsequent terminal output.

    :param color_function: A callable that applies a color or style to the output text
                           when invoked (e.g., a function for terminal color settings).
    :param text: The text string to be printed, styled using the given `color_function`.
    """
    color_function()
    print(text)
    reset()


def print_black(text: str):
    """
    Prints the given text in black.

    This function formats the provided text to be displayed in black
    color by utilizing the necessary commands. It ensures that the
    text output is temporarily styled in red and then resets the
    styling after being printed.
    """
    _print_generic(black, text)


def print_red(text: str):
    """
    Prints the given text in red color.

    This function formats the provided text to be displayed in red
    color by utilizing the necessary commands. It ensures that the
    text output is temporarily styled in red and then resets the
    styling after being printed.
    """
    _print_generic(red, text)


def print_green(text: str):
    """
    Prints the given text in green color.

    This function formats the provided text to be displayed in green
    color by utilizing the necessary commands. It ensures that the
    text output is temporarily styled in red and then resets the
    styling after being printed.
    """
    _print_generic(green, text)


def print_yellow(text: str):
    """
    Prints the given text in yellow color.

    This function formats the provided text to be displayed in yellow
    color by utilizing the necessary commands. It ensures that the
    text output is temporarily styled in red and then resets the
    styling after being printed.
    """
    _print_generic(yellow, text)


def print_blue(text: str):
    """
    Prints the given text in blue  color.

    This function formats the provided text to be displayed in blue
    color by utilizing the necessary commands. It ensures that the
    text output is temporarily styled in red and then resets the
    styling after being printed.
    """
    _print_generic(blue, text)


def print_cyan(text: str):
    """
    Prints the given text in magenta color.

    This function formats the provided text to be displayed in magenta
    color by utilizing the necessary commands. It ensures that the
    text output is temporarily styled in red and then resets the
    styling after being printed.
    """
    _print_generic(cyan, text)


def print_magenta(text: str):
    """
    Prints the given text in magenta color.

    This function formats the provided text to be displayed in magenta
    color by utilizing the necessary commands. It ensures that the
    text output is temporarily styled in red and then resets the
    styling after being printed.
    """
    _print_generic(magenta, text)


def demo() -> None:
    """
    Demo function for the ansi module.
    """
    for style in range(8):
        for fg in range(30, 38):
            for bg in range(40, 48):
                print(f"\033[{style};{fg};{bg}m {style};{fg};{bg} \033[0m", end="  ")
            print()


if __name__ == "__main__":
    raise NotImplementedError(f"This module is not meant to be run directly: {__file__}")
