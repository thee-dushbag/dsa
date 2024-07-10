from .abc import ListABC
from .node import CircularNode
import typing as ty


_T = ty.TypeVar("_T")


class CircularDoublyList(ListABC[_T]):
    def __init__(self, iterable: ty.Iterable[_T] | None = None, /) -> None:
        self._head: CircularNode[_T] | None = None
        self._size: int = 0
        if iterable is not None:
            self.extend(iterable)

    def size(self) -> int:
        return self._size

    def nodefactory(self, value: _T) -> CircularNode[_T]:
        return CircularNode(value)

    def empty(self) -> bool:
        return self._head is None

    def clear(self):
        self._head = None
        self._size = 0

    def getnode(self, index: int) -> CircularNode[_T]:
        _index = index + self._size if index < 0 else index
        if self._head is None or _index < 0 or _index >= self._size:
            raise IndexError
        node = self._head
        if index < 0:
            while index != 0:
                index += 1
                node = ty.cast(CircularNode[_T], node.prev)
        else:
            while index != 0:
                index -= 1
                node = ty.cast(CircularNode[_T], node.next)
        return node

    def _iter(self, _next) -> ty.Iterator[CircularNode[_T]]:
        if self._head is None:
            return
        head = self._head
        for _ in range(self._size):
            yield head
            head = _next(head)

    def __iter__(self) -> ty.Iterator[CircularNode[_T]]:
        return self._iter(lambda node: node.next)

    def __reversed__(self) -> ty.Iterator[CircularNode[_T]]:
        return self._iter(lambda node: node.prev)

    def insert(self, index: int, node: CircularNode[_T]):
        node.clear()
        if self._head is None:
            self._head = node
        else:
            try:
                target = self.getnode(index)
            except IndexError:
                target = self._head
            target.prev.next = node
            node.prev = target.prev
            node.next = target
            target.prev = node
        if index == 0:
            self._head = self._head.prev
        self._size += 1

    def extend(self, iterable: ty.Iterable[_T]):
        head = self.nodefactory(ty.cast(_T, None))
        temp, size = head, 0

        for value in iterable:
            node = self.nodefactory(value)
            temp.next = node
            node.prev = temp
            temp = node
            size += 1

        if head is head.next:
            return

        head = head.next

        if self._head is None:
            temp.next = head
            head.prev = temp
            self._head = head
            self._size = size
        else:
            self._head.prev.next = head
            head.prev = self._head.prev
            temp.next = self._head
            self._head.prev = temp
            self._size += size

    def delnode(self, index: int) -> CircularNode[_T]:
        target = self.getnode(index)
        if self._size == 1:
            self._head = None
        if index == 0:
            self._head = target.next
        target.next.prev = target.prev
        target.prev.next = target.next
        self._size -= 1
        target.clear()
        return target
