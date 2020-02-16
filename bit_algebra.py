from enum import Enum


class Bit:
    def __init__(self, value):
        """Value should be 0, 1, or a unique name."""
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


class Not:
    """Unitary NOT, represented with `~` rather than `!` or `not`."""

    def __init__(self, child):
        self.child = child

    def __repr__(self):
        return f"Not({repr(self.child)})"

    def __str__(self):
        return f"~{str(self.child)}"

    def __invert__(self):
        return self.child

    @property
    def value(self):
        if self.child.value in (0, 1):
            return not self.child.value
