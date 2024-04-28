"""
Bloom filters are a variant of hash tables
with a twist, they occupy way less space and
are super fast but unfortunately, they are
probabilistic. This means if a bloom says it
has no value then the value is definately not
there but when it says there is, then the value
may or may not be in the bloom.

A bloom works by using some integer types bits
and bit operations to mark the presence or absence
of a value. To insert a value, hash it and
mod by the total number of bits in the integer
then activate the bit that corresponds to that
mod result. You can notice that multiple
values may activate the same bit hence if the bit
is on, it may mean some multiple values are in but
if it is off, then all values that activate that
bit were definately not added.

Bloom filters are perfect for caching data.
Before going on to start some heavy processing
to calculate a value, you can simply see if the
bloom has already seen it and therefore don't need
to embark on the processing journey.
"""

import typing as ty
import pool
import mhash


def bit_hashes(
    hasher: mhash.Hasher | None,
    clamp_shifts: tuple[tuple[int, int], ...],
):
    """
    Create a hash function that turns on N bits
    at indices streamed by the hash function returned.
    N is equal to `len(clamp_shifts) + 1`.
    """

    def hash_function(
        value: mhash.Hashable, bit_count: int
    ) -> ty.Generator[int, None, None]:
        hashes = (
            mhash.hash(value, clamp, shift, hasher=hasher)
            for clamp, shift in clamp_shifts
        )
        return (h % bit_count for h in hashes)

    return hash_function


class BloomFilterABC(ty.Protocol):
    def extend(self, values: ty.Iterable[mhash.Hashable]): ...
    def add(self, value: mhash.Hashable): ...
    def has(self, value: mhash.Hashable) -> bool: ...
    @property
    def pool(self) -> pool.BitPool: ...
    @property
    def max_markers(self) -> int: ...
    @property
    def bit_count(self) -> int: ...
    @property
    def size_hint(self) -> int: ...
    def __contains__(self, value: mhash.Hashable) -> bool: ...
    def __len__(self) -> int: ...


class BloomFilter(BloomFilterABC):
    clamp_shifts: tuple[tuple[int, int], ...] = (103, 11), (151, 7), (211, 3)

    def __init__(
        self,
        pool: pool.BitPool,
        hasher: mhash.Hasher | None = None,
        clamp_shifts: tuple[tuple[int, int], ...] | None = None,
    ) -> None:
        self._pool = pool
        if clamp_shifts is None:
            clamp_shifts = self.clamp_shifts
        assert clamp_shifts, 'Must provide atleast one clamp_shift pair'
        self._bit_hash = bit_hashes(hasher, clamp_shifts)
        self._max_markers = len(clamp_shifts)
        self._size_hint = 0

    def _hash(self, value: mhash.Hashable) -> ty.Iterable[int]:
        return self._bit_hash(value, self._pool.size)

    @property
    def pool(self) -> pool.BitPool:
        return self._pool

    @property
    def size_hint(self) -> int:
        return self._size_hint

    @property
    def max_markers(self) -> int:
        return self._max_markers

    @property
    def bit_count(self) -> int:
        return self._pool.size

    def _has(self, hash_value: ty.Iterable[int]) -> bool:
        return all(self._pool.read_bits(hash_value))

    def add(self, value: mhash.Hashable):
        from itertools import tee

        h1, h2 = tee(self._hash(value))
        self._size_hint += not self._has(h1)
        self._pool.write_bits(map(lambda i: (i, True), h2))

    def extend(self, values: ty.Iterable[mhash.Hashable]):
        from itertools import chain, tee

        def _hash(value: mhash.Hashable):
            h1, h2 = tee(self._hash(value))
            self._size_hint += not self._has(h1)
            return h2

        indices = chain.from_iterable(map(_hash, values))
        self._pool.write_bits(map(lambda i: (i, True), indices))

    def has(self, value: mhash.Hashable) -> bool:
        return self._has(self._hash(value))

    def __len__(self) -> int:
        return self._size_hint

    __contains__ = has

    def __str__(self) -> str:
        return f"BloomFilter(pool={self._pool!s}, size_hint={self._size_hint})"

    def __repr__(self) -> str:
        return f"<BloomFilter(pool={self._pool!r}, size={self._size_hint}, markers={self._max_markers})>"
