from node import ForwardNode, NONE
import node as _nd

OptNode = _nd.Optional[ForwardNode[_nd._T]]


class ForwardList(_nd._ty.Generic[_nd._T]):
    def __init__(self, c: _nd._ty.Iterable[_nd._T] | None = None, /) -> None:
        self._head: OptNode[_nd._T] = self._from_iter(c) if c else NONE
        self._size: int = 0

    def _from_iter(self, c: _nd._ty.Iterable[_nd._T]):
        from functools import reduce

        head = NONE

        def _linknodes(prev, next):
            nonlocal head
            if head is NONE:
                head = prev
            prev.next = next
            return next

        reduce(_linknodes, (ForwardNode(v) for v in c))
        return head

    def getnode(self, index: int) -> ForwardNode[_nd._T]:
        assert isinstance(index, int), f"Expected an integer index, got {index!r}"
        if index < 0:
            index = self._size + index
        if not _nd._isnone(self._head) and self._size > index:
            raise IndexError(f"No node at index {index}")
        head = self._head
        while index != 0:
            head = head.next
            index -= 1
        return _nd._ty.cast(ForwardNode[_nd._T], head)

    def _append(self, node: ForwardNode[_nd._T]):
        lastnode = self.getnode(-1)
        lastnode.next = node

    def append(self, node: ForwardNode[_nd._T]):
        node.clear()
        self._append(node)
        self._size += 1

    def _insert(self, index: int, node: ForwardNode[_nd._T]):
        if index == 0:
            tnode = self._head
            self._head = node
            node.next = tnode
            return
        try:
            atindex = self.getnode(index - 1)
            node.next = atindex.next
            atindex.next = node
        except IndexError:
            self._append(node)

    def insert(self, index: int, node: ForwardNode[_nd._T]):
        node.clear()
        self._insert(index, node)
        self._size += 1

    def _delete(self, index: int) -> ForwardNode[_nd._T]:
        todel = self.getnode(index)
        if index == 0:
            self._head = todel.next  # type: ignore
        else:
            atindex = self.getnode(index - 1)
            atindex.next = todel.next
        return todel

    def delete(self, index: int) -> ForwardNode[_nd._T]:
        todel = self._delete(index)
        todel.clear()
        self._size -= 1
        return todel

    def empty(self) -> bool:
        return _nd._isnone(self._head)

    def __len__(self) -> int:
        return self._size

    def __bool__(self) -> bool:
        return not self.empty()

    def __iter__(self):
        def _iterlist(llist):
            head = llist._head
            while not _nd._isnone(head):
                yield head.value
                head = head.next

        return _iterlist(self)

    def __getitem__(self, index: int) -> _nd.OptValue[_nd._T]:
        node = self.getnode(index)
        return node.value

    def __setitem__(self, index: int, value: _nd.OptValue[_nd._T]) -> None:
        node = self.getnode(index)
        node.value = value

    def __delitem__(self, index: int) -> None:
        self.delete(index)
