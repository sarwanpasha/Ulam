"""Exact computation of the capacity T(n, l) by exhaustive search.

T(n, l) is the largest size of a family of permutations of [n] with LIS = n - l
(weight l) and pairwise LCS = n - 2l.  Two members of such a family have disjoint
defects (proof of Proposition 2.6), so the search below is exhaustive: it runs over
systems of pairwise disjoint l-subsets of [n] and picks one codeword per subset.
"""

from itertools import combinations, combinations_with_replacement, permutations

from .core import lcs, lis


def words_with_defect(n, D):
    """All permutations of [n] of weight exactly |D| that become increasing when the
    values in D are deleted.  They are obtained by inserting the elements of D, in
    every order, into every choice of gaps of the increasing word on [n] \\ D."""
    l = len(D)
    rest = [v for v in range(1, n + 1) if v not in D]
    gaps = len(rest) + 1
    out = []
    for order in permutations(D):
        # choose a gap for each element; elements in the same gap keep the given order
        for slots in combinations_with_replacement(range(gaps), l):
            word = []
            k = 0
            for g in range(gaps):
                while k < l and slots[k] == g:
                    word.append(order[k])
                    k += 1
                if g < len(rest):
                    word.append(rest[g])
            w = tuple(word)
            if lis(w) == n - l:
                out.append(w)
    # heuristic order only (does not affect exhaustiveness): words with more
    # inversions first, since the extremal examples are reversal-like
    out.sort(key=lambda w: -sum(1 for i in range(n) for j in range(i + 1, n) if w[i] > w[j]))
    return out


def exact_capacity(n, l, want=None, return_code=False):
    """Exact value of T(n, l), together with a code attaining it if return_code is set.

    The search stops as soon as a code of size floor(n / l) is found, since no larger
    code exists (Proposition 2.6).  If want is given, the search instead stops as soon
    as a code of that size is found (useful to confirm a lower bound quickly).
    """
    target = n // l if want is None else want
    subsets = list(combinations(range(1, n + 1), l))
    cands = {}

    def candidates(D):
        # candidate words are generated on demand and cached
        if D not in cands:
            cands[D] = words_with_defect(n, D)
        return cands[D]

    need = n - 2 * l
    best = [0, []]

    def compatible(w, chosen):
        return all(lcs(w, c) == need for c in chosen)

    def rec(start, used, chosen):
        if len(chosen) > best[0]:
            best[0] = len(chosen)
            best[1] = list(chosen)
            if best[0] >= target:
                return True
        # bound: how many further disjoint subsets could still fit
        if len(chosen) + (n - len(used)) // l <= best[0]:
            return False
        for idx in range(start, len(subsets)):
            D = subsets[idx]
            if used & set(D):
                continue
            # any two codewords need LCS = n - 2l >= 1
            if chosen and need < 1:
                continue
            for w in candidates(D):
                if compatible(w, chosen):
                    chosen.append(w)
                    if rec(idx + 1, used | set(D), chosen):
                        return True
                    chosen.pop()
        return False

    rec(0, frozenset(), [])
    if return_code:
        return best[0], best[1]
    return best[0]
