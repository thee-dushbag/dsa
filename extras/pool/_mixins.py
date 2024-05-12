from .abc import BitPoolABC as _Pool
import typing as ty, functools


class UsedSizeABCMixin:
    "Deps: size, used"
    if ty.TYPE_CHECKING:
        # Used by other Mixins to represent
        # an object with properties size and used
        @property
        def size(self) -> int: ...

        @property
        def used(self) -> int: ...


class StrReprMixin(UsedSizeABCMixin):
    "Deps: _to_str, used, size"
    if ty.TYPE_CHECKING:
        # Dependency for this mixin
        def _to_str(self) -> str: ...

    def __str__(self):
        name = self.__class__.__name__
        capacity = self.used / self.size * 100
        return f"{name}(used={self.used}, size={self.size}, {capacity=:.1f}%)"

    def __repr__(self) -> str:
        name = self.__class__.__name__
        capacity = self.used / self.size * 100
        value = self._to_str()
        if len(value) > 13:
            value = f"{value[:5]}...{value[-5:]}"
        return (
            f"<{name}(used={self.used} size={self.size} {capacity=:.3f}% {value=!r})>"
        )


def _index_type_err(index: object) -> ty.NoReturn:
    msg = "Expected index to be int, slice or ty.SupportsIndex but got %s"
    raise TypeError(msg % type(index).__name__)


def _index_to_int(v: object) -> int:
    match v:
        case int():
            return v
        case ty.SupportsIndex():
            return v.__index__()
        case _:
            _index_type_err(v)


def _index_stream(
    indices: ty.Iterable[ty.SupportsIndex | int | slice], size: int
) -> ty.Iterable[int]:
    for index in indices:
        match index:
            case int():
                yield index
            case ty.SupportsIndex():
                yield index.__index__()
            case slice():
                yield from _slice_to_range(index, size)
            case _:
                _index_type_err(index)


def _slice_to_range(s: slice, size: int) -> range:
    if s.start is not None and s.start < 0:
        size = 0
    start = _index_to_int(s.start or 0)
    stop = _index_to_int(s.stop or size)
    step = _index_to_int(s.step or 1)
    return range(start, stop, step)


def _value_stream(value: object) -> ty.Iterable[bool]:
    if isinstance(value, ty.Iterable):
        return map(bool, value)
    from itertools import repeat

    return repeat(bool(value))


@functools.total_ordering
class BitPoolPyAPIMixin(UsedSizeABCMixin):
    "Deps: size, used, read_bits, read_bits, read_bit, write_bits, write_bit"

    if ty.TYPE_CHECKING:
        # Dependencies for this mixin
        # For the syntactic analysis
        def read_bit(self, index: int) -> bool: ...
        def read_bits(self, indices: ty.Iterable[int]) -> ty.Iterator[bool]: ...
        def write_bit(self, index: int, value: bool) -> None: ...
        def write_bits(self, indices: ty.Iterable[tuple[int, bool]]) -> None: ...

    def __invert__(self) -> ty.Iterator[bool]:
        return (not b for b in self)

    def __iter__(self) -> ty.Iterator[bool]:
        return self.read_bits(range(self.size))

    def __reversed__(self) -> ty.Iterator[bool]:
        return self.read_bits(range(-1, -self.size - 1, -1))

    def __pos__(self) -> int:
        return self.used

    def __neg__(self) -> int:
        return self.size - self.used

    def __len__(self) -> int:
        return self.size

    def __eq(self, other: _Pool) -> bool:
        return self.size == other.size and all(map(lambda a, b: a == b, self, other))

    def __eq__(self, other: object):
        return self.__eq(other) if isinstance(other, _Pool) else NotImplemented

    def __ne__(self, other: object):
        return not self.__eq(other) if isinstance(other, _Pool) else NotImplemented

    def __gt__(self, other: object):
        return (self.used > other.used) if isinstance(other, _Pool) else NotImplemented

    def __getitem__(self, index):
        match index:
            case int():
                return self.read_bit(index)
            case ty.SupportsIndex():
                return self.read_bit(index.__index__())
            case slice():
                return self.read_bits(_slice_to_range(index, self.size))
            case _:
                if isinstance(index, ty.Iterable):
                    return self.read_bits(_index_stream(index, self.size))
                _index_type_err(index)

    def __setitem__(self, index, value):
        match index:
            case int():
                self.write_bit(index, bool(value))
            case ty.SupportsIndex():
                index = index.__index__()
                self.write_bit(index, bool(value))
            case slice():
                self.write_bits(
                    zip(_slice_to_range(index, self.size), _value_stream(value))
                )
            case _:
                if isinstance(index, ty.Iterable):
                    return self.write_bits(
                        zip(_index_stream(index, self.size), _value_stream(value))
                    )
                _index_type_err(index)


class ValidIndexMixin(UsedSizeABCMixin):
    "Deps: size"

    def _valid_index(self, index: int) -> int:
        if -self.size <= index < self.size:
            return index % self.size
        msg = "Out of range [-%r,%r), got %r"
        raise IndexError(msg % (self.size, self.size, index))


class SizedMixin:
    "Deps: _size"
    # Subclass has to set this as
    # an attribute of the instance
    # The Bitpool's size stored by
    # the subclass
    _size: int

    @property
    def size(self) -> int:
        return self._size


class BitPoolMixin(BitPoolPyAPIMixin, SizedMixin, ValidIndexMixin, StrReprMixin): ...
