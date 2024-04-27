import typing as ty

__all__ = ("hash", "Hashable")

Hashable = bytes | bytearray | memoryview | str | int | float | complex | bool


def _to_bytes(value: int) -> bytes:
    "A much better, faster and perfomant int byte-izer."
    return value.to_bytes(value.bit_length() // 8 + 1, signed=True)


def hash(value: Hashable, clamp: int | None = None, shift: int | None = None) -> int:
    """
    This is a parametric hash function, this means by tuning
    the input values `clamp` and `shift` it can yield
    wildly different hash values hence can be used where
    multiple hash functions are needed like in a bloom filter.

    Remember, this is just a simple function so that I don't
    have to create multiple hash functions to use in the bloom
    filter which means there are some major drawbacks to this
    algorithm, for example, a huge shift and small clamp values
    may render this function slow, errorneous and very
    predictable (theoretically). Gets slower as the `value`
    size gets larger; long strings/bytes.

    It can produce different values depending on the type of
    data; hash(b'Hey') != hash('Hey'), hash(-90) != hash(90),
    hash(1) != hash(1.0) != hash(1 + 0j).
    """
    shift = 8 if shift is None else shift
    clamp = (1 << ((clamp or 64) + shift)) - 1
    hash_value = 7919
    if not isinstance(value, Hashable):
        msg = "Unhashable type, %r of type %s"
        raise TypeError(msg % (value, type(value).__name__))
    if isinstance(value, int):
        # prevent the generator from being
        # unwrapped by bytes. cast it to bytes
        # to make the type checker happy and
        # still make `value` an integer iterable
        # the intergers yielded are all in [0, 255]
        value = _to_bytes(value)
        hash_value *= 892189
    elif isinstance(value, float):
        from itertools import chain

        ratio = map(_to_bytes, value.as_integer_ratio())
        value = ty.cast(bytes, chain.from_iterable(ratio))
        hash_value *= 688951
    elif isinstance(value, complex):
        from itertools import chain

        iratio = map(_to_bytes, value.imag.as_integer_ratio())
        rratio = map(_to_bytes, value.real.as_integer_ratio())
        ratio = chain(chain(rratio), chain(iratio))
        value = ty.cast(bytes, ratio)
        hash_value *= 134867
    elif isinstance(value, str):
        value = value.encode()
        hash_value *= 744377
    else:
        hash_value *= 324673
    total = 1
    for byte in value:
        total = (total * byte ** (byte // (shift + 1))) & clamp
        hash_value <<= shift
        hash_value ^= ((total << shift) | byte) * byte
        hash_value ^= byte**shift * 362717 * (byte ^ 82757**shift)
        hash_value ^= (hash_value >> shift) * 403133 * shift**byte
        hash_value ^= ((byte << shift) ^ 570373**byte) ^ 570461 ** (byte + shift)
        hash_value ^= ((total * byte) ** shift) & (hash_value >> shift)
        hash_value ^= (byte**shift ^ (821297 // (byte + 1))) * total
        hash_value &= clamp
    return (hash_value + (total * shift)) & (clamp >> shift)
