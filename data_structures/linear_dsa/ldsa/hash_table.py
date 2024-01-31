from ._util import ValueList, myhash, Hashable, Array
import typing as ty

_KeyType = ty.TypeVar("_KeyType", str, int, float, bytes, Hashable)
_U = ty.TypeVar("_U", str, int, float, bytes, Hashable)
_ValueType = ty.TypeVar("_ValueType")
_T = ty.TypeVar("_T")


class _MISSING:
    ...


def _identity(item: _T) -> _T:
    return item


_missing = _MISSING()


class KeyValueNode(ty.Generic[_KeyType, _ValueType]):
    def __init__(self, key: _KeyType, value: _ValueType) -> None:
        self.key = key
        self.value = value

    def __myhash__(self) -> int:
        return myhash(self.key)


class HashTable(ty.MutableMapping[_KeyType, _ValueType]):
    def __init__(
        self, iterable: ty.Iterable[tuple[_KeyType, _ValueType]] | None = None, /
    ) -> None:
        self._store: Array[ValueList[KeyValueNode[_KeyType, _ValueType]]] = Array(8)
        self._max_load: float = 0.7
        self._store.fill(ValueList)
        self._used: int = 0
        if iterable is not None:
            self.update(iterable)

    def _setitem(self, key: _KeyType, value: _ValueType):
        _hash = myhash(key)
        index = _hash % self._size
        vlist = self._store[index]
        for slot in vlist:
            if myhash(slot) == _hash:
                slot.value = value
                return
        node = KeyValueNode(key, value)
        vlist.append(node)
        self._used += 1
        self._stabilize()

    def _delitem(self, key: _KeyType) -> KeyValueNode[_KeyType, _ValueType] | _MISSING:
        _hash = myhash(key)
        index = _hash % self._size
        vlist = self._store[index]
        for index, slot in enumerate(vlist):
            if myhash(slot) == _hash:
                node = vlist.delvalue(index)
                self._used -= 1
                return node
        return _missing

    def _getitem(self, key: _KeyType) -> _ValueType | _MISSING:
        _hash = myhash(key)
        index = _hash % self._size
        vlist = self._store[index]
        for slot in vlist:
            if myhash(slot) == _hash:
                return slot.value
        return _missing

    def __contains__(self, key: object) -> bool:
        return not isinstance(self._getitem(ty.cast(_KeyType, key)), _MISSING)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, HashTable):
            return False
        keys: set[_KeyType] = set(*other, *self)
        for key in keys:
            v1, v2 = self._getitem(key), other._getitem(key)
            if any(map(isinstance, (v1, v2), (_MISSING, _MISSING))) or v1 != v2:
                return False
        return True

    def __len__(self) -> int:
        return self._used

    def get(self, key: _KeyType, default: _T = _missing) -> _ValueType | _T:
        value = self._getitem(key)
        if isinstance(value, _MISSING):
            if isinstance(default, _MISSING):
                raise KeyError(key)
            return default
        return value

    def _iter(
        self,
        transform: ty.Callable[[KeyValueNode[_KeyType, _ValueType]], _T],
        prep_store=_identity,
        prep_vlist=_identity,
    ) -> ty.Generator[_T, None, None]:
        for vlist in prep_store(self._store):
            for slot in prep_vlist(vlist):
                yield transform(slot)

    def values(self) -> ty.Generator[_ValueType, None, None]:
        return self._iter(lambda slot: slot.value)

    def keys(self) -> ty.Generator[_KeyType, None, None]:
        return self._iter(lambda slot: slot.key)

    def items(self) -> ty.Generator[tuple[_KeyType, _ValueType], None, None]:
        return self._iter(lambda slot: (slot.key, slot.value))

    __iter__ = keys

    def __reversed__(self) -> ty.Generator[_ValueType, None, None]:
        return self._iter(lambda slot: slot.value, reversed, reversed)

    def __setitem__(self, key: _KeyType, value: _ValueType) -> None:
        self._setitem(key, value)

    def __delitem__(self, key: _KeyType) -> None:
        node = self._delitem(key)
        if isinstance(node, _MISSING):
            raise KeyError(key)

    def __getitem__(self, key: _KeyType) -> _ValueType:
        return ty.cast(_ValueType, self.get(key))

    def pop(self, key: _KeyType, default: _T = _missing) -> _ValueType | _T:
        node = self._delitem(key)
        if isinstance(node, _MISSING):
            if isinstance(default, _MISSING):
                raise KeyError(key)
            return default
        return node.value

    def setdefault(self, key: _KeyType, default: _ValueType) -> _ValueType:
        value = self._getitem(key)
        if isinstance(value, _MISSING):
            self._setitem(key, default)
            value = default
        return value

    def update(
        self,
        other: "HashTable[_KeyType, _ValueType] | ty.Iterable[tuple[_KeyType, _ValueType]]",
    ):
        iterable = other.items() if isinstance(other, HashTable) else other
        for key, value in iterable:
            self._setitem(key, value)  # type: ignore

    def popitem(self) -> tuple[_KeyType, _ValueType]:
        rev_items = self._iter(lambda s: (s.key, s.value), reversed, reversed)
        for key, value in rev_items:
            self.pop(key)
            return key, value
        raise KeyError("Dictionary is empty.")

    def clear(self) -> None:
        self._store.clear()
        self._store.fill(ValueList)
        self._used = 0

    def __str__(self) -> str:
        items = [f"{key!r}: {value!r}" for key, value in self.items()]
        return "{" + ", ".join(items) + "}"

    __repr__ = __str__

    @property
    def _size(self) -> int:
        return self._store._size

    @property
    def _load_factor(self) -> float:
        return self._used / self._size

    def _stabilize(self):
        if self._load_factor < self._max_load:
            return
        values: list[tuple[_KeyType, _ValueType]] = [*self.items()]
        self._store._grow(self._size)
        self.clear()
        self.update(values)

    @classmethod
    def fromkeys(
        cls: type['HashTable[_U, _T]'],
        iterable: ty.Iterable[_U],
        value: _T | _MISSING = _missing,
    ) -> "HashTable[_U, _T]":
        value = ty.cast(_T, None) if isinstance(value, _MISSING) else value
        return cls(map(lambda key: (key, value), iterable))
