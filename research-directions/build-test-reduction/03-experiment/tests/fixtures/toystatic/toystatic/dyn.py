from . import targets


def dispatch(name):
    return getattr(targets, name)()
