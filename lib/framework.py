
from lib.ansi import print_red

def MustBeTested(func):
    def wrapper(*args, **kwargs):
        print_red(f"Tests must still be coded for function: {func.__name__}()")
        return func(*args, **kwargs)
    return wrapper