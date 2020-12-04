from collections import Iterable


# Convenience method to flatten a list, since doing that in python is a PITA. Credit @grym from #python on freenode.
def should_flatten(x):
    return isinstance(x, Iterable) and not isinstance(x, (str, bytes))


def flatten(x, should_flatten=should_flatten):
    for y in x:
        if should_flatten(y):
            yield from flatten(y, should_flatten=should_flatten)
        else:
            yield y
