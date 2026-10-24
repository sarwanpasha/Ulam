"""Minimum working example: the isometric embedding of the spider S(d, l) into S_{ld}."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from ulam import spider_embedding, verify_spider_embedding, spider, n_star

d, l = 3, 2
phi = spider_embedding(d, l)
print("embedding of S(%d, %d) into S_%d:" % (d, l, d * l))
for v, p in phi.items():
    print("  ", v, "->", p)
print("  verified:", verify_spider_embedding(d, l))

print("\nsweep: l = 2..4, d = 3..6")
for l in range(2, 5):
    for d in range(3, 7):
        ok, msg = verify_spider_embedding(d, l)
        assert ok, (d, l, msg)
print("  all pass")

print("\nexact symbol cost of S(3, 2) by search:", n_star(spider(3, 2)), "(theorem: 6)")
