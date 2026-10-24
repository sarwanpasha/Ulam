"""Exhaustive sweep over all free trees with a given number of vertices.

For every tree T the script computes the symbol cost n*(T) and the edge-local bound
max_uv n*(DS_uv) of inequality (4) in the paper, and reports where the bound is strict.

Usage:
    python scripts/census.py 7            # all trees with 3..7 vertices
    python scripts/census.py 8 --only 8   # only the 23 trees with 8 vertices
    python scripts/census.py 8 --procedure B

Trees with 9 vertices take minutes each in pure Python; 10 vertices is out of reach
without a cluster.  Output is one line per tree followed by a summary.
"""

import argparse
import sys
import time

sys.path.insert(0, __import__("os").path.join(__import__("os").path.dirname(__file__), ".."))

from ulam.trees import free_trees, canonical_form, diameter, max_degree, edges_of
from ulam.embed import n_star, edge_bound


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("kmax", type=int, help="largest number of vertices")
    ap.add_argument("--only", type=int, default=None, help="only this number of vertices")
    ap.add_argument("--procedure", default="A", choices=["A", "B"])
    args = ap.parse_args()

    sizes = [args.only] if args.only else list(range(3, args.kmax + 1))
    summary = {}
    for k in sizes:
        trees = free_trees(k)
        tight = strict = 0
        for T in trees:
            t0 = time.time()
            eb = edge_bound(T, procedure=args.procedure)
            ns = n_star(T, procedure=args.procedure)
            gap = ns - eb
            if gap == 0:
                tight += 1
            else:
                strict += 1
            print("k=%d  diam=%d  maxdeg=%d  edges=%s  edge_bound=%d  n*=%d  gap=%d  (%.1fs)"
                  % (k, diameter(T), max_degree(T), edges_of(T), eb, ns, gap, time.time() - t0),
                  flush=True)
        summary[k] = (len(trees), tight, strict)
    print()
    print("vertices  trees  bound tight  bound strict")
    for k, (m, t, s) in summary.items():
        print("%8d  %5d  %11d  %12d" % (k, m, t, s))


if __name__ == "__main__":
    main()
