import pytest
import toylib


def test_add():
    assert toylib.add(1, 2) == 3


class TestAcc:
    @pytest.mark.parametrize("x", [1, 2])
    def test_push(self, x):
        assert toylib.Acc().push(x) == x


def test_bad():
    assert toylib.total(3) == 99
