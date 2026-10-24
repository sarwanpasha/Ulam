"""Permutation codes and tree embeddings in the Ulam metric.

Companion code for the paper "Constant-weight codes and tree embeddings in the
Ulam metric".  Pure Python, no dependencies.
"""

from .core import lcs, lis, ulam, weight, defects, disagreement_graph, reverse_complement, identity
from .constructions import (reversal_pair, block_family, is_max_separated_code,
                            spider_embedding, verify_spider_embedding)
from .capacity import exact_capacity
from .trees import make_tree, free_trees, spider, double_spider, diameter, max_degree
from .embed import embed_A, embed_B, n_star, edge_bound, lower_bound, verify_embedding

__all__ = [
    "lcs", "lis", "ulam", "weight", "defects", "disagreement_graph", "reverse_complement",
    "identity", "reversal_pair", "block_family", "is_max_separated_code",
    "spider_embedding", "verify_spider_embedding", "exact_capacity", "make_tree",
    "free_trees", "spider", "double_spider", "diameter", "max_degree", "embed_A",
    "embed_B", "n_star", "edge_bound", "lower_bound", "verify_embedding",
]
