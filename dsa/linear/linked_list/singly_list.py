import typing as ty
from .node import ForwardNode
from .abc import ListABC, NodeABC

_T = ty.TypeVar("_T")


class SinglyList(ListABC[_T]):
    def __init__(self, iterable: ty.Iterable[_T] | None = None, /) -> None:
        self._head: None | NodeABC[_T] = None
        self._size = 0
        if iterable is not None:
            self.extend(iterable)

    def size(self) -> int:
        return self._size

    def nodefactory(self, value: _T) -> NodeABC[_T]:
        return ForwardNode(value)

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
            temp.next = self.nodefactory(value)
            temp = temp.next
            size += 1

        if self.empty():
            self._head = head.next
            self._size = size
        else:
            lastnode = self.getnode(-1)
            lastnode.next = head.next
            self._size += size

    def clear(self):
        self._head = None
        self._size = 0

    def insert(self, index: int, node: NodeABC[_T]):
        node.clear()
        if index == 0 or self.empty():
            node.next = self._head
            self._head = node
        else:
            try:
                before = self.getnode(index - 1)
                node.next = before.next
                before.next = node
            except IndexError:
                lastnode = self.getnode(-1)
                lastnode.next = node
        self._size += 1

    def delnode(self, index: int) -> NodeABC[_T]:
        index = self._size + index if index < 0 else index
        target = self.getnode(index)
        if index == 0:
            self._head = self._head.next # type: ignore
        else:
            before = self.getnode(index - 1)
            before.next = target.next
        target.clear()
        self._size -= 1
        return target

    def __reversed__(self) -> ty.Iterator[NodeABC[_T]]:
        return reversed(self)
