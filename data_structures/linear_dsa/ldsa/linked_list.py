import typing as ty, dataclasses as dt
from ._none import NONE, Optional, is_not_none

_T = ty.TypeVar("_T")

__all__ = "Node", "BiNode", "ForwardList", "List"


class Node(ty.Generic[_T]):
    def __init__(
        self,
        value: _T,
        *,
        next: Optional["Node[_T]"] = NONE,
    ) -> None:
        self.value = value
        self.next = next

    def clear(self) -> ty.Self:
        self.next = NONE
        return self


class BiNode(ty.Generic[_T]):
    def __init__(
        self,
        value: _T,
        *,
        next: Optional["BiNode[_T]"] = NONE,
        prev: Optional["BiNode[_T]"] = NONE,
    ) -> None:
        self.value = value
        self.next = next
        self.prev = prev

    def clear(self) -> ty.Self:
        self.next = NONE
        self.prev = NONE
        return self


class ForwardList(ty.Generic[_T]):
    def __init__(self, head: Optional[Node[_T]] = NONE):
        self.items = head

    @classmethod
    def fromiter(cls, iterable: ty.Iterable[_T]) -> "ForwardList[_T]":
        try:
            items = iter(iterable)
            head: Optional[Node[_T]] = Node(next(items))
            c_node = head
            for item in items:
                c_node.next = Node(item)
                c_node = c_node.next
        except StopIteration:
            head = NONE
        return cls(head)

    def getindex(self, index: int) -> Node[_T]:
        if not isinstance(index, int):
            raise IndexError(f"Expected n integer index, got {index}")
        if index < 0: index = self.size() + index + 1
        c_node, c_index = self.items, 0
        while is_not_none(c_node):
            if c_index == index:
                return c_node
            c_node = c_node.next
            c_index += 1
        raise IndexError(f"Linked list has no Node at index {index}")

    def lastnode(self) -> Node[_T]:
        if self.items is NONE:
            raise ValueError("Linked List is empty.")
        return self.getindex(-1)


    def insert(self, node: Node[_T], index: int = -1):
        if index == 0:
            node.next = self.items
            self.items = node
            return
        try:
            p_node = self.getindex(index - 1)
            node.next = p_node.next
            p_node.next = node
        except IndexError:
            p_node = self.lastnode()
            p_node.next = node.clear()

    def delete(self, index: int) -> Node[_T]:
        if self.items is NONE:
            raise IndexError(f"Deleting from empty linked list")
        t_node, p_node = self.getindex(index), self.getindex(index - 1)
        p_node.next = t_node.next
        return t_node.clear()

    def append(self, node: Node[_T]):
        if is_not_none(self.items):
            self.lastnode().next = node.clear()
        else:
            self.items = node.clear()

    def empty(self):
        return self.items is NONE

    def size(self) -> int:
        node, size = self.items, 0
        while is_not_none(node.next):
            node = node.next
            size += 1
        return size

    def __len__(self) -> int:
        return self.size()

    def __getitem__(self, __index: int) -> _T:
        return self.getindex(__index).value

    def __delitem__(self, __index: int):
        return self.delete(__index)

    def __bool__(self) -> bool:
        return not self.empty()

    def __iter__(self):
        def nodegen() -> ty.Generator[_T, None, None]:
            c_node = self.items
            while is_not_none(c_node):
                yield c_node.value
                c_node = c_node.next

        return nodegen()

    def __reversed__(self):
        return reversed(list(self))

    def __str__(self) -> str:
        vstr = (f'{v!r}' for v in self)
        fstr = '' if self.empty() else ', '.join(vstr)
        return f'forward_list([{fstr}])'


class List(ty.Generic[_T]):
    def __init__(self, head: Optional[BiNode[_T]]):
        self.items = head

    @classmethod
    def fromiter(cls, iterable: ty.Iterable[_T]) -> "List[_T]":
        try:
            items = iter(iterable)
            head: Optional[BiNode[_T]] = BiNode(next(items))
            c_node = head
            for item in items:
                node = BiNode(item)
                c_node.next, node.prev = node, c_node
                c_node = c_node.next
        except StopIteration:
            head = NONE
        return cls(head)

    def getindex(self, index: int) -> BiNode[_T]:
        if not isinstance(index, int):
            raise IndexError(f"Expected n integer index, got {index}")
        if index < 0: index = self.size() + index + 1
        c_node, c_index = self.items, 0
        while is_not_none(c_node):
            if c_index == index:
                return c_node
            c_node = c_node.next
            c_index += 1
        raise IndexError(f"Linked list has no Node at index {index}")

    def lastnode(self) -> BiNode[_T]:
        if self.items is NONE:
            raise ValueError("Doubly Linked List is empty.")
        return self.getindex(-1)


    def insert(self, node: BiNode[_T], index: int = -1):
        if self.items is NONE:
            self.items = node.clear()
        elif index == 0:
            self.items.prev, node.next = node.clear(), self.items
            self.items = node
        else:
            try:
                if index < 0: index = self.size() + index + 1
                n_node, p_node = self.getindex(index), self.getindex(index - 1)
                node.prev, p_node.next = p_node, node
                node.next, n_node.prev = n_node, node
            except IndexError:
                self.append(node)

    def delete(self, index: int) -> BiNode[_T]:
        if self.items is NONE:
            raise IndexError(f"Deleting from empty doubly linked list")
        t_node, p_node = self.getindex(index), self.getindex(index - 1)
        p_node.next, p_node.prev = t_node.next, t_node.prev
        return t_node.clear()

    def append(self, node: BiNode[_T]):
        if is_not_none(self.items):
            p_node = self.lastnode()
            p_node.next, node.prev = node.clear(), p_node
        else:
            self.items = node.clear()

    def empty(self):
        return self.items is NONE

    def size(self) -> int:
        node, size = self.items, 0
        while is_not_none(node.next):
            node = node.next
            size += 1
        return size

    def __len__(self) -> int:
        return self.size()

    def __getitem__(self, __index: int) -> _T:
        return self.getindex(__index).value

    def __bool__(self) -> bool:
        return not self.empty()

    def __delitem__(self, __index: int):
        return self.delete(__index)

    def __iter__(self):
        def nodegen() -> ty.Generator[_T, None, None]:
            c_node = self.items
            while is_not_none(c_node):
                yield c_node.value
                c_node = c_node.next

        return nodegen()

    def __reversed__(self):
        print("reversed method")
        def nodegen() -> ty.Generator[_T, None, None]:
            try:
                c_node: Optional[BiNode[_T]] = self.lastnode()
                while is_not_none(c_node):
                    print(f"current {c_node.value}")
                    yield c_node.value
                    c_node = c_node.prev
            except ValueError:
                ...

        return nodegen()

    def __str__(self) -> str:
        vstr = (f'{v!r}' for v in self)
        fstr = '' if self.empty() else ', '.join(vstr)
        return f'doubly_list([{fstr}])'
