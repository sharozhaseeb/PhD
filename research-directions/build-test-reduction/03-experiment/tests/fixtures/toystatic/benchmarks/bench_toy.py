import toystatic
from toystatic import util


class TimeX:
    def setup(self):
        self.k = 1

    def time_foo(self):
        toystatic.foo()

    def time_run(self):
        util.Engine().run()

    def time_dyn(self):
        toystatic.dispatch("t1")

    def helper(self):
        toystatic.util.leaf()


def time_bar():
    from toystatic.b import bar

    bar()
