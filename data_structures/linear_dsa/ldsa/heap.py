import typing as ty
from enum import StrEnum, auto

__all__ = "heapify", "HeapType", "heappush", "heappop", "setheaptype", "getheaptype"

_T = ty.TypeVar("_T")
_CompareF = ty.Callable[[_T, _T], bool]


# Hail MYPY, bloody bastard!!!
class _LTComparisson(ty.Protocol):
    def __lt__(self: ty.Self, value: ty.Self) -> bool: ...

class _GTComparisson(ty.Protocol):
    def __gt__(self: ty.Self, value: ty.Self) -> bool: ...

class _LEComparisson(ty.Protocol):
    def __le__(self: ty.Self, value: ty.Self) -> bool: ...

class _GEComparisson(ty.Protocol):
    def __ge__(self: ty.Self, value: ty.Self) -> bool: ...

_min_heap: _CompareF[_LTComparisson]    = lambda head, child: head > child
_max_heap: _CompareF[_GTComparisson]    = lambda head, child: head < child
_min_heap_eq: _CompareF[_GEComparisson] = lambda head, child: head >= child
_max_heap_eq: _CompareF[_LEComparisson] = lambda head, child: head <= child

class HeapType(StrEnum):
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
    MIN = auto()
    MAX = auto()
    MINEQ = auto()
    MAXEQ = auto()


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


def heapify(
    heap: ty.MutableSequence, *, heap_type: ty.Optional[HeapType] = None
) -> None:
    """
    Convert a mutable sequence (eq list) to a heap
    (MIN-HEAP default or specify using param heap_type)
    """
    comparer, size = _cmp_heap_type_map[heap_type or _default_heap_type], len(heap)
    for head in reversed(range(size // 2)):
        _heapify_impl(heap, head, comparer)


def heappush(
    heap: ty.MutableSequence[_T], item: _T, *, heap_type: ty.Optional[HeapType] = None
):
    """
    Add an element to heep, uses default heap type
    if the heap_type is not specified.
    """
    comparer, index = _cmp_heap_type_map[heap_type or _default_heap_type], len(heap)
    heap.append(item)
    while index:
        parent = (index - 1) >> 1
        if comparer((pv := heap[parent]), item):
            heap[parent], heap[index] = item, pv
            index = parent
        else:
            break


def heappop(
    heap: ty.MutableSequence[_T],
    index: ty.Optional[int] = None,
    *,
    heap_type: ty.Optional[HeapType] = None,
) -> _T:
    """
    Remove and get an Item from the heap.
    Uses the default heaptype if not specified.
    """
    comparer = _cmp_heap_type_map[heap_type or _default_heap_type]
    index = index or 0
    heap[index], heap[-1] = heap[-1], heap[index]  # Raise IndexError when necessary
    item: _T = heap.pop()
    if heap:
        _heapify_impl(heap, index, comparer)
    return item


class _Child(ty.Generic[_T]):
    """
    Simple representation of a node's state.
    The node identified by the head index,
    its parent as parent which may not exist
    if its value is -1, its left and right index
    represented as left and right which may or may
    not exist as calculated by has_left or has_right
    respectively.
    """
    def __init__(
        self, heap: ty.MutableSequence[_T], head: int, cmp: _CompareF[_T]
    ) -> None:
        self._head: int = head
        self._heap = heap
        self.cmp = cmp
        self.head = head
    
    @property
    def size(self) -> int:
        return len(self.heap)

    @property
    def parent(self) -> ty.Optional[int]:
        if not self.head: return None
        return (self.head - 1) >> 1

    @property
    def heap(self) -> ty.MutableSequence:
        return self._heap

    @property
    def head(self) -> int:
        return self._head

    @head.setter
    def head(self, head: int) -> None:
        assert (
            head < self.size
        ), "head index must be lower than the size, got {head} >= {self.size}"
        self._head = head

    @property
    def left(self) -> int:
        return 2 * self.head + 1

    @property
    def right(self) -> int:
        return 2 * (self.head + 1)

    def swaped_index(self) -> ty.Optional[int]:
        if self.has_right:
            value, left = self.heap[self.right], self.heap[self.left]
            index = self.left if self.cmp(value, left) else self.right
        elif self.has_left:
            index = self.left
        else:
            return None
        head, value = self.heap[self.head], self.heap[index]
        if self.cmp(head, value):
            self.heap[self.head], self.heap[index] = value, head
            return index
        return None

    @property
    def has_left(self) -> bool:
        return self.left < self.size

    @property
    def has_right(self) -> bool:
        return self.right < self.size

    def __str__(self) -> str:
        return (
            f"Child(head={self.head}, parent={self.parent},"
            f"left={self.left if self.has_left else None},"
            f"right={self.right if self.has_right else None})"
        )


def _heapify_impl(
    heap: ty.MutableSequence[_T], head: int, cmp: _CompareF[_T]
):
    child = _Child(heap, head, cmp)
    _heapify_detail_impl(child)


def _heapify_detail_impl(child: _Child) -> None:
    index = child.swaped_index()
    if index is None: return
    child.head = index
    _heapify_detail_impl(child)
