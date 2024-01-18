import typing as ty


class _sentinel:
    def __bool__(self):
        return False

    def __str__(self) -> str:
        return "<none>"

    __repr__ = __str__


NONE = _sentinel
sentinel = NONE()
T = ty.TypeVar("T")
Optional = ty.Union[NONE, T]


def isnone(value: ty.Any) -> bool:
    return isinstance(value, NONE)


class Bucket(ty.Generic[T]):
    def __init__(self, value: Optional[T] = sentinel) -> None:
        self.value: Optional[T] = value

    def __str__(self) -> str:
        return f"Slot({self.value!r})"

    __repr__ = __str__


class Array(ty.Generic[T]):
    def __init__(self, size: int) -> None:
        assert isinstance(
            size, int
        ), f"Expected array size to be an integer, got {size}"
        if size < 0:
            raise IndexError("Array cannot have a negative size.")
        self._size = size
        self._buckets: list[Bucket[T]] = [Bucket() for _ in range(size)]

    def __setitem__(self, index: int, value: Optional[T]):
        self._buckets[index].value = value

    def __getitem__(self, index: int) -> Optional[T]:
        return self._buckets[index].value

    def __iter__(self):
        for index in range(self._size):
            yield self._buckets[index].value

    def __len__(self) -> int:
        return self._size

    def __str__(self) -> str:
        return f"Array({self._buckets})"

    isnone = staticmethod(isnone)

    def __reversed__(self):
        for index in range(self._size - 1, -1, -1):
            yield self._buckets[index].value
