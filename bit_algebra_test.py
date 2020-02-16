import unittest

from bit_algebra import Bit


class BitAlgebraTest(unittest.TestCase):
    def test_bits_one_equals_one(self):
        a, b = Bit(1), Bit(1)
        self.assertEqual(a, b)

    def test_bits_zero_equals_zero(self):
        a, b = Bit(0), Bit(0)
        self.assertEqual(a, b)

    def test_bits_zero_ne_one(self):
        a, b = Bit(0), Bit(1)
        self.assertNotEqual(a, b)

    def test_same_names_equal(self):
        a, b = Bit("x"), Bit("x")
        self.assertEqual(a, b)

    def test_different_names_not_equal(self):
        a, b = Bit("x"), Bit("y")
        self.assertNotEqual(a, b)

    def test_not_inverts_bits(self):
        x, y = Bit(0), Bit(1)
        self.assertEqual(x, ~y)
        self.assertEqual(~x, y)
        self.assertEqual(x.value, 0)
        self.assertEqual((~x).value, 1)


if __name__ == "__main__":
    unittest.main()


import unittest
