import math

CONST = 1


def g():
    return 1


def f():
    return g()


def h():
    return 2


class Box:
    def __init__(self, v):
        self.v = v

    def size(self):
        return self.v


def outer():
    def inner():
        return 3

    return inner()


def root_of(x):
    return math.sqrt(x)
