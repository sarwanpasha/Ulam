"""Minimum working example: symbol cost of a tree, the edge-local bound, and the two
trees on 8 vertices for which the bound is strict (Figure 2 of the paper)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from ulam import make_tree, n_star, edge_bound, embed_A, embed_B, verify_embedding

# T_A: spine u1 - u0 - u2, two leaves at u1, two leaves at u2, one leaf at u0
TA = make_tree([(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6), (0, 7)])
# T_B: spine w0 - w1 - w2, three leaves at w0, two leaves at w2
TB = make_tree([(0, 1), (1, 2), (0, 3), (0, 4), (0, 5), (2, 6), (2, 7)])

for name, T in [("T_A", TA), ("T_B", TB)]:
    print(name)
    print("  edge-local bound (4):", edge_bound(T))
    print("  Procedure A, embeds into S_6:", embed_A(T, 6) is not None)
    phi = embed_A(T, 7)
    print("  Procedure A, embeds into S_7:", phi is not None, " verified:", verify_embedding(T, phi))
    print("  n*(T) =", n_star(T))

# Procedure B is slower (whole LIS levels, no pruning) but shares no code path with A
print("\nProcedure B on T_A at n = 6 (takes about a minute):", embed_B(TA, 6))
