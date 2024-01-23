from ._util import ValueList, myhash, Hashable, Array
import typing as ty

_KeyType = ty.TypeVar("_KeyType", str, int, float, bytes, Hashable)
_ValueType = ty.TypeVar("_ValueType")


class KeyValueNode(ty.Generic[_KeyType, _ValueType]):
    def __init__(self, key: _KeyType, value: _ValueType) -> None:
        self.key = key
        self.value = value

    def __myhash__(self) -> int:
        return myhash(self.key)


class HashTable(ty.Generic[_KeyType, _ValueType]):
    def __init__(
        self, iterable: ty.Iterable[tuple[_KeyType, _ValueType]] | None = None, /
    ) -> None:
        self._store: Array[ValueList[KeyValueNode[_KeyType, _ValueType]]] = Array(8)
        self._used: int = 0
        self._store.fill(ValueList)

    @property
    def _size(self) -> int:
        return self._store._size
