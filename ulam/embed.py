"""Exact symbol cost n*(T) of a tree T: the least n such that T embeds isometrically,
with all distances doubled, into (S_n, d_U).

Two independent search procedures are provided (Section 5.1 of the paper).

Procedure A  places the vertices in breadth-first order from a root sent to the
             identity, generates the candidates of a vertex from the image of its
             parent by single-value moves, tests each candidate against every placed
             vertex, uses forward checking, and halves the search with the
             reverse-complement symmetry (Lemma 5.1).
Procedure B  takes as candidates of a vertex at depth t the whole level
             {sigma : LIS(sigma) = n - t}, uses a table of pairwise LCS values on S_n,
             orders the vertices by increasing candidate count, and backtracks.

Both return an embedding (a dict vertex -> permutation) or None.  Every embedding
returned is re-verified from the definition by verify_embedding().
"""

from functools import lru_cache
from itertools import permutations

from .core import lcs, lis, identity, single_moves, reverse_complement
from .trees import (all_distances, bfs_distances, diameter, max_degree, edges_of,
                    double_spider, canonical_form)


@lru_cache(maxsize=None)
def _lcs(a, b):
    if a > b:
        a, b = b, a
    return lcs(a, b)


def verify_embedding(tree, phi):
    """Recompute all pairwise Ulam distances and compare with twice the tree distance."""
    dist = all_distances(tree)
    n = len(next(iter(phi.values())))
    verts = list(tree)
    for i, u in enumerate(verts):
        for v in verts[i + 1:]:
            if 2 * (n - lcs(phi[u], phi[v])) != 2 * dist[u][v]:
                return False
    return True


# ---------------------------------------------------------------------------
# Procedure A
# ---------------------------------------------------------------------------

def embed_A(tree, n, root=0, symmetry=True, forward_check=True):
    """Return an isometric embedding of tree into S_n with root sent to the identity,
    or None if there is none."""
    dist = all_distances(tree)
    order = sorted(tree, key=lambda v: (dist[root][v], v))
    parent = {}
    for v in order[1:]:
        parent[v] = min((u for u in tree[v] if dist[root][u] < dist[root][v]))
    placed = {root: identity(n)}
    first_child = order[1] if len(order) > 1 else None

    def candidates(v):
        base = placed[parent[v]]
        out = []
        for q in single_moves(base):
            if symmetry and v == first_child and q > reverse_complement(q):
                continue
            ok = True
            for u, pu in placed.items():
                if _lcs(q, pu) != n - dist[u][v]:
                    ok = False
                    break
            if ok:
                out.append(q)
        return out

    def rec(i):
        if i == len(order):
            return True
        v = order[i]
        for q in candidates(v):
            placed[v] = q
            good = True
            if forward_check:
                for w in order[i + 1:]:
                    if parent[w] in placed and w not in placed:
                        if not candidates(w):
                            good = False
                            break
            if good and rec(i + 1):
                return True
            del placed[v]
        return False

    if rec(1):
        phi = dict(placed)
        assert verify_embedding(tree, phi)
        return phi
    return None


# ---------------------------------------------------------------------------
# Procedure B
# ---------------------------------------------------------------------------

_level_cache = {}


def levels(n):
    """levels(n)[t] is the list of permutations of [n] with LIS = n - t."""
    if n not in _level_cache:
        lv = {}
        for p in permutations(range(1, n + 1)):
            lv.setdefault(n - lis(p), []).append(p)
        _level_cache[n] = lv
    return _level_cache[n]


def lcs_table(n):
    """Full table of pairwise LCS values on S_n (dict keyed by ordered pairs a <= b).
    Only practical for n <= 6; for larger n the lookups fall back to the cache."""
    table = {}
    perms = list(permutations(range(1, n + 1)))
    for i, a in enumerate(perms):
        for b in perms[i:]:
            table[(a, b)] = lcs(a, b)
    return table


def embed_B(tree, n, root=0, precompute_table=None):
    """Return an isometric embedding of tree into S_n with root sent to the identity,
    or None.  Candidates are whole LIS levels; no forward checking and no symmetry
    reduction are used, so the procedure shares no pruning rule with embed_A."""
    dist = all_distances(tree)
    lv = levels(n)
    if precompute_table is None:
        precompute_table = n <= 6
    table = lcs_table(n) if precompute_table else None

    def look(a, b):
        if a > b:
            a, b = b, a
        if table is not None:
            return table[(a, b)]
        return _lcs(a, b)

    cand = {}
    for v in tree:
        if v == root:
            cand[v] = [identity(n)]
        else:
            cand[v] = lv.get(dist[root][v], [])
            if not cand[v]:
                return None
    order = sorted(tree, key=lambda v: (len(cand[v]), v))
    placed = {}

    def rec(i):
        if i == len(order):
            return True
        v = order[i]
        for q in cand[v]:
            ok = True
            for u, pu in placed.items():
                if look(q, pu) != n - dist[u][v]:
                    ok = False
                    break
            if ok:
                placed[v] = q
                if rec(i + 1):
                    return True
                del placed[v]
        return False

    if rec(0):
        phi = dict(placed)
        assert verify_embedding(tree, phi)
        return phi
    return None


# ---------------------------------------------------------------------------
# Symbol cost and the edge-local bound
# ---------------------------------------------------------------------------

_nstar_cache = {}


def lower_bound(tree, use_subtrees=True):
    """The three lower bounds of Section 5.1: diameter + 1, maximum degree (via
    T(n, 1) >= Delta, which needs n >= Delta and n >= 4 when Delta >= 3), and the
    symbol cost of every proper double spider."""
    lb = diameter(tree) + 1
    D = max_degree(tree)
    lb = max(lb, D if D < 3 else max(D, 4))
    if use_subtrees:
        for u, v in edges_of(tree):
            ds, verts = double_spider(tree, u, v)
            if len(verts) < len(tree):
                lb = max(lb, n_star(ds))
    return lb


def embeds(tree, n, procedure="A", root=0):
    if procedure == "A":
        return embed_A(tree, n, root=root)
    if procedure == "B":
        return embed_B(tree, n, root=root)
    raise ValueError("procedure must be 'A' or 'B'")


def n_star(tree, procedure="A", root=0, n_max=12, start=None):
    """The symbol cost n*(T).  The search starts at the largest lower bound (or at
    start) and increases n until an embedding is found."""
    key = (canonical_form(tree), procedure)
    if key in _nstar_cache:
        return _nstar_cache[key]
    n = lower_bound(tree) if start is None else start
    while n <= n_max:
        if embeds(tree, n, procedure=procedure, root=root) is not None:
            _nstar_cache[key] = n
            return n
        n += 1
    raise RuntimeError("no embedding found up to n = %d" % n_max)


def edge_bound(tree, procedure="A"):
    """Right-hand side of inequality (4): max over edges uv of n*(DS_uv)."""
    best = 0
    for u, v in edges_of(tree):
        ds, _ = double_spider(tree, u, v)
        best = max(best, n_star(ds, procedure=procedure))
    return best
