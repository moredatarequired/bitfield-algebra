# Bitfield Algebra
Symbolic algebra over bitfields

This isn't a fully built out system; it's just a toy I developed to help me
with some cryptoanalysis when I found myself making too many mistakes while
working things out on paper.

In particular, the idea is to have an operation, such as `y ^= (y << 15) & MASK`,
and be able to examine the result symbolically, i.e.

```python3
y, m = BitVector("y", 8), BitVector("m", 8)

print(y ^ ((y << 3) & m))
```
Prints `y0^y3&m0 y1^y4&m1 y2^y5&m2 y3^y6&m3 y4^y7&m4 y5^y8&m5 y6^y9&m6 y7^y10&m7`

This is mostly helpful when examining which operations cancel or simplify,
e.g. `x^x == 0`, `x&x == x`, and simplifying those operations. Continuing the
example from above,

```python3
z = (y ^ y << 3 & m)
z ^= z << 3 & m
print(z)
```

Now we can see that we've recovered come the original bits of `y`, but mucked up
the high order bits. By playing with these strings we can reason a little about
how all these operations go together.



