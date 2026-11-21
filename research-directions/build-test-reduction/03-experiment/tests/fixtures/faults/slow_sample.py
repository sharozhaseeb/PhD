"""Handcrafted sample for slowdown tests (do not reformat)."""
import functools

CALLS = []


def deco(fn):
    CALLS.append(fn.__name__)
    return fn


@deco
@functools.lru_cache(maxsize=None)
def plain(n):
    seen = set()
    out = []
    for k in range(n):
        if k in seen:
            continue
        seen.add(k)
        out.append(k)
    return out


def membership(xs, extra):
    s = set(xs)
    d = {1: 2}
    lst = [1, 2]
    c = {x for x in xs}
    hits = 0
    for x in xs:
        if x in s:
            hits += 1
        if x not in d:
            hits += 2
        if x in lst:
            hits += 4
        if x in extra:
            hits += 8
        if x in c:
            hits += 16
    return hits


def looped(n):
    items = [1, 2, 3]
    total = 0
    for v in items:
        total += v
    return total


def unbound_loop(pairs):
    for a, b in pairs:
        print(a, b)


def gen(n):
    for i in range(n):
        yield i


async def agen(n):
    return n


class Box:
    @property
    def size(self):
        return 3

    @staticmethod
    def helper(x):
        return x + 1

    def run(self, x):
        return self.helper(x)
