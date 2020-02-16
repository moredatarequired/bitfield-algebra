from dataclasses import dataclass
from typing import List, Union


class Node:
    pass


@dataclass(frozen=True, order=True)
class Bit(Node):
    value: Union[bool, str] = 0  # Value should be 0, 1, or a unique name.

    def __str__(self):
        return str(self.value)

    def __invert__(self):
        if self.value == 0:
            return Bit(1)
        if self.value == 1:
            return Bit(0)
        return Not(self)

    def __and__(self, other):
        if self.value == 0 or other.value == 0:
            return Bit(0)
        if self.value == 1:
            return other
        if other.value == 1:
            return self
        if self == other:
            return self
        return And.new(self, other)


@dataclass(frozen=True)
class Not(Node):
    """Unitary NOT, represented with `~` rather than `!` or `not`."""

    child: Node

    def __str__(self):
        return f"~({str(self.child)})"

    def __invert__(self):
        return self.child

    @property
    def value(self):
        if self.child.value in (0, 1):
            return not self.child.value


@dataclass(frozen=True)
class And(Node):
    """Binary AND, represented with `&`."""

    children: List[Node]

    @staticmethod
    def new(*children):
        return And(children=list(sorted(children)))

    def __str__(self):
        return "&".join(str(n) for n in self.children)

    def __and__(self, other):
        if other in self.children:
            return self
        raise NotImplementedError
