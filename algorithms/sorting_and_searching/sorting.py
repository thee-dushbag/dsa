import typing as ty


def identity(item):
    return item


def bubble_sort(array: ty.MutableSequence, *, key=None):
    key = identity if key is None else key
    size = len(array)
    for i in range(size):
        for j in range(size):
            if key(array[i]) < key(array[j]):
                array[j], array[i] = array[i], array[j]
