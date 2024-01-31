import typing as ty

T = ty.TypeVar("T")


class Node(ty.Generic[T]):
    def __init__(
        self, value: T, *, next: "Node[T] | None" = None, prev: "Node[T] | None" = None
    ) -> None:
        self.value = value
        self.next = next
        self.prev = prev

    def clear(self) -> ty.Self:
        self.next = None
        self.prev = None
        return self

    def __str__(self) -> str:
        return f"Node({self.value!r})"

    __repr__ = __str__


class SimpleLinkedList(ty.Generic[T]):
    def __init__(self, iterable: ty.Iterable[Node[T]] | None = None) -> None:
        self._head: Node[T] | None = None
        self._tail: Node[T] | None = None
        self._size = 0
        if iterable is not None:
            self.extend(iterable)

    def _append(self, node: Node[T]):
        if self._tail is None:
            self._head = node
            self._tail = node
        else:
            node.prev = self._tail
            self._tail.next = node
            self._tail = node

    def _appendleft(self, node: Node[T]):
        if self._head is None:
            self._head = node
            self._tail = node
        else:
            node.next = self._head
            self._head.prev = node
            self._head = node

    def _pop(self):
        if self._tail is None:
            raise ValueError
        node = self._tail
        self._tail = node.prev
        if self._tail is None:
            self._head = None
        else:
            self._tail.next = None
        return node

    def _popleft(self):
        if self._head is None:
            raise ValueError
        node = self._head
        self._head = node.next
        if self._head is None:
            self._tail = None
        else:
            self._head.prev = None
        return node

    def _appendnode(self, node: Node[T], appender: ty.Callable[[Node[T]], None]):
        self._size += 1
        node.clear()
        appender(node)

    def _popnode(self, popper: ty.Callable[[], Node[T]]):
        node = popper()
        self._size -= 1
        return node.clear()

    def append(self, node: Node[T]):
        self._appendnode(node, self._append)

    def appendleft(self, node: Node[T]):
        self._appendnode(node, self._appendleft)

    def pop(self):
        return self._popnode(self._pop)

    def popleft(self):
        return self._popnode(self._popleft)

    def _getnode(self, index: int, iterable: ty.Iterable[Node[T]]):
        for idx, node in enumerate(iterable):
            if idx == index:
                return node

    def getnode(self, index: int):
        assert isinstance(
            index, int
        ), f"expected integer index, got {type(index).__name__}"
        iterable = reversed(self) if index < 0 else self
        node = self._getnode(abs(index) - (index < 0), iterable)
        if node is None:
            raise IndexError
        return node

    def _remove(self, index: int):
        node = self.getnode(index)
        if node is self._head:
            self._head = node.next
        if node is self._tail:
            self._tail = node.prev
        if node.prev is not None:
            node.prev.next = node.next
        if node.next is not None:
            node.next.prev = node.prev
        return node.clear()

    def remove(self, index: int):
        self._size -= 1
        return self._remove(index)

    def index(self, node: Node[T]):
        for idx, _node in enumerate(self):
            if node is _node:
                return idx
        raise ValueError(f"Node not found is this list.")

    def clear(self):
        self.__init__()

    def _extend(
        self, adder: ty.Callable[[Node[T]], None], iterable: ty.Iterable[Node[T]]
    ):
        for node in iterable:
            adder(node)

    def extend(self, iterable: ty.Iterable[Node[T]]):
        self._extend(self._append, iterable)

    def extendleft(self, iterable: ty.Iterable[Node[T]]):
        self._extend(self._appendleft, iterable)

    def __len__(self) -> int:
        return self._size

    def _iter(
        self, start: Node[T] | None, stepper: ty.Callable[[Node[T]], Node[T] | None]
    ) -> ty.Generator[Node[T], None, None]:
        current = start
        while current is not None:
            yield current
            current = stepper(current)

    def __iter__(self) -> ty.Generator[Node[T], None, None]:
        return self._iter(self._head, lambda node: node.next)

    def __reversed__(self) -> ty.Generator[Node[T], None, None]:
        return self._iter(self._tail, lambda node: node.prev)


class ValueList(ty.Generic[T]):
    def __init__(self) -> None:
        self._list: SimpleLinkedList[T] = SimpleLinkedList()

    def append(self, value: T):
        node = Node(value)
        self._list.append(node)

    def remove(self, value: T):
        for idx, _value in enumerate(self):
            if value == _value:
                node = self._list.remove(idx)
                return node.value
        raise ValueError

    def delvalue(self, index: int) -> T:
        return self._list.remove(index).value

    def _iter(self, iterable: ty.Iterable[Node[T]]) -> ty.Generator[T, None, None]:
        for node in iterable:
            yield node.value

    def __len__(self) -> int:
        return self._list._size

    def __iter__(self) -> ty.Generator[T, None, None]:
        return self._iter(self._list)

    def __reversed__(self) -> ty.Generator[T, None, None]:
        return self._iter(reversed(self._list))

    def __str__(self) -> str:
        vals = ", ".join(map(repr, self._list))
        return "[" + vals + "]"

    __repr__ = __str__


class Slot(ty.Generic[T]):
    def __init__(self, value: T) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f"Slot({self.value!r})"


class Array(ty.Generic[T]):
    def __init__(self, size: int) -> None:
        assert isinstance(size, int) and size >= 0, size
        self._list: list[Slot[T]] = []
        self._size = 0
        self._grow(size)

    def _grow(self, size: int):
        init = ty.cast(T, None)
        slots = [Slot(init) for _ in range(size)]
        self._list.extend(slots)
        self._size += size

    def __setitem__(self, index: int, value: T):
        self._list[index].value = value

    def __getitem__(self, index: int) -> T:
        return self._list[index].value

    def fill(self, creator: ty.Callable[[], T]):
        for slot in self._list:
            slot.value = creator()

    def clear(self):
        self.fill(lambda: ty.cast(T, None))

    def _iter(self, iterable: ty.Iterable[Slot[T]]) -> ty.Generator[T, None, None]:
        for slot in iterable:
            yield slot.value

    def __iter__(self) -> ty.Generator[T, None, None]:
        return self._iter(self._list)

    def __reversed__(self) -> ty.Generator[T, None, None]:
        return self._iter(reversed(self._list))

    def __len__(self) -> int:
        return self._size


@ty.runtime_checkable
class Hashable(ty.Protocol):
    def __myhash__(self) -> int:
        ...


_HashableType = ty.TypeVar("_HashableType", str, int, float, bytes, Hashable)


def _myhash_function(value: float | int | bytes | str, *, shift: int = 2):
    if not isinstance(value, (str, float, bytes, int)):
        raise TypeError(
            "Unhashable type. Expected float, int, "
            f"str or bytes, got {type(value).__name__}"
        )
    hash_value = 1
    if isinstance(value, (float, int)):
        value = str(value).encode()
        hash_value = 2
    elif isinstance(value, str):
        value = value.encode()
        hash_value = 4
    for byte in value:
        hash_value <<= shift
        hash_value += byte
    return hash_value


def myhash(hashable: _HashableType, /) -> int:
    if isinstance(hashable, Hashable):
        hash_value = hashable.__myhash__()
        assert isinstance(
            hash_value, int
        ), f"Hash value must be an integer, got {hash_value!r}"
        return hash_value
    return _myhash_function(hashable)
