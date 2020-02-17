from collections import Counter
from dataclasses import dataclass
from typing import Tuple, Union


class BitExpr:
    def __lt__(self, other):
        return repr(self) < repr(other)


@dataclass(frozen=True)
class Bit(BitExpr):
    value: Union[bool, str] = 0  # Value should be 0, 1, or a unique name.

    def __str__(self):
        return str(self.value)

    def __invert__(self) -> BitExpr:
        if self.value == 0:
            return Bit(1)
        if self.value == 1:
            return Bit(0)
        return Xor.new(Bit(1), self)

    def __and__(self, other: BitExpr) -> BitExpr:
        if self.value == 0:
            return self
        if self.value == 1:
            return other
        if isinstance(other, Bit):
            if other.value == 0:
                return other
            if other.value == 1 or self == other:
                return self
        if isinstance(other, Xor):
            return Xor.new(*[self & c for c in other.children])
        return And.new(self, other)

    def __rand__(self, other: BitExpr) -> BitExpr:
        return self & other

    def __xor__(self, other: BitExpr) -> BitExpr:
        if self.value == 0:
            return other
        if self.value == 1:
            return ~other
        if isinstance(other, Bit):
            if other.value == 0:
                return self
            if other.value == 1:
                return ~self
        return Xor.new(self, other)

    def __rxor__(self, other: BitExpr) -> BitExpr:
        return self ^ other

    def __or__(self, other: BitExpr) -> BitExpr:
        if self.value == 0:
            return other
        if self.value == 1:
            return self
        if isinstance(other, Bit):
            if other.value == 0:
                return self
            if other.value == 1:
                return other
        return Xor.new(self, other, self & other)

    def __ror__(self, other: BitExpr) -> BitExpr:
        return self | other


@dataclass(frozen=True)
class And(BitExpr):
    """Binary AND, represented with `&`."""

    children: Tuple[BitExpr]

    def __str__(self):
        return "&".join(str(n) for n in self.children)

    @staticmethod
    def new(*children) -> BitExpr:
        # Flatten any direct children that are also ANDs of something.
        new_children = set()
        for child in children:
            if isinstance(child, And):
                new_children.update(child.children)
            elif isinstance(child, Bit):
                if child.value == 0:
                    return Bit(0)
                if child.value != 1:
                    new_children.add(child)
            else:
                raise NotImplementedError

        assert Bit(0) not in new_children and Bit(1) not in new_children

        if len(new_children) == 1:
            return new_children.pop()

        # Otherwise aggregate all children that are being ANDed together.
        return And(children=tuple(sorted(new_children)))

    def __invert__(self) -> BitExpr:
        return Xor.new(Bit(1), self)

    def __and__(self, other):
        if isinstance(other, Bit):
            return other & self
        if isinstance(other, And):
            return And.new(*(self.children + other.children))
        if isinstance(other, Xor):
            return Xor.new(*[c & self for c in other.children])
        raise NotImplementedError

    def __rand__(self, other: BitExpr) -> BitExpr:
        return self & other

    def __xor__(self, other):
        return Xor.new(self, other)

    def __rxor__(self, other: BitExpr) -> BitExpr:
        return self ^ other


@dataclass(frozen=True)
class Xor(BitExpr):
    """Binary XOR, represented with `^`."""

    children: Tuple[BitExpr]

    def __str__(self) -> str:
        return "^".join(str(c) for c in self.children)

    @staticmethod
    def new(*children):
        child_counts = Counter()
        for child in children:
            if isinstance(child, Xor):
                child_counts.update(child.children)
            elif child != Bit(0):
                child_counts[child] += 1

        # Children that match each other cancel out, so we can keep just the count % 2.
        new_children = [child for child, count in child_counts.items() if count % 2]

        if not new_children:
            return Bit(0)
        if len(new_children) == 1:
            return new_children[0]

        return Xor(children=tuple(sorted(new_children)))

    def __invert__(self) -> BitExpr:
        return Xor.new(Bit(1), *self.children)

    def __and__(self, other: BitExpr) -> BitExpr:
        if isinstance(other, Bit) or isinstance(other, And):
            return other & self
        return Xor.new(*[a & b for a in self.children for b in other.children])

    def __xor__(self, other: BitExpr) -> BitExpr:
        if isinstance(other, Bit) or isinstance(other, And):
            return other ^ self
        return Xor.new(*(self.children + other.children))

    def __or__(self, other: BitExpr) -> BitExpr:
        if isinstance(other, Bit) or isinstance(other, And):
            return other | self
        return Xor.new(self, other, self & other)
