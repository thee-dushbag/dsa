from .abc import ListABC
import typing as ty

_T = ty.TypeVar("_T")


class MutableSequenceMixin(ty.MutableSequence[_T]):
    def __init__(self, _list: ListABC[_T], /) -> None:
        self._list = _list

    def insert(self, index: int, value: _T) -> None:
        node = self._list.nodefactory(value)
        self._list.insert(index, node)

    def __getitem__(self, index: int) -> _T:
        return self._list.getnode(index).value

    def __setitem__(self, index: int, value: _T):
        node = self._list.getnode(index)
        node.value = value

    def __delitem__(self, index: int) -> _T:
        return self.pop(index)

    def append(self, value: _T) -> None:
        node = self._list.nodefactory(value)
        self._list.insert(self._list.size(), node)

    def clear(self) -> None:
        self._list.clear()

    def extend(self, values: ty.Iterable[_T]) -> None:
        self._list.extend(values)

    def pop(self, index: int = -1) -> _T:
        return self._list.delnode(index).value

    def remove(self, value: _T) -> None:
        index = self.index(value)
        self._list.delnode(index)

    def __iadd__(self, values: ty.Iterable[_T]) -> ty.Self:
        self._list.extend(values)
        return self

    def reverse(self) -> None:
        values = map(lambda node: node.value, reversed(self._list))
        self._list.clear()
        self._list.extend(values)

    def count(self, value: ty.Any) -> int:
        count = 0
        for node in self._list:
            if value == node.value:
                count += 1
        return count

    def index(self, value: ty.Any, start: int = 0, stop: int | None = None) -> int:
        stop = self._list.size() if stop is None else stop
        for index, node in enumerate(self._list):
            if index >= start and index < stop:
                if value == node.value:
                    return index
        raise ValueError

    def __contains__(self, value: object) -> bool:
        return bool(self.count(value))

    def __iter__(self) -> ty.Iterator[_T]:
        return map(lambda node: node.value, iter(self._list))

    def __len__(self) -> int:
        return self._list.size()
