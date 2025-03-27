"""
My first class
"""

class Person:
    """
    Represents a person with a name and an age.

    This class is designed to encapsulate the basic attributes of a person,
    specifically their name and age. It provides a convenient way to represent
    a person object and display it as a string for debugging or logging purposes.

    :ivar name: The name of the person.
    :type name: str
    :ivar age: The age of the person.
    :type age: int
    """
    def __init__(self, name:str, age: int):
        self.name = name
        self.age = age

    def __repr__(self):
        return f"Person(name={self.name}, age={self.age})"

    def __eq__(self, other):
        return self.name == other.name and self.age == other.age

    def __lt__(self, other):
        return self.age < other.age

    def is_adult(self):
        """
        Determines if the individual is considered an adult based on their age.

        The method evaluates the `age` attribute of the instance and checks
        if it is greater than or equal to 18. This is used to determine if the
        individual qualifies as an adult.

        :return: A boolean value indicating if the individual is an adult (True) or
            not (False).
        :rtype: bool
        """
        return self.age >= 18

a = Person("John", 36)
b = Person("John", 36)

print(f"{a} == {b} : {a==b}")
b = a

print(f"{a} == {b} : {a==b}")
# a == b   =>   a.__eq__(b)

print(dir(a))
print(vars(a))

a = Person("Jane", 36)
b = Person("Jonh", 13)
print(f"{a} < {b} : {a<b}")
print(f"{b} < {a} : {b<a}")





