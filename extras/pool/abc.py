import typing as ty


@ty.runtime_checkable
class BitPoolABC(ty.Protocol):
    "Represents a container of bits."
    # Core functionality for a BitPool

    def flip_bit(self, index: int) -> bool:
        "Flip the bit at `index`"
        ...

    def flip_bits(self, indices: ty.Iterable[int]) -> list[bool]:
        """
        For each index `i` in `indices`, flip bit at `i`.
        """
        ...

    def read_bit(self, index: int) -> bool:
        "Get the value of the bit at `index`"
        ...

    def read_bits(self, indices: ty.Iterable[int]) -> ty.Iterator[bool]:
        """
        Can be lazy, expand to get instant bit values or be sure
        the pool will not be altered as you read the bit values.
        """
        ...

    def write_bit(self, index: int, value: bool) -> None:
        "Set bit at `index` to `value`"
        ...

    def write_bits(self, indices: ty.Iterable[tuple[int, bool]]) -> None:
        "Set the bit at index `i` with value `v` for all (`i`, `v`) in `indices`"
        ...

    @property
    def used(self) -> int:
        """
        The number of bits that are `1`.
        Use `self.size - self.used` to get
        the number of bits that are `0`
        """
        ...

    @property
    def size(self) -> int:
        """
        Returns the total number of bits in the self.
        """
        ...

    # For the ones below, inherit them from
    # the `_mixins.BitPoolPyAPIMixin` class which
    # implements each and every one of these.
    # They are mainly to lessen typing when
    # using the bitpool; they are all syntactic
    # sugar for the core API.

    # BitPool Comparators

    def __eq__(self, other: object) -> bool:
        """
        `self.size == other.size and all(map(lambda a, b: a and b, zip(self.read_bits(self.size), other.read_bits(other.size))))`
        """
        ...

    def __ne__(self, other: object) -> bool:
        "`not (self == other)`"
        ...

    def __gt__(self, other: object) -> bool:
        "`self.used > other.used`"
        ...

    def __lt__(self, other: object) -> bool:
        "`self.used < other.used`"
        ...

    def __ge__(self, other: object) -> bool:
        "`self.used >= other.used`"
        ...

    def __le__(self, other: object) -> bool:
        "`self.used <= other.used`"
        ...

    # Sugarcoats to the BitPool core API

    def __len__(self) -> int:
        """
        `self.size`
        """
        ...

    def __iter__(self) -> ty.Iterator[bool]:
        """
        `self.read_bits(range(self.size))`
        """
        ...

    def __reversed__(self) -> ty.Iterator[bool]:
        """
        `self.read_bits(range(-1, -self.size - 1, -1))`
        """
        ...

    def __pos__(self) -> int:
        """
        Returns number of bits that are `1`.
        `self.used`
        """
        ...

    def __neg__(self) -> int:
        """
        Returns number of bits that are `0`.
        `self.size - self.used`
        """
        ...

    def __invert__(self) -> ty.Iterable[bool]:
        """
        `map(lambda v: not v, self.read_bits(range(self.size)))`
        """
        ...

    @ty.overload
    def __getitem__(self, index: int) -> bool:
        """
        `self.read_bit(index)`
        """
        ...

    @ty.overload
    def __getitem__(self, index: ty.SupportsIndex) -> bool:
        """
        `self.read_bit(index.__index__())`
        """

    @ty.overload
    def __getitem__(self, indices: slice) -> ty.Iterable[bool]:
        """
        `self.read_bits(range(indices.start or 0, indices.stop or self.size, indices.step or 1))`
        """
        ...

    @ty.overload
    def __getitem__(
        self, indices: ty.Iterable[int | ty.SupportsIndex | slice]
    ) -> ty.Iterable[bool]:
        """
        `self.read_bits(indices)`
        `self.read_bits(map(lambda i: i.__index__(), indices))`
        `self.read_bits(chain.from_iterable(map(lambda s: range(s.start, s.stop, s.step), indices)))`
        """
        ...

    @ty.overload
    def __setitem__(self, index: int, value: object) -> None:
        """
        `self.write_bit(index, bool(value))`
        """
        ...

    @ty.overload
    def __setitem__(self, index: ty.SupportsIndex, value: object) -> None:
        """
        `self.write_bit(index.__index__(), bool(value))`
        """
        ...

    @ty.overload
    def __setitem__(self, indices: slice, values: ty.Iterable[object]) -> None:
        """
        `self.write_bits(zip(range(indices.start, indices.stop, indices.step), map(bool, values)))`
        """
        ...

    @ty.overload
    def __setitem__(self, indices: slice, value: object) -> None:
        """
        `self.write_bits(map(lambda i: (i, bool(value)), range(indices.start, indices.stop, indices.step)))`
        """
        ...

    @ty.overload
    def __setitem__(
        self,
        indices: ty.Iterable[int | ty.SupportsIndex | slice],
        values: ty.Iterable[object],
    ) -> None:
        """
        Depending on the type of index, one of these will be used.
        `self.write_bits(zip(indices, map(bool, values)))`
        `self.write_bits(zip(map(lambda i: i.__index__(), indices), map(bool, values)))`
        `self.write_bits(zip(chain.from_iterable(map(lambda s: range(s.start, s.stop, s.step), indices)), map(bool, values)))`
        """
        ...

    @ty.overload
    def __setitem__(
        self, indices: ty.Iterable[int | ty.SupportsIndex | slice], value: object
    ) -> None:
        """
        Depending on the type of index, one of these will be used.
        `self.write_bits(map(lambda i: (i, bool(value)), indices))`
        `self.write_bits(map(lambda i: (i.__index__(), bool(value)), indices))`
        `self.write_bits(map(lambda i: (i, bool(value)), chain.from_iterable(map(lambda s: range(s.start, s.stop, s.step), indices))))`
        """
        ...
