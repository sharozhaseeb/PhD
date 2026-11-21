class Engine:
    def run(self):
        return self.step() + self.step()

    def step(self):
        return leaf()


def leaf():
    return 5


def make_and_run():
    e = Engine()
    return e.run()
