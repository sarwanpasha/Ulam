"""Minimum working example: the reversal pair and the block family, checked from the
definition of a maximally separated constant-weight code."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from ulam import reversal_pair, block_family, is_max_separated_code

n, l = 7, 3
sigma, tau = reversal_pair(n, l)
print("reversal pair for n=%d, l=%d:" % (n, l), sigma, tau)
print("  is a maximally separated code:", is_max_separated_code([sigma, tau], l))

n, l = 10, 3
fam = block_family(n, l)
print("\nblock family for n=%d, l=%d (%d words):" % (n, l, len(fam)))
for w in fam:
    print("  ", w)
print("  is a maximally separated code:", is_max_separated_code(fam, l))

print("\nsweep: block family for l = 2..6 and n = 3l..40")
for l in range(2, 7):
    for n in range(3 * l, 41):
        ok, msg = is_max_separated_code(block_family(n, l), l)
        assert ok, (n, l, msg)
print("  all pass")
