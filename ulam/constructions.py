"""The two explicit code families and the spider embedding from the paper.

* reversal_pair(n, l): two permutations of weight l at LCS = n - 2l  (Theorem 3.6)
* block_family(n, l):  floor(n/l) permutations of weight l, pairwise LCS = n - 2l,
                       valid for l >= 2 and n >= 3l                      (Theorem 3.7)
* spider_embedding(d, l): isometric embedding of the spider S(d, l) into S_{ld}
                       (Theorem 1.2)
"""

from itertools import combinations

from .core import lcs, lis, ulam, identity


def reversal_pair(n, l):
    """Definition 3.1: sigma reverses the prefix 1..l+1, tau moves the l largest values
    to the front in decreasing order.  Requires n >= 2l + 1."""
    if n < 2 * l + 1:
        raise ValueError("reversal pair needs n >= 2l + 1")
    sigma = tuple(range(l + 1, 0, -1)) + tuple(range(l + 2, n + 1))
    tau = tuple(range(n, n - l, -1)) + tuple(range(1, n - l + 1))
    return sigma, tau


def block_family(n, l):
    """Definition 3.2.  Returns the list t_1, ..., t_m with m = floor(n / l).

    Block i consists of the l-1 consecutive small values
        L_i = {(l-1)(i-1)+1, ..., (l-1) i}
    and the cap c_i = (l-1) m + i.  The codeword t_i puts c_i first, then every value
    outside the block in increasing order, then L_i in decreasing order.
    """
    if l < 2:
        raise ValueError("block family needs l >= 2")
    m = n // l
    if m < 3:
        raise ValueError("block family needs floor(n/l) >= 3, that is n >= 3l")
    words = []
    for i in range(1, m + 1):
        L = list(range((l - 1) * (i - 1) + 1, (l - 1) * i + 1))
        c = (l - 1) * m + i
        B = set(L) | {c}
        middle = [v for v in range(1, n + 1) if v not in B]
        words.append(tuple([c] + middle + L[::-1]))
    return words


def is_max_separated_code(words, l):
    """Check Definition 2.1: every word has LIS = n - l and every pair has LCS = n - 2l.
    Returns (ok, message)."""
    n = len(words[0])
    for w in words:
        if lis(w) != n - l:
            return False, "word %s has weight %d, expected %d" % (w, n - lis(w), l)
    for a, b in combinations(words, 2):
        if lcs(a, b) != n - 2 * l:
            return False, "pair %s, %s has LCS %d, expected %d" % (a, b, lcs(a, b), n - 2 * l)
    return True, "ok"


def spider_vertices(d, l):
    """Vertices of S(d, l): 'c' for the center and (i, t) for depth t on leg i."""
    return ["c"] + [(i, t) for i in range(1, d + 1) for t in range(1, l + 1)]


def spider_distance(u, v):
    """Path distance in S(d, l) between two vertices in the labelling above."""
    if u == v:
        return 0
    if u == "c":
        return v[1]
    if v == "c":
        return u[1]
    if u[0] == v[0]:
        return abs(u[1] - v[1])
    return u[1] + v[1]


def spider_embedding(d, l):
    """Equation (11) of the paper: an isometric embedding of S(d, l) into S_{ld}.

    With n = ld the block family has exactly d blocks covering [n].  Order block i as
    c_i, a_{i,1}, ..., a_{i,l-1} and let D_{i,t} be its first t entries.  The vertex at
    depth t on leg i is mapped to (c_i, [n] \\ D_{i,t} increasing, D_{i,t} \\ {c_i} decreasing)
    and the center to the identity.
    """
    if d < 3 or l < 2:
        raise ValueError("spider embedding is stated for d >= 3 and l >= 2")
    n = l * d
    m = d
    phi = {"c": identity(n)}
    for i in range(1, d + 1):
        c = (l - 1) * m + i
        a = list(range((l - 1) * (i - 1) + 1, (l - 1) * i + 1))
        order = [c] + a
        for t in range(1, l + 1):
            D = order[:t]
            S = set(D)
            middle = [v for v in range(1, n + 1) if v not in S]
            closing = sorted(D[1:], reverse=True)
            phi[(i, t)] = tuple([c] + middle + closing)
    return phi


def verify_spider_embedding(d, l):
    """Recompute all pairwise Ulam distances of the embedding and compare with twice the
    tree distance.  Returns (ok, message)."""
    phi = spider_embedding(d, l)
    verts = spider_vertices(d, l)
    for u, v in combinations(verts, 2):
        want = 2 * spider_distance(u, v)
        got = ulam(phi[u], phi[v])
        if want != got:
            return False, "vertices %s, %s: distance %d, expected %d" % (u, v, got, want)
    return True, "ok"
