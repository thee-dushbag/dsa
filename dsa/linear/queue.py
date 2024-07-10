from .linked_list import list as _list
from . import heap as _heap
import typing as ty

_T = ty.TypeVar("_T")


__all__ = "Queue", "LIFOQueue", "PriorityQueue", "Deque"


class QueueError(Exception):
    ...


class QueueFull(QueueError):
    ...


class QueueEmpty(QueueError):
    ...


class Queue(ty.Generic[_T]):
    def __init__(
        self, iterable: ty.Iterable[_T] | None = None, maxsize: int | None = None
    ) -> None:
        self._queue = self._store_factory()
        self._maxsize = maxsize or 0
        self._size = 0
        if iterable is not None:
            self.extend(iterable)

    def _store_factory(self) -> ty.MutableSequence:
        return _list.SinglyLinkedList()

    def full(self) -> bool:
        return False if self._maxsize <= 0 else self._size >= self._maxsize

    def empty(self) -> bool:
        return self._size <= 0

    def __len__(self) -> int:
        return self._size

    def append(self, value: _T):
        if self.full():
            raise QueueFull
        self._size += 1
        self._append(value)

    def pop(self) -> _T:
        if self.empty():
            raise QueueEmpty
        self._size -= 1
        return self._pop()

    def _append(self, value: _T):
        self._queue.append(value)

    def _pop(self) -> _T:
        return self._queue.pop(0)

    def extend(self, iterable: ty.Iterable[_T]):
        for value in iterable:
            self.append(value)

    def __str__(self) -> str:
        name = self.__class__.__name__
        return f"{name}({list(self._queue)})"

    __repr__ = __str__


class LIFOQueue(Queue[_T]):
    def _store_factory(self) -> ty.MutableSequence:
        return list()

    def _pop(self) -> _T:
        return self._queue.pop()

    def _append(self, value: _T):
        return self._queue.append(value)


class PriorityQueue(Queue[_T]):
    heap_type: _heap.HeapType = _heap.HeapType.MIN

    def _store_factory(self) -> ty.MutableSequence:
        return list()

    def _append(self, value: _T):
        _heap.heappush(self._queue, value, heap_type=self.heap_type)

    def _pop(self) -> _T:
        return _heap.heappop(self._queue, 0, heap_type=self.heap_type)


class Deque(LIFOQueue[_T]):
    def _store_factory(self) -> ty.MutableSequence:
        return _list.CirDoublyLinkedList()

    def appendleft(self, value: _T):
        if self.full():
            raise QueueFull
        self._size += 1
        self._appendleft(value)

    def popleft(self) -> _T:
        if self.empty():
            raise QueueEmpty
        self._size -= 1
        return self._popleft()

    def _appendleft(self, value: _T):
        self._queue.insert(0, value)

    def _popleft(self) -> _T:
        return self._queue.pop(0)

    def extendleft(self, iterable: ty.Iterable[_T]):
        for value in iterable:
            self.appendleft(value)
