"""Handcrafted sample for operator tests (do not reformat: tests pin line numbers)."""
import os


def target(a, b, items):
    total = 0
    if a < b and b >= 3:
        total = total + a
    elif a == b or a != 7:
        total = total - 2
    for i in items:
        total += i
    return total * 2


def other(x):
    return x < 5


class K:
    def method(self, n):
        if n > 0:
            return n - 1
        return None
