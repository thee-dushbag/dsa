import typing as ty, heapq as _hq

__all__ = (
    "bubble_sort",
    "selection_sort",
    "insertion_sort",
    "insertion_sort_bst",
    "quick_sort",
)


def _identity(item):
    return item


def bubble_sort(array: ty.MutableSequence, *, key=None):
    key = _identity if key is None else key
    size = len(array)
    for i in range(size):
        for j in range(size):
            if key(array[i]) < key(array[j]):
                array[j], array[i] = array[i], array[j]


def _select_next(array, start, end, key):
    smallest = array[start]
    smallest_index = start
    while start < end:
        item = array[start]
        if key(item) < key(smallest):
            smallest_index = start
            smallest = item
        start += 1
    return smallest_index


def selection_sort(array: ty.MutableSequence, *, key=None):
    key = _identity if key is None else key
    start, size = 0, len(array)
    while start < size:
        index = _select_next(array, start, size, key)
        array.insert(start, array.pop(index))
        start += 1


def _insert_item(array, stop, key):
    index, item = 0, array[stop]
    while index <= stop:
        sitem = array[index]
        if key(sitem) >= key(item):
            break
        index += 1
    return index


def _insert_item_bst(array, stop, key):
    item = key(array[stop])
    low, high = 0, stop
    while True:
        mid = int((high + low) / 2)
        current = key(array[mid])
        if (high - low) <= 1:
            return high if current < item else low
        elif current == item:
            return mid
        elif current < item:
            low = mid
        else:
            high = mid


def _insertion_sort_impl(array, key, insertindex):
    insertindex = _insert_item if insertindex is None else insertindex
    key = _identity if key is None else key
    start, size = 1, len(array)
    while start < size:
        index = insertindex(array, start, key)
        array.insert(index, array.pop(start))
        start += 1


def insertion_sort(array: ty.MutableSequence, *, key=None):
    _insertion_sort_impl(array, key=key, insertindex=_insert_item)


def insertion_sort_bst(array: ty.MutableSequence, *, key=None):
    _insertion_sort_impl(array, key=key, insertindex=_insert_item_bst)


def _partition_by(array: list, item, key):
    low, high, middle = [], [], []
    while array:
        current = key(array.pop())
        if current < item:
            low.append(current)
        elif current > item:
            high.append(current)
        else:
            middle.append(current)
    return low, middle, high


def _quick_sort_impl(array: list, key=None):
    size = len(array)
    key = _identity if key is None else key
    if size <= 1:
        if size == 2:
            if key(array[0]) > key(array[1]):
                array[0], array[1] = array[1], array[0]
        return array
    mid_item = key(array[int(size / 2)])
    low, middle, high = _partition_by(array, mid_item, key)
    return _quick_sort_impl(low) + middle + _quick_sort_impl(high)


def quick_sort(array: list, *, key=None):
    array[:] = _quick_sort_impl(array, key=key)


class _RichCmp:
    def __init__(self, item, key) -> None:
        self._item = item
        self._key = key

    def __eq__(self, other):
        return self._key == other._key

    def __lt__(self, other):
        return self._key < other._key


def _heap_sort(heap: list):
    _hq.heapify(heap)
    while heap:
        yield _hq.heappop(heap)


def heap_sort(array: list, *, key=None):
    key = _identity if key is None else key
    heap = [_RichCmp(i, key(i)) for i in array]
    array[:] = (r._item for r in _heap_sort(heap))
