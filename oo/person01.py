"""
My first class
"""

class Person:
    def __init__(self):
        self.name = "John"
        self.age = 36


    def __repr__(self):
        return f"Person(name={self.name}, age={self.age})"




a = Person()
print(a)
print(a.name)
print(a.age)

b = Person()
print(b)
print(b.name)
print(b.age)

b.name = "Jane"
print(b.name)
print(a.name)
