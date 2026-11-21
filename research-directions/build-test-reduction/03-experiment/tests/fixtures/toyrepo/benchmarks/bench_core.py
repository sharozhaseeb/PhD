import toylib


class TimeTotal:
    params = [10, 100]
    param_names = ["n"]
    timeout = 30

    def setup(self, n):
        self.n = n

    def time_total(self, n):
        toylib.total(n)

    def teardown(self, n):
        self.n = None

    def track_size(self, n):
        return n

    def peakmem_total(self, n):
        toylib.total(n)

    def helper(self):
        pass


class TimeGrid:
    params = ([1, 2], ["a", "b"])
    param_names = ["i", "s"]

    def time_pair(self, i, s):
        toylib.add(i, i)


class TimeSkip:
    def setup(self):
        raise NotImplementedError

    def time_never(self):
        pass


def time_add():
    toylib.add(1, 2)


def time_k(k):
    toylib.total(k)


time_k.params = [3, 4]
time_k.timeout = 5
