from bit_algebra import Bit


def test_bits_one_equals_one():
    assert Bit(1) == Bit(1)


def test_bits_zero_equals_zero():
    assert Bit(0) == Bit(0)


def test_bits_zero_ne_one():
    assert Bit(0) != Bit(1)
    assert Bit(1) != Bit(0)


def test_same_names_equal():
    assert Bit("x") == Bit("x")


def test_different_names_not_equal():
    assert Bit("x") != Bit("y")


def test_not_inverts_bits():
    t, f = Bit(1), Bit(0)
    assert t == ~f
    assert ~t == f
    assert t == ~~t
    assert repr(~~t) == repr(t)
    assert ~t != ~f


def test_and1_simplifies():
    t, f, x = Bit(1), Bit(0), Bit("x")
    assert t & f == f
    assert f & t == f
    assert t & t == t
    assert t & x == x
    assert x & t == x


def test_and0_simplifies():
    f, x = Bit(0), Bit("x")
    assert f & f == f
    assert f & x == f
    assert x & f == f


def test_and_symbolic():
    x, y = Bit("x"), Bit("y")
    assert str(x & y) == "x&y"
    assert x & y == y & x


def test_and_symbolic_simplifies():
    x, y = Bit("x"), Bit("y")
    assert x & x == x
    assert str(x & x) == "x"
    assert x & y & x == x & y

