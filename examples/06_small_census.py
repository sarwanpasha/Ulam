"""Minimum working example: n*(T) and the edge-local bound for every tree with at most
6 vertices (runs in seconds).  See scripts/census.py for larger sizes."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from ulam import free_trees, n_star, edge_bound
from ulam.trees import edges_of

print("free trees with 1..9 vertices:", [len(free_trees(k)) for k in range(1, 10)])
for k in range(3, 7):
    for T in free_trees(k):
        print("k=%d  edges=%s  edge_bound=%d  n*=%d" % (k, edges_of(T), edge_bound(T), n_star(T)))
