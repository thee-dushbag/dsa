import typing as ty

__all__ = ("hash", "Hashable")

Hashable = bytes | bytearray | memoryview | str | int | float | complex | bool
Hasher = ty.Callable[[ty.Iterable[int], int, int, int], int]


def _to_bytes(value: int) -> bytes:
    "A much better, faster and perfomant int byte-izer."
    return value.to_bytes(value.bit_length() // 8 + 1, signed=True)


def mmh3_hasher(value: ty.Iterable[int], seed: int, clamp: int, shift: int) -> int:
    seed *= clamp * shift
    # mypy not finding `mmh3` stub files
    from mmh3 import hash128 # type: ignore

    return hash128(bytes(value), seed=seed)


def py_hasher(value: ty.Iterable[int], seed: int, clamp: int, shift: int):
    import builtins

    seed *= clamp * shift
    return builtins.hash(bytes(value)) * seed


def my_hasher(value: ty.Iterable[int], seed: int, clamp: int, shift: int):
    total = 1
    for byte in value:
        total = (total * byte ** (byte // (shift + 1))) & clamp
        seed <<= shift
        seed ^= ((total << shift) | byte) * byte
        seed ^= byte**shift * 362717 * (byte ^ 82757**shift)
        seed ^= (seed >> shift) * 403133 * shift**byte
        seed ^= ((byte << shift) ^ 570373**byte) ^ 570461 ** (byte + shift)
        seed ^= ((total * byte) ** shift) & (seed >> shift)
        seed ^= (byte**shift ^ (821297 // (byte + 1))) * total
        seed = (seed >> shift) & clamp
    return seed + total


def _default_hasher() -> Hasher:
    """
    Check if mmh3 is installed.
    If so, prefer mmh3 hasher to py hasher.
    These two are faster than my hasher.
    """
    try:
        import mmh3
    except ImportError:
        return py_hasher
    else:
        return mmh3_hasher


def hash(
    value: Hashable,
    clamp: int | None = None,
    shift: int | None = None,
    hasher: Hasher | None = None,
) -> int:
    """
    This is a parametric hash function, this means by tuning
    the input values `clamp` and `shift` it can yield
    wildly different hash values hence can be used where
    multiple hash functions are needed like in a bloom filter.

    It can produce different values depending on the type of
    data; hash(b'Hey') != hash('Hey'), hash(-90) != hash(90),
    hash(1) != hash(1.0) != hash(1 + 0j).
    """
    hasher = _default_hasher() if hasher is None else hasher
    shift = 8 if shift is None else shift
    clamp = (1 << ((clamp or 64) + shift)) - 1
    bytes_seq: ty.Iterable[int]
    hash_value = 7919

    match value:
        case int() | bool():
            bytes_seq = _to_bytes(value)
            hash_value *= 892189
        case float():
            from itertools import chain

            ratio = map(_to_bytes, value.as_integer_ratio())
            bytes_seq = chain.from_iterable(ratio)
            hash_value *= 688951
        case complex():
            from itertools import chain

            comps = value.real, value.imag
            ratios = map(lambda f: f.as_integer_ratio(), comps)
            stream = chain.from_iterable(ratios)
            bytes_seq = chain.from_iterable(map(_to_bytes, stream))
            hash_value *= 134867
        case str():
            bytes_seq = value.encode()
            hash_value *= 744377
        case bytes() | memoryview() | bytearray():
            bytes_seq = value
            hash_value *= 324673
        case _:
            msg = "Unhashable type, %r of type %s"
            raise TypeError(msg % (value, type(value).__name__))

    hash_value = hasher(bytes_seq, hash_value, clamp, shift)
    return (hash_value + (clamp * shift)) & (clamp >> shift)
