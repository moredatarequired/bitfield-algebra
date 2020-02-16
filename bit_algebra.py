from enum import Enum


class Bit:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Bit({self.value})"

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        return self.value == other.value

    def __invert__(self):
        if self.value == 0:
            return Bit(1)
        if self.value == 1:
            return Bit(0)
        return Not(Bit(self.value[:]))


# A bit can be True, or False, or variable / unknown.
class Variable:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Variable({self.name})"

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def __not__(self):
        return Not(self)


class Not:
    def __init__(self, child):
        self.child = child

