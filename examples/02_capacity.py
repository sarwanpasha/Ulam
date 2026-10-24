"""Minimum working example: exact capacity T(n, l) by exhaustive search (Table 1)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from ulam import exact_capacity

for l, ns in [(1, [2, 3, 4, 5]), (2, [4, 5, 6, 7, 8]), (3, [6, 7, 8]), (4, [8, 9, 10, 11])]:
    for n in ns:
        print("T(%2d, %d) = %d    floor(n/l) = %d" % (n, l, exact_capacity(n, l), n // l))

size, code = exact_capacity(8, 2, return_code=True)
print("\nA maximally separated constant-weight-2 code in S_8 of size", size)
for w in code:
    print("  ", w)
