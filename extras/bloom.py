"""
Bloom filters are a variant of hash tables
with a twist, they occupy way less space and
are super fast but unfortunately, they are
probabilistic. This means if a bloom says it
has no value then the value is definately not
there but when it says there is, then the value
there may or may not be in the bloom.

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

import functools
import operator
import typing as ty

Hashable = str | bytes | int


def flags_ison(mask: int, flag: int, /) -> bool:
    return mask & flag == flag


def my_hash_function(
    value: Hashable, clamp: int | None = None, shift: int | None = None
) -> int:
    """
    Use clamp and shift parameters to tune the hash_value
    so that it is random and therefore the hash_function
    may produce different hash values which may emulate
    different hash functions.

    Remember, this is just a simple function so that I don't
    have to create multiple hash functions to use in the bloom
    filter which means there are some major drawbacks to this
    algorithm, for example, a huge shift and small clamp values
    may render this function slow, errorneous and very
    predictable.

    It can produce different values depending on the type of
    data; hash(b'Hey') != hash('Hey'). Hashing integers is the
    simplest and straight forward.
    """
    shift = 8 if shift is None else shift
    clamp = (1 << ((clamp or 64) + shift)) - 1
    hash_value = 688951
    if isinstance(value, int):
        return (value ^ hash_value * shift) & (clamp >> shift)
    if isinstance(value, str):
        value = value.encode()
        hash_value = 744377 * hash_value
    assert isinstance(value, bytes), "Expected value to be an int, bytes or str object."
    for byte in value:
        hash_value <<= shift
        hash_value ^= byte**shift * 362717 * (byte ^ 82757**shift)
        hash_value ^= (hash_value >> shift) * 403133 * byte
        hash_value ^= ((byte << shift) & 570373**byte) ^ 570461 ** (byte + shift)
        hash_value ^= byte * 821297
        hash_value &= clamp
    return hash_value & (clamp >> shift)


def bit_hashes(bit_count: int, *clamp_shift: tuple[int, int]):
    """
    Create `len(clamps)` hash_functions to
    randomize the bit_hashes, they produce
    a hash_value that has a bit_count equal
    or less than `bit_count`
    """

    def hash_function(value: Hashable) -> int:
        hashes = (my_hash_function(value, clamp, shift) for clamp, shift in clamp_shift)
        bits = (1 << (h % bit_count) for h in hashes)
        return functools.reduce(operator.or_, bits)

    return hash_function


class BloomFilter:
    """
    Store data in a small amount of space.
    You can tune this structure as you wish
    but the most important setting is `bit_count`
    which controls the capacity of the bloom filter.
    An integer with bits `bit_count` on is the
    highest bloom value it can go.
    """

    __slots__ = "_hash_function", "__bit_count", "_bloom_value"
    # Some random clamps and shifts, these will produce a hash function
    # that produces an interger that has only 3 bits set which should
    # produce less collisions and hopefully spread out values.
    clamp_shifts: tuple[tuple[int, int], ...] = (501, 3), (873, 5), (773, 7)

    def __init__(
        self, bit_count: int | None = None, *clamp_shifts: tuple[int, int]
    ) -> None:
        """
        `bit_count`    - max number of bits the bloom value the bloom can hold. Default 256
        `clamp_shifts` - though there is a sensible default, you can alter
                      it to get more randomness from the my_hash_function function.
                      it is a tuple of two integers (clamp, shift).
        Do not alter the protected instance variables, it might break the blooms
        functionality. That is `_hash_funtion`, `__bit_count` and `_bloom_value`.
        """
        if not clamp_shifts:
            clamp_shifts = self.clamp_shifts
        if bit_count is None:
            bit_count = 256
        if not isinstance(bit_count, int):
            raise TypeError(f"bit_count must be an integer")
        if bit_count <= 0:
            raise ValueError(f"bit_count cannot be negative or zero")
        self._hash_function = bit_hashes(bit_count, *clamp_shifts)
        self.__bit_count = bit_count
        self._bloom_value = 0

    @property
    def bit_count(self) -> int:
        return self.__bit_count

    def add(self, value: Hashable):
        self._bloom_value |= self._hash_function(value)

    def extend(self, values: ty.Iterable[Hashable], /):
        hashes = map(self._hash_function, values)
        self._bloom_value |= functools.reduce(operator.or_, hashes)

    def has(self, value: Hashable) -> bool:
        return flags_ison(self._bloom_value, self._hash_function(value))

    def __contains__(self, value: Hashable) -> bool:
        return self.has(value)

    def __str__(self) -> str:
        value = str(self._bloom_value)
        used = self._bloom_value.bit_count()
        if len(value) > 11:
            value = f"{value[:4]}...{value[-4:]}"
        return f"BloomFilter({value}, {used=} bits={self.__bit_count})"

    def __repr__(self) -> str:
        used = self._bloom_value.bit_count()
        capacity = (used / self.__bit_count) * 100
        value = str(self._bloom_value)
        if len(value) > 11:
            value = f"{value[:4]}...{value[-4:]}"
        return (
            f"<BloomFilter on={used} bits={self.__bit_count} "
            f"capacity={capacity:.2f}% value={value}>"
        )
