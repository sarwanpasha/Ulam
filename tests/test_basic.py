"""Run with:  python -m pytest tests   (or simply  python tests/test_basic.py)"""
import os, random, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from ulam import *
from ulam.core import lcs_check_bruteforce, single_moves


def test_lcs_against_bruteforce():
    random.seed(1)
    for _ in range(300):
        n = random.randint(2, 7)
        a = list(range(1, n + 1)); b = a[:]
        random.shuffle(a); random.shuffle(b)
        assert lcs(a, b) == lcs_check_bruteforce(a, b)


def test_single_moves_are_distance_two():
    p = (2, 4, 1, 3, 5)
    for q in single_moves(p):
        assert ulam(p, q) == 2
    assert len(single_moves(p)) > 0


def test_reverse_complement():
    for p in [(1, 2, 3, 4), (2, 4, 1, 3), (4, 3, 2, 1, 5)]:
        q = (1, 3, 2, 4) if len(p) == 4 else (3, 1, 2, 4, 5)
        assert reverse_complement(identity(len(p))) == identity(len(p))
        assert lcs(reverse_complement(p), reverse_complement(q)) == lcs(p, q)


def test_constructions():
    for l in range(2, 6):
        for n in range(3 * l, 25):
            assert is_max_separated_code(block_family(n, l), l)[0]
    for l in range(1, 5):
        for n in range(2 * l + 1, 20):
            assert is_max_separated_code(list(reversal_pair(n, l)), l)[0]
    for l in range(2, 4):
        for d in range(3, 6):
            assert verify_spider_embedding(d, l)[0]


def test_capacity_table():
    assert [exact_capacity(n, 1) for n in (2, 3, 4, 5)] == [1, 2, 4, 5]
    assert [exact_capacity(n, 2) for n in (4, 5, 6, 7, 8)] == [1, 2, 3, 3, 4]
    assert [exact_capacity(n, 3) for n in (6, 7, 8)] == [1, 2, 2]


def test_tree_counts():
    assert [len(free_trees(k)) for k in range(1, 10)] == [1, 1, 1, 2, 3, 6, 11, 23, 47]


def test_small_trees_tight():
    for k in range(3, 7):
        for T in free_trees(k):
            assert n_star(T) == edge_bound(T)


def test_counterexample_TA():
    TA = make_tree([(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6), (0, 7)])
    assert edge_bound(TA) == 6
    assert embed_A(TA, 6) is None
    assert n_star(TA) == 7


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
