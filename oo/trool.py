"""

"""
VALUES = {
    0 : "FALSE",
    1 : "TRUE",
    2 : "UNKNOWN"
}
class Trool:

    def __init__(self, value = 2):
        self._value = value

    def __repr__(self):
        return f"{VALUES[self.value]})"

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if value not in VALUES.keys():
            raise ValueError(f"Invalid value: {value}")

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __le__(self, other):
        return self.value <= other.value

    def __ge__(self, other):
        return self.value >= other.value

    def __ne__(self, other):
        return self.value != other.value

    def __bool__(self):
        if self.value == VALUES[0]:
            return False
        elif self.value == VALUES[1]:
            return True
        else:
            return None

    def __or__(self, other):