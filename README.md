# Ulam: constant-weight codes and tree embeddings in the Ulam metric

Companion code for the paper *Constant-weight codes and tree embeddings in the Ulam
metric*. Pure Python 3 (3.9 or later), no dependencies.

The Ulam distance between two permutations of `[n] = {1, ..., n}` is
`d_U(s, t) = 2 (n - LCS(s, t))`, where `LCS` is the length of a longest common
subsequence. The code computes this distance, verifies the two explicit code families
and the spider embedding of the paper, computes the capacity `T(n, l)` exactly by
exhaustive search, and computes the symbol cost `n*(T)` of a tree `T`, the least `n`
such that `T` embeds isometrically (with all distances doubled) into `(S_n, d_U)`.

## Layout

| Path | Contents |
| --- | --- |
| `ulam/core.py` | `lcs`, `lis`, `ulam`, `weight`, `defects`, `disagreement_graph`, `reverse_complement`, `single_moves` |
| `ulam/constructions.py` | `reversal_pair`, `block_family`, `is_max_separated_code`, `spider_embedding`, `verify_spider_embedding` |
| `ulam/capacity.py` | `exact_capacity(n, l)`: exhaustive search for `T(n, l)` |
| `ulam/trees.py` | free-tree enumeration with a canonical form, distances, double spiders `DS_uv`, spiders `S(d, l)` |
| `ulam/embed.py` | Procedure A (`embed_A`), Procedure B (`embed_B`), `n_star`, `edge_bound`, `lower_bound`, `verify_embedding` |
| `examples/` | six short, self-contained scripts (see below) |
| `scripts/census.py` | the exhaustive sweep over all free trees with a given number of vertices |
| `tests/test_basic.py` | checks that reproduce the small claims of the paper |

## Quick start

```bash
git clone https://github.com/sarwanpasha/Ulam.git
cd Ulam
python examples/01_distances.py
python tests/test_basic.py          # or: python -m pytest tests
```

```python
from ulam import lcs, ulam, block_family, is_max_separated_code, exact_capacity, make_tree, n_star, edge_bound

ulam((3, 1, 2, 5, 4), (1, 2, 3, 4, 5))          # 4
fam = block_family(10, 3)                        # 3 permutations of [10] of weight 3
is_max_separated_code(fam, 3)                    # (True, 'ok')
exact_capacity(8, 2)                             # 4  (= floor(8/2))
TA = make_tree([(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6), (0, 7)])
edge_bound(TA), n_star(TA)                       # (6, 7): the edge-local bound is strict
```

## Examples

| Script | What it shows | Time |
| --- | --- | --- |
| `examples/01_distances.py` | distance, weight, defects, disagreement graph | instant |
| `examples/02_capacity.py` | Table 1 of the paper: `T(n, l)` for `l = 1..4` | seconds |
| `examples/03_constructions.py` | reversal pair and block family, checked from the definition | seconds |
| `examples/04_spider.py` | the embedding of `S(d, l)` into `S_{ld}`, checked pairwise | seconds |
| `examples/05_tree_symbol_cost.py` | the two trees on 8 vertices with `n* = 7` and edge bound 6 | about 2 minutes |
| `examples/06_small_census.py` | `n*` and the edge bound for every tree with at most 6 vertices | seconds |

## Reproducing the computational results of the paper

* **Table 1 (exact capacities).** `python examples/02_capacity.py`.
* **Constructions.** `examples/03_constructions.py` and `examples/04_spider.py` run
  reduced sweeps; the full ranges of the paper are obtained by changing the loop bounds
  (`l = 2..25`, `n = 3l..300` for the block family; `l = 2..12`, `d = 3..14` for the
  spider).
* **Theorem 1.3 (the trees on 8 vertices).** `python examples/05_tree_symbol_cost.py`.
  Both search procedures report no embedding into `S_6`, and Procedure A returns and
  verifies an embedding into `S_7`.
* **Exhaustive sweep (Table 2).** `python scripts/census.py 7` covers the 23 trees with
  at most 7 vertices in well under a minute; `python scripts/census.py 8 --only 8` covers
  the 23 trees with 8 vertices in some minutes. Trees with 9 vertices take minutes to
  hours each in pure Python and were run one tree per core on a compute cluster;
  `--procedure B` runs the independent second solver.

## How the searches work

* `exact_capacity` uses the fact that two codewords of a maximally separated code have
  disjoint defects (Proposition 2.6 of the paper): it enumerates systems of pairwise
  disjoint `l`-subsets of `[n]`, picks one candidate word per subset, and stops as soon as
  `floor(n/l)` codewords are found.
* `embed_A` sends one vertex to the identity, places the other vertices in breadth-first
  order, generates the candidates of a vertex from the image of its parent by the
  `n(n-1)` single-value moves, checks every candidate against all placed vertices, uses
  forward checking, and halves the search with the reverse-complement symmetry.
* `embed_B` uses whole LIS levels as candidate sets, a table of pairwise LCS values, an
  ordering of the vertices by candidate count, and plain backtracking; it shares no
  pruning rule with `embed_A`.
* `n_star` starts the search at the largest of three lower bounds (diameter, maximum
  degree, symbol cost of the proper double spiders) and increases `n` until an embedding
  is found. Every embedding returned is re-verified from the definition.

## License

MIT, see `LICENSE`.
