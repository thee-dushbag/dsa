from .linked_list.list import CirDoublyLinkedList
from .array import Array


def hash_function(key: float | str | bytes, /, *, shift_size: int | None = None):
    if not isinstance(key, (str, float, bytes, int)):
        raise Exception(
            f"Unhashable key. Expected float, str or bytes, but got {type(key)}"
        )
    shift_size = 3 if shift_size is None else shift_size
    hash_value = 0x1
    if isinstance(key, (float, int)):
        key = str(key).encode()
        hash_value = 0x2
    elif isinstance(key, str):
        key = key.encode()
        hash_value = 0x3
    for byte in key:
        hash_value <<= shift_size
        hash_value |= byte
    return hash_value


class Node:
    def __init__(self, key: float | str | bytes, value: object) -> None:
        self.value = value
        self.key = key


class HashTable:
    def __init__(self) -> None:
        self._size = 32
        self._store: Array[CirDoublyLinkedList[Node] | Node] = Array(self._size)
        self._used = 0
        self._max_load = 0.6

    @property
    def _load_factor(self) -> float:
        return self._used / self._size

    def _grow(self):
        if self._load_factor >= self._max_load:
            self._size *= 2
            self._store.grow(self._size)
            self._rearrange()

    def _rearrange(self):
        flattened: list[Node] = []
        for d in self._store:
            if isinstance(d, CirDoublyLinkedList):
                flattened.extend(d)
            elif isinstance(d, Node):
                flattened.append(d)
        self._store.clear()
        for node in flattened:
            self._insert(node)

    def _get(self, key: str | bytes | float):
        index = hash_function(key) % self._size
        if isinstance((l := self._store[index]), CirDoublyLinkedList):
            for node in l:
                if node.key == key:
                    return node
        elif isinstance((n := self._store[index]), Node):
            if n.key == key:
                return n
        return key

    def _delete(self, key: str | bytes | float):
        index = hash_function(key) % self._size
        if isinstance((l := self._store[index]), CirDoublyLinkedList):
            for index, node in enumerate(l):
                if node.key == key:
                    l.pop(index)
                    return node
        elif isinstance((n := self._store[index]), Node):
            if n.key == key:
                self._store[index].clear()  # type: ignore
                return n
        return key

    def _insert(self, node: Node):
        index = hash_function(node.key) % self._size
        if isinstance((l := self._store[index]), CirDoublyLinkedList):
            l.append(node)
        elif isinstance((n := self._store[index]), Node):
            l = CirDoublyLinkedList([n, node])
            self._store[index] = l
        else:
            self._store[index] = node

    def __setitem__(self, key: str | bytes | float, value: object):
        self._insert(Node(key, value))
        self._grow()
        self._used += 1

    def __getitem__(self, key: str | bytes | float):
        node = self._get(key)
        if isinstance(node, Node):
            return node.value
        raise KeyError

    def __delitem__(self, key: str | float | bytes):
        self._delete(key)
        self._used -= 1

    def __iter__(self):
        for data in self._store:
            if isinstance(data, Node):
                yield data.key
            elif isinstance(data, CirDoublyLinkedList):
                for d in data:
                    yield d.key

    def __contains__(self, key):
        return isinstance(key, (float, str, bytes)) and self._get(key) != key

    def items(self):
        for key in self:
            yield key, self[key]

    def __str__(self) -> str:
        items = [f"{key!r}: {value!r}" for key, value in self.items()]
        return "{" + ", ".join(items) + "}"

    __repr__ = __str__
