import typing as ty


__all__ = "binary_search", "simple_search"


def _identity(item):
    return item


def simple_search(array: ty.Sequence, item, *, key=None) -> None | int:
    key = _identity if key is None else key
    for index, itemc in enumerate(map(key, array)):
        if item == itemc: return index


def binary_search(sorted_array: ty.Sequence, item, *, key=None):
    key = _identity if key is None else key
    low, high, item = 0, len(sorted_array), key(item)
    while low < high:
        mid = int((high + low) / 2)
        itemc = key(sorted_array[mid])
        prev = low, high
        if itemc == item: return mid
        elif itemc > item: high = mid
        else: low = mid
        if prev == (low, high): break
