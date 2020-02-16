from dataclasses import dataclass
from typing import Tuple, Union


class Node:
    def __lt__(self, other):
        return repr(self) < repr(other)


@dataclass(frozen=True)
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
        if isinstance(other, Not) and self == other.child:
            return Bit(0)
        return And.new(self, other)

    def __xor__(self, other):
        if self.value == 0:
            return other
        if other.value == 0:
            return self
        if self.value == 1:
            return ~other
        if other.value == 1:
            return ~self
        raise NotImplementedError


@dataclass(frozen=True)
class Not(Node):
    """Unitary NOT, represented with `~` rather than `!` or `not`."""

    child: Node

    def __str__(self):
        return f"~({str(self.child)})"

    def __invert__(self):
        return self.child

    def __and__(self, other):
        if isinstance(other, Bit):
            return other & self
        if self.child == other:
            return Bit(0)
        return And.new(self, other)

    @property
    def value(self):
        if self.child.value in (0, 1):
            return not self.child.value
        if isinstance(self.child.value, str):
            return str(self)
        raise NotImplementedError


@dataclass(frozen=True)
class And(Node):
    """Binary AND, represented with `&`."""

    children: Tuple[Node]

    @staticmethod
    def new(*children):
        # Flatten any direct children that are also ANDs of something.
        new_children = set()
        for child in children:
            if isinstance(child, And):
                for grandchild in child.children:
                    new_children.add(grandchild)
            else:
                new_children.add(child)

        # If any children negate each other, the result is 0.
        for child in new_children:
            if isinstance(child, Not) and child.child in new_children:
                return Bit(0)

        # Otherwise aggregate all children that are being ANDed together.
        return And(children=tuple(sorted(new_children)))

    def __str__(self):
        return "&".join(str(n) for n in self.children)

    def __invert__(self):
        # Todo: push down (and make ORs instead)?
        return Not(self)

    def __and__(self, other):
        if other in self.children:
            return self
        if isinstance(other, And):
            return And.new(*(self.children + other.children))
        if isinstance(other, Not) and self == other.child:
            return Bit(0)
        return And.new(other, *self.children)
