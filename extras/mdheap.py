import typing

__all__ = "heapify", "heappush", "heappop", "DHeap"


class _LessThan(typing.Protocol):
    def __lt__(self, other, /) -> bool: ...


def _findmin[T: _LessThan](items: list[T], indices: range) -> int:
    """
    Find the smallest item in a sublist of D items.
    Returns the index of the smallest item in the list
    Takes `O(D)` regardless of size of list.
    """
    minindex: int = indices.start
    try:
        for index in indices:
            if items[index] < items[minindex]:
                minindex = index
    except IndexError:
        ...
    return minindex


def _siftup[T: _LessThan](dheap: list[T], current_index: int, D: int):
    """
    Bubble an element up till it's greater
    than its parent.
    Takes `O(logD(n))`, n being the size of the heap
    and D, the branching factor.
    """
    current = dheap[current_index]
    while current_index > 0:
        parent_index = (current_index - 1) // D
        if current < dheap[parent_index]:
            dheap[current_index] = dheap[parent_index]
            current_index = parent_index
        else:
            break
    dheap[current_index] = current


def _children(parent_index: int, D: int):
    """
    Get the indices of the children of the parent
    item at index `parent_index`, the children may
    not exist; raise an error if accessed.
    """
    parent_index = parent_index * D
    return range(parent_index + 1, parent_index + D + 1)


def _siftdown[T: _LessThan](dheap: list[T], current_index: int, D: int):
    """
    Push an element down from `current_index`.
    Takes `O(D*logD(n))`, n being the size of the heap
    and D the branching factor of the heap.
    """
    current = dheap[current_index]
    last_parent: int = (len(dheap) - 2) // D
    while current_index <= last_parent:
        child_index = _findmin(dheap, _children(current_index, D))
        if dheap[child_index] < current:
            dheap[current_index] = dheap[child_index]
            current_index = child_index
        else:
            break
    dheap[current_index] = current


def heapify[T: _LessThan](dheap: list[T], D: int):
    """
    Heapify a list into a heap with branching factor D.
    Takes `O(n)`, funny story; a bit complicated
    to calculate an conclude to this but it is true.
    """
    for index in range((len(dheap) - 1) // D, -1, -1):
        _siftdown(dheap, index, D)


def heappush[T: _LessThan](dheap: list[T], item: T, D: int):
    """
    Add an element in a dheap of branching factor D.
    Takes `O(logD(n))`, mainly because it is
    an insertion and bubbling.
    """
    index = len(dheap)
    dheap.append(item)
    _siftup(dheap, index, D)


def heappop[T: _LessThan](dheap: list[T], D: int) -> T:
    """
    Remove the most minimum element from the dheap.
    Takes `O(D*logD(n))`, main operation is siftdown.
    """
    replacement: T = dheap.pop()
    if not dheap:
        return replacement
    target, dheap[0] = dheap[0], replacement
    _siftdown(dheap, 0, D)
    return target


class DHeap[T: _LessThan]:
    __slots__ = ("_D",)

    def __init__(self, D: int, /) -> None:
        assert isinstance(D, int) and D > 0, (
            "Expected a positive integer greater than 0: %r" % D
        )
        self._D: typing.Final[int] = D

    @property
    def branching_factor(self) -> int:
        return self._D

    def heapify(self, dheap: list[T]):
        return heapify(dheap, self._D)

    def heappush(self, dheap: list[T], item: T):
        return heappush(dheap, item, self._D)

    def heappop(self, dheap: list[T]) -> T:
        return heappop(dheap, self._D)

    # Shortcuts
    fy = heapify
    pop = heappop
    push = heappush
    D = branching_factor
