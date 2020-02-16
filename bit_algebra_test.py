from bit_algebra import Bit


t = Bit(1)
f = Bit(0)
x, y, z, w = [Bit(v) for v in "xyzw"]


def test_bits_one_equals_one():
    assert t == Bit(1)


def test_bits_zero_equals_zero():
    assert f == Bit(0)


def test_bits_zero_ne_one():
    assert Bit(0) != Bit(1)
    assert Bit(1) != Bit(0)


def test_same_names_equal():
    assert x == Bit("x")


def test_different_names_not_equal():
    assert x != y


def test_not_inverts_bits():
    assert t == ~f
    assert ~t == f
    assert t == ~~t
    assert repr(~~t) == repr(t)
    assert ~t != ~f


def test_and1_simplifies():
    assert t & f == f
    assert f & t == f
    assert t & t == t
    assert t & x == x
    assert x & t == x


def test_and0_simplifies():
    assert f & f == f
    assert f & x == f
    assert x & f == f


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
    assert ~(x & y) & (y & x) == f
    assert (x & y) & ~(y & x) == f


def test_xor_zero_simplifies():
    assert t ^ f == t
    assert f ^ t == t
    assert f ^ f == f
    assert x ^ f == x
    assert f ^ x == x


def test_xor_one_inverts():
    assert t ^ t == f
    assert x ^ t == ~x
    assert t ^ x == ~x


def test_xor_symbolic_simplifies():
    assert x ^ x == f
    assert x ^ ~x == t
    assert ~x ^ x == t
    assert (x & y) ^ (y & x) == f
    assert (x & y) ^ (~x & ~y) == ~(x ^ y)
