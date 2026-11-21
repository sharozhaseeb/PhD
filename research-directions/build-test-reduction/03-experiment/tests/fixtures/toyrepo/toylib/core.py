def add(a, b):
    return a + b


def total(n):
    return sum(i for i in range(n))


class Acc:
    def __init__(self):
        self.v = 0

    def push(self, x):
        self.v = add(self.v, x)
        return self.v
