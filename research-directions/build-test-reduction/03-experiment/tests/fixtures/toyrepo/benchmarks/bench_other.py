import toylib


class TimeAcc:
    def time_push(self):
        toylib.Acc().push(1)

    def time_boom(self):
        raise RuntimeError("boom")
