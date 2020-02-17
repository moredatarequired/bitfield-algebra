import math
from dataclasses import dataclass
from typing import Tuple

from bit_algebra import Bit


@dataclass(frozen=True)
class BitVector:
    """A vector of bits (such as byte) with known or unknown values."""

    bits: Tuple[Bit]

    @staticmethod
    def new(name, size=8):
        return BitVector(bits=tuple(Bit(f"{name}{i}") for i in range(size)))

    @staticmethod
    def from_value(n: int, size=None):
        if size is None:
            size = math.ceil(math.log(n, 2))
        return BitVector(tuple(Bit((n >> i) % 2) for i in range(size)))

    def __str__(self) -> str:
        return " ".join(str(b) for b in self.bits)

    def __len__(self):
        return len(self.bits)

    def __iter__(self):
        return iter(self.bits)

    def __getitem__(self, i: int) -> Bit:
        return self.bits[i]

    def __invert__(self):
        return BitVector(tuple(~b for b in self.bits))

    def __and__(self, other):
        return BitVector(tuple(s & o for s, o in zip(self, other)))

    def __or__(self, other):
        return BitVector(tuple(s | o for s, o in zip(self, other)))

    def __xor__(self, other):
        return BitVector(tuple(s ^ o for s, o in zip(self, other)))

    def __lshift__(self, n: int):
        return BitVector(tuple([Bit(0)] * n + list(self.bits[:-n])))

    def __rshift__(self, n: int):
        return BitVector(tuple(list(self.bits[n:]) + [Bit(0)] * n))
