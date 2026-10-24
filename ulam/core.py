"""Basic operations on permutations under the Ulam metric.

A permutation of [n] = {1, ..., n} is represented as a tuple of the values
1..n in one-line notation, for example (3, 1, 2).  All distances use the
scale-two normalization

    d_U(sigma, tau) = 2 * (n - LCS(sigma, tau)),

where LCS is the length of a longest common subsequence of the two words.
"""

from bisect import bisect_left
from itertools import combinations


def lis(seq):
    """Length of a longest strictly increasing subsequence (patience sorting, O(n log n))."""
    tails = []
    for x in seq:
        i = bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)


def lcs(a, b):
    """Length of a longest common subsequence of two permutations of the same set."""
    pos = {v: i for i, v in enumerate(b)}
    return lis([pos[v] for v in a])


def ulam(a, b):
    """Ulam distance 2 * (n - LCS(a, b))."""
    return 2 * (len(a) - lcs(a, b))


def identity(n):
    return tuple(range(1, n + 1))


def weight(p):
    """Weight n - LIS(p), that is, half the Ulam distance from the identity."""
    return len(p) - lis(p)


def is_increasing(seq):
    return all(seq[i] < seq[i + 1] for i in range(len(seq) - 1))


def defects(p):
    """All defects of p: sets D of size weight(p) whose deletion leaves p increasing."""
    w = weight(p)
    out = []
    for D in combinations(sorted(p), w):
        S = set(D)
        if is_increasing([v for v in p if v not in S]):
            out.append(D)
    return out


def disagreement_graph(a, b):
    """Edge set of the graph on the values in which {x, y} is an edge when x and y
    appear in different relative orders in a and in b.  By Lemma 2.3 of the paper,
    LCS(a, b) is the independence number of this graph."""
    pa = {v: i for i, v in enumerate(a)}
    pb = {v: i for i, v in enumerate(b)}
    vals = sorted(a)
    edges = set()
    for x, y in combinations(vals, 2):
        if (pa[x] < pa[y]) != (pb[x] < pb[y]):
            edges.add((x, y))
    return edges


def reverse_complement(p):
    """r(p)_k = n + 1 - p_{n+1-k}.  Fixes the identity and preserves LCS (Lemma 5.1)."""
    n = len(p)
    return tuple(n + 1 - v for v in reversed(p))


def single_moves(p):
    """All permutations obtained from p by relocating one value to another position.
    These are exactly the permutations at Ulam distance 2 from p."""
    n = len(p)
    out = set()
    lst = list(p)
    for i in range(n):
        v = lst[i]
        rest = lst[:i] + lst[i + 1:]
        for j in range(n):
            if j == i:
                continue
            q = rest[:j] + [v] + rest[j:]
            out.add(tuple(q))
    out.discard(p)
    return out


def lcs_check_bruteforce(a, b):
    """LCS by exhaustive enumeration of subsets; for testing only (small n)."""
    n = len(a)
    pa = {v: i for i, v in enumerate(a)}
    pb = {v: i for i, v in enumerate(b)}
    best = 0
    vals = sorted(a)
    for k in range(n, 0, -1):
        for S in combinations(vals, k):
            sa = sorted(S, key=lambda v: pa[v])
            sb = sorted(S, key=lambda v: pb[v])
            if sa == sb:
                return k
    return best
