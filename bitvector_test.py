from bitvector import BitVector
from bit_algebra import Bit

t = Bit(1)
f = Bit(0)
zeros = BitVector.from_value(0, 8)
ones = BitVector.from_value(0xFF)
x, y = BitVector.new("x"), BitVector.new("y")


def test_zeros_are_zero():
    assert len(zeros) == 8
    assert all([b == f for b in zeros.bits]), str(zeros)


def test_create_mask():
    n = BitVector.from_value(0xDEADBEEF)
    assert tuple(n) == tuple(Bit(int(b)) for b in f"{0xDEADBEEF:016b}"[::-1])


def test_named_bitsequence():
    assert x[0] == Bit("x0") and x[7] == Bit("x7")


def test_readable_str():
    assert str(x) == "x0 x1 x2 x3 x4 x5 x6 x7"


def test_supports_bitwise_not():
    assert ~ones == zeros
    assert ~x[0] == ~Bit("x0")


def test_supports_xor():
    assert x ^ x == zeros
    assert x ^ ~x == ones
    assert str(x ^ y) == "x0^y0 x1^y1 x2^y2 x3^y3 x4^y4 x5^y5 x6^y6 x7^y7"


def test_supports_and():
    assert x & x == x
    assert x & ~x == zeros
    assert str(x & y) == "x0&y0 x1&y1 x2&y2 x3&y3 x4&y4 x5&y5 x6&y6 x7&y7"


def test_supports_or():
    assert x | x == x
    assert x | ~x == ones


def test_supports_lshift():
    z = x << 3
    assert str(z) == "0 0 0 x0 x1 x2 x3 x4"
    assert all(z[i] == f for i in range(3))
    assert z[3] == Bit("x0")


def test_supports_rshift():
    z = x >> 5
    assert str(z) == "x5 x6 x7 0 0 0 0 0"


def test_compound_operations():
    assert x >> 3 & x << 5 == zeros
