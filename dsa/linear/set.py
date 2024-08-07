from ._util import ValueList, Hashable, Array, myhash
import typing as ty

_ValueType = ty.TypeVar("_ValueType", str, int, float, bytes, Hashable)


class Set(ty.MutableSet[_ValueType]):
    def __init__(self, iterable: ty.Iterable[_ValueType] | None = None, /) -> None:
        self._store: Array[ValueList[_ValueType]] = Array(8)
        self._store.fill(ValueList)
        self._max_load: float = 0.7
        self._used: int = 0
        if iterable is not None:
            for item in iterable:
                self.add(item)

    @property
    def _size(self) -> int:
        return self._store._size

    @property
    def _load_factor(self) -> float:
        return self._used / self._size

    def _stabilize(self):
        if self._load_factor < self._max_load:
            return
        values = list(self)
        self._store._grow(self._size)
        self._store.fill(ValueList)
        for value in values:
            self.add(value)

    def contains(self, value: ty.Any):
        _hash = myhash(value)
        index = _hash % self._size
        vlist = self._store[index]
        for v in vlist:
            if myhash(v) == _hash:
                return True
        return False

    def add(self, value: _ValueType):
        _hash = myhash(value)
        index = _hash % self._size
        vlist = self._store[index]
        for _value in vlist:
            if myhash(_value) == _hash:
                return
        vlist.append(value)
        self._used += 1
        self._stabilize()

    def _remove(self, value: _ValueType) -> bool:
        _hash = myhash(value)
        index = _hash % self._size
        vlist = self._store[index]
        for idx, _value in enumerate(vlist):
            if myhash(_value) == _hash:
                vlist.delvalue(idx)
                return True
        return False

    def discard(self, value: _ValueType) -> None:
        self._used -= self._remove(value)

    def remove(self, value: _ValueType):
        if not self._remove(value):
            raise ValueError(value)
        self._used -= 1

    def pop(self) -> _ValueType:
        for value in self:
            self.remove(value)
            return value
        raise ValueError("pop from an empty set.")

    def clear(self) -> None:
        self._store.fill(ValueList)
        self._used = 0

    def union(self, other: "ty.AbstractSet[_ValueType]") -> "Set[_ValueType]":
        return Set([*self, *other])

    def intersection(self, other: "ty.AbstractSet[_ValueType]") -> "Set[_ValueType]":
        return Set([item for item in self if item in other])

    def difference(self, other: "ty.AbstractSet[_ValueType]") -> "Set[_ValueType]":
        return Set([item for item in self if item not in self.intersection(other)])

    def __eq__(self, other: object) -> bool:
        return all(item in other for item in self) and all(
            item in self for item in other
        ) if isinstance(other, ty.Iterable) else NotImplemented

    __and__ = intersection
    __sub__ = difference
    __or__ = __add__ = union

    def __contains__(self, x: object) -> bool:
        return self.contains(x)

    def __bool__(self) -> bool:
        return self._used > 0

    def __str__(self) -> str:
        vals = ", ".join(map(repr, self))
        return "{" + vals + "}"

    def __len__(self) -> int:
        return self._used

    def __iter__(self) -> ty.Generator[_ValueType, None, None]:
        for vlist in self._store:
            yield from vlist

    def __reversed__(self) -> ty.Generator[_ValueType, None, None]:
        for vlist in reversed(self._store):
            yield from reversed(vlist)
