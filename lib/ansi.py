"""
Ansi console styling module
"""

# ANSI-stijl reset
RESET = "\033[0m"

# Stijlen
BOLD = "\033[1m"
ITALIC = "\033[3m"
UNDERLINE = "\033[4m"

# Voorgrondkleuren
BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"

# Helder (bright) voorgrondkleuren
BRIGHT_BLACK = "\033[90m"
BRIGHT_RED = "\033[91m"
BRIGHT_GREEN = "\033[92m"
BRIGHT_YELLOW = "\033[93m"
BRIGHT_BLUE = "\033[94m"
BRIGHT_MAGENTA = "\033[95m"
BRIGHT_CYAN = "\033[96m"
BRIGHT_WHITE = "\033[97m"

# Achtergrondkleuren
BG_BLACK = "\033[40m"
BG_RED = "\033[41m"
BG_GREEN = "\033[42m"
BG_YELLOW = "\033[43m"
BG_BLUE = "\033[44m"
BG_MAGENTA = "\033[45m"
BG_CYAN = "\033[46m"
BG_WHITE = "\033[47m"

# Helder (bright) achtergrondkleuren
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


def red():
    """
    Provides a function to reset the terminal color and set it to red.
    """
    reset()
    print(RED, end='')


def green():
    """
    Provides a function to reset the terminal color and set it to green
    """
    reset()
    print(GREEN, end='')


def yellow():
    """
    Provides a function to reset the terminal color and set it to yellow.
    """
    reset()
    print(YELLOW, end='')


def blue():
    """
    Provides a function to reset the terminal color and set it to blue.
    """
    reset()
    print(BLUE, end='')


def magenta():
    """
    Provides a function to reset the terminal color and set it to magenta.
    """
    reset()
    print(MAGENTA, end='')


def print_red(text):
    """
    Prints the given text in red color.

    This function formats the provided text to be displayed in red
    color by utilizing the necessary commands. It ensures that the
    text output is temporarily styled in red and then resets the
    styling after being printed.
    """
    red()
    print(text)
    reset()


def print_green(text):
    """
    Prints the given text in green color.

    This function formats the provided text to be displayed in green
    color by utilizing the necessary commands. It ensures that the
    text output is temporarily styled in red and then resets the
    styling after being printed.
    """

    green()
    print(text)
    reset()


def print_yellow(text):
    """
    Prints the given text in yellow color.

    This function formats the provided text to be displayed in yellow
    color by utilizing the necessary commands. It ensures that the
    text output is temporarily styled in red and then resets the
    styling after being printed.
    """
    yellow()
    print(text)
    reset()


def print_blue(text):
    """
    Prints the given text in blue  color.

    This function formats the provided text to be displayed in blue
    color by utilizing the necessary commands. It ensures that the
    text output is temporarily styled in red and then resets the
    styling after being printed.
    """
    blue()
    print(text)
    reset()


def print_magenta(text):
    """
    Prints the given text in magenta color.

    This function formats the provided text to be displayed in magenta
    color by utilizing the necessary commands. It ensures that the
    text output is temporarily styled in red and then resets the
    styling after being printed.
    """

    magenta()
    print(text)
    reset()
