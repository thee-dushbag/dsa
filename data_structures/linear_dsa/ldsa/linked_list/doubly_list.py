from .abc import ListABC, NodeABC
from .node import Node
import typing as ty

_T = ty.TypeVar("_T")


class DoublyList(ListABC[_T]):
    def __init__(self, iterable: ty.Iterable[_T] | None = None, /) -> None:
        self._head: NodeABC[_T] | None = None
        self._size: int = 0
        if iterable is not None:
            self.extend(iterable)

    def size(self) -> int:
        return self._size

    def nodefactory(self, value: _T) -> NodeABC[_T]:
        return Node(value)

    def empty(self) -> bool:
        return self._head is None

    def getnode(self, index: int) -> NodeABC[_T]:
        index = self._size + index if index < 0 else index
        for current, node in enumerate(self):
            if current == index:
                return node
        raise IndexError

    def __iter__(self) -> ty.Iterator[NodeABC[_T]]:
        head = self._head
        while head is not None:
            yield head
            head = head.next

    def extend(self, iterable: ty.Iterable[_T]):
        head = self.nodefactory(ty.cast(_T, None))
        size, temp = 0, head

        for value in iterable:
            node = self.nodefactory(value)
            temp.next = node
            node.prev = temp
            temp = node
            size += 1

        if self.empty():
            self._head = head.next
            self._size = size
        else:
            lastnode = self.getnode(-1)
            if head.next is not None:
                head.next.prev = lastnode
            lastnode.next = head.next
            self._size += size

    def clear(self):
        self._head = None
        self._size = 0

    def insert(self, index: int, node: NodeABC[_T]):
        node.clear()
        if index == 0 or self.empty():
            node.next = self._head
            if self._head is not None:
                self._head.prev = node
            self._head = node
        else:
            try:
                target = self.getnode(index)
                target.prev.next = node  # type: ignore
                node.next = target
                node.prev = target.prev
                target.prev = node
            except IndexError:
                lastnode = self.getnode(-1)
                lastnode.next = node
                node.prev = lastnode
        self._size += 1

    def delnode(self, index: int) -> NodeABC[_T]:
        index = self._size + index if index < 0 else index
        target = self.getnode(index)
        if index == 0:
            self._head = self._head.next  # type: ignore
        if target.prev is not None:
            target.prev.next = target.next
        if target.next is not None:
            target.next.prev = target.prev
        target.clear()
        self._size -= 1
        return target

    def __reversed__(self) -> ty.Iterator[NodeABC[_T]]:
        return reversed(self)


