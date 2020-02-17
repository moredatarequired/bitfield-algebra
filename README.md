# Bitfield Algebra

Symbolic algebra over bitfields

This isn't a fully built out system; it's just a toy I developed to help me
with some cryptoanalysis when I found myself making too many mistakes while
working things out on paper.

In particular, the idea is to have an operation, such as `y ^= (y << 3) & MASK`,
and be able to examine the result symbolically, for example:

```python3
y, m = BitVector.new("y"), BitVector.new("m")

print(y ^ ((y << 3) & m))
```

Prints `y0 y1 y2 m3&y0^y3 m4&y1^y4 m5&y2^y5 m6&y3^y6 m7&y4^y7`

This is mostly helpful when examining which operations cancel or simplify,
e.g. `x^x == 0`, `x&x == x`, and simplifying those operations. Continuing the
example from above,

```python3
z = (y ^ y << 3 & m)
print(z ^ z << 3 & m)
```

Prints `y0 y1 y2 y3 y4 y5 m3&m6&y0^y6 m4&m7&y1^y7`

Now we can see that we've recovered some the original bits of `y`, but mucked up
the high order bits. If we imagine we're trying to reverse the operation from
above, now we have an idea that we should mask out the three MSB of `z << 3 & m`
before the XOR; if we do that,

```python3
v = BitVector.from_value(0x1F, 8)  # First keep 5 bits for XORing.
z1 = z ^ (z << 3 & m & v)
w = BitVector.from_value(0xE0, 8)  # Then keep only 3.
print(z1 ^ z1 << 3 & m & w)
```

Prints `y0 y1 y2 y3 y4 y5 y6 y7`

And we've recovered the original bits of `y`! This isn't actually that hard to do
on paper, unless you're like me and make a lot of mistakes. But even if you do
it right all the time, this makes it a little faster and enables writing
code to automatically look for and find formulas to create certain operations.
