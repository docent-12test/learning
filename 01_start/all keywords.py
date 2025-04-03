# False, None, True: Gebruik van booleaanse en speciale waarden
is_ready = True
data = None
if not False:
    print("Demo script is running.")


# and, as, assert, break, continue, del, elif, else, except, finally, for, from, global, if, import, in, is, not, or, pass, raise, return, try, while, with, yield
def demo_function():
    global data  # gebruik van global
    data = {"key1": 1, "key2": 2}

    try:
        for key in data:
            if data[key] % 2 == 0 and key is not None:  # gebruik van and, is, not
                print(f"{key} is even")
            elif key in data:  # gebruik van elif, in
                continue
            else:
                break
    except KeyError as e:
        print(f"KeyError occurred: {e}")
        raise
    finally:
        print("Demo function completed")


# as, with: Gebruik van contextbeheer
with open("example.txt", "w") as file:
    file.write("This is a demo text file.")

# async, await: Voorbeelden voor asynchrone programmeerstijl
import asyncio


async def async_task():
    await asyncio.sleep(1)  # gebruik van await
    return "Task completed!"


# class, def, lambda: Definieer een klasse en een functie met een lambda
class ExampleClass:
    def __init__(self, value):
        self.value = value

    def multiply(self):
        return lambda x: x * self.value  # Gebruik van lambda


# nonlocal: Gebruik variabelen buiten de huidige scope
def outer_function():
    counter = 0

    def inner_counter():
        nonlocal counter  # Gebruik van nonlocal
        counter += 1
        return counter

    return inner_counter


# Decorators: Gebruik van functies als decorateurs
def decorator(func):
    def wrapper(*args, **kwargs):
        print(f"Calling function: {func.__name__}")
        return func(*args, **kwargs)

    return wrapper


@decorator
def decorated_function():
    print("This function is decorated!")


# Demonstratie van alle delen
if __name__ == "__main__":
    assert is_ready, "Script is not ready"  # gebruik van assert

    demo_function()

    example = ExampleClass(10)
    doubler = example.multiply()
    print(doubler(5))  # Output: 50

    counter = outer_function()
    print(counter())  # Output: 1
    print(counter())  # Output: 2

    decorated_function()

    result = asyncio.run(async_task())  # Gebruik van async/await
    print(result)

    # Booleaanse operatoren gebruiken
    condition = True or False and not False
    print(f"Condition result: {condition}")

    # Delete object
    del example
    print("Example class instance deleted.")
