from bit_algebra import Bit
from hypothesis import given
from hypothesis.strategies import booleans, characters, sampled_from


t = Bit(1)
f = Bit(0)
x, y, z, w = [Bit(v) for v in "xyzw"]

standard_samples = sampled_from([0, 1, "a", "b"])


@given(standard_samples)
def test_identity_function(b):
    assert Bit(b) == Bit(b)


@given(a=standard_samples, b=standard_samples)
def test_boolean_equality(a, b):
    assert (a == b) == (Bit(a) == Bit(b))


@given(c=characters(), b=booleans())
def test_known_ne_unknown(c, b):
    assert Bit(c) != Bit(b)


@given(standard_samples)
def test_boolean_not_on_known(b):
    B = Bit(b)
    assert B != ~B
    assert B == ~~B
    assert repr(B) == repr(~~B)


@given(a=booleans(), b=booleans())
def test_and_with_known(a, b):
    assert Bit(a & b) == Bit(a) & Bit(b)


@given(b=booleans(), c=standard_samples)
def test_and_with_known_and_unknown(b, c):
    assert Bit(b) & Bit(c) == Bit(c) if b else Bit(0)
    assert Bit(c) & Bit(b) == Bit(c) if b else Bit(0)


def test_and_symbolic():
    assert str(x & y) == "x&y"
    assert x & y == y & x


def test_and_symbolic_simplifies():
    assert x & x == x
    assert (x & y) & (y & x) == x & y
    assert str(x & x) == "x"
    assert x & y & x == x & y
    assert x & y & (z & y) & x == x & y & z


def test_and_not_simplifies():
    assert x & ~x == f
    assert ~x & x == f
    assert ~x & ~x == ~x
    assert ~(x & y) & (y & x) == f
    assert (x & y) & ~(y & x) == f


@given(a=booleans(), b=booleans())
def test_xor_with_known(a, b):
    assert Bit(a ^ b) == Bit(a) ^ Bit(b)


@given(b=booleans(), c=standard_samples)
def test_xor_with_known_and_unknown(b, c):
    assert Bit(b) ^ Bit(c) == ~Bit(c) if b else Bit(c)
    assert Bit(c) ^ Bit(b) == ~Bit(c) if b else Bit(c)


def test_xor_symbolic_simplifies():
    assert x ^ x == f
    assert x ^ ~x == t
    assert ~x ^ x == t
    assert ~x ^ ~x == f
    assert (x & y) ^ (y & x) == f
    assert (x & y) ^ (~x & ~y) == ~(x ^ y)
    assert (x ^ y) ^ (x ^ y) == f
    assert (x ^ y) ^ ~(x & y) == ~x & ~y


def test_operand_commutativity():
    assert ~(x & y) == ~x | ~y
    assert ~(x ^ y) == t ^ x ^ y
    assert z & (x ^ y) == z & x ^ z & y


def test_operand_associativity():
    assert z & (x & y) == (x & y) & z
    assert z ^ (x & y) == (x & y) ^ z
    assert z ^ (x ^ y) == (z ^ x) ^ y


@given(a=booleans(), b=booleans())
def test_or_with_known(a, b):
    assert Bit(a | b) == Bit(a) | Bit(b)


@given(b=booleans(), c=standard_samples)
def test_or_with_known_and_unknown(b, c):
    assert Bit(b) | Bit(c) == Bit(1) if b else Bit(c)
    assert Bit(c) | Bit(b) == Bit(1) if b else Bit(c)


def test_or_symbolic_simplifies():
    assert x | x == x
    assert x | ~x == t
    assert ~x | x == t
    assert ~x | ~x == ~x
    assert ~x | ~y == ~(x & y)
    assert x | (y & z) == (x | y) & (x | z)
    assert (x & y) | (z & x) == (z | x & y) & (x & (y | x))
