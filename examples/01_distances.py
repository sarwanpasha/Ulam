"""Minimum working example: Ulam distance, weight, defects, disagreement graph."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from ulam import lcs, ulam, weight, defects, disagreement_graph, identity

a = (3, 1, 2, 5, 4)
b = (1, 2, 3, 4, 5)
print("LCS(a, b)          =", lcs(a, b))
print("d_U(a, b)          =", ulam(a, b))
print("weight(a)          =", weight(a))
print("defects of a       =", defects(a))
print("defects of 213     =", defects((2, 1, 3)))     # two defects: {1} and {2}
print("disagreement graph =", sorted(disagreement_graph(a, b)))
print("identity(5)        =", identity(5))
