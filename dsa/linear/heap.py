import typing as ty, enum

__all__ = "heapify", "HeapType", "heappush", "heappop", "setheaptype", "getheaptype"

_T = ty.TypeVar("_T")
_CompareF = ty.Callable[[_T, _T], bool]


# Hail MYPY, bloody bastard!!!
class _LTComparisson(ty.Protocol):
    def __lt__(self: ty.Self, value: ty.Any) -> bool:
        ...


class _GTComparisson(ty.Protocol):
    def __gt__(self: ty.Self, value: ty.Any) -> bool:
        ...


class _LEComparisson(ty.Protocol):
    def __le__(self: ty.Self, value: ty.Any) -> bool:
        ...


class _GEComparisson(ty.Protocol):
    def __ge__(self: ty.Self, value: ty.Any) -> bool:
        ...


_min_heap: _CompareF[_LTComparisson] = lambda head, child: head > child
_max_heap: _CompareF[_GTComparisson] = lambda head, child: head < child
_min_heap_eq: _CompareF[_GEComparisson] = lambda head, child: head >= child
_max_heap_eq: _CompareF[_LEComparisson] = lambda head, child: head <= child


class HeapType(enum.IntEnum):
    """
    Heap types:
    1. MIN
        This represents a min-heap as usual, such
        that, if two values are equal, they are not swapped.
        (ie the newest gets the higher index)
        This behaves like a queue, FIFO.
    2. MINEQ
        This represents a min-heap as usual, such
        that, if two values are equal, they are swapped.
        (ie the newest gets the lower index)
        Behaves like a stack, FILO.
    3. MAX
        This represents a max-heap as usual, such
        that, if two values are equal, they are not swapped.
        (ie the newest gets the higher index)
        This behaves like a queue, FIFO.
    4. MAXEQ
        This represents a max-heap as usual, such
        that, if two values are equal, they are swapped.
        (ie the newest gets the lower index)
        Behaves like a stack, FILO.
    """

    MIN = enum.auto()
    MAX = enum.auto()
    MINEQ = enum.auto()
    MAXEQ = enum.auto()


_cmp_heap_type_map: dict[HeapType, _CompareF] = {
    HeapType.MIN: _min_heap,
    HeapType.MAX: _max_heap,
    HeapType.MAXEQ: _max_heap_eq,
    HeapType.MINEQ: _min_heap_eq,
}

_default_heap_type: HeapType = HeapType.MIN


def setheaptype(heap_type: HeapType):
    """
    Set a global heap type to use by default
    for operations like heapify if the heap
    type is not spacified.
    """
    global _default_heap_type
    _default_heap_type = heap_type


def getheaptype() -> HeapType:
    """
    Get the default global heap type used
    by operations like heapify if the heap
    type was not specified on operation use.
    """
    return _default_heap_type


def heapify(heap: ty.MutableSequence, heap_type: ty.Optional[HeapType] = None) -> None:
    """
    Convert a mutable sequence (eg list) to a heap
    (MIN-HEAP default or specify using param heap_type)
    """
    comparer, size = _cmp_heap_type_map[heap_type or _default_heap_type], len(heap)
    for index in reversed(range(size // 2)):
        _siftdown(heap, comparer, index, size)


def heappush(
    heap: ty.MutableSequence[_T], value: _T, heap_type: ty.Optional[HeapType] = None
) -> None:
    comparer, index = _cmp_heap_type_map[heap_type or _default_heap_type], len(heap)
    heap.append(value)
    _siftup(heap, comparer, index)


def heappop(
    heap: ty.MutableSequence[_T],
    index: int | None = None,
    heap_type: ty.Optional[HeapType] = None,
) -> _T:
    comparer, index = _cmp_heap_type_map[heap_type or _default_heap_type], index or 0
    heap[index], heap[-1] = heap[-1], heap[index]
    value = heap.pop()
    _siftdown(heap, comparer, index, len(heap))
    return value


def _siftup(heap: ty.MutableSequence[_T], comparer: _CompareF[_T], index: int):
    while index > 0:
        parent = (index - 1) >> 1
        pv, cv = heap[parent], heap[index]
        if comparer(pv, cv):
            heap[index], heap[parent] = pv, cv
            index = parent
        else:
            break


def _siftdown(
    heap: ty.MutableSequence[_T], comparer: _CompareF[_T], parent: int, size: int
):
    while True:
        left = 2 * parent + 1
        right = left + 1
        if left >= size:
            break
        index = left if right >= size or comparer(heap[right], heap[left]) else right
        pv, cv = heap[parent], heap[index]
        if comparer(pv, cv):
            heap[index], heap[parent] = pv, cv
            parent = index
        else:
            break
