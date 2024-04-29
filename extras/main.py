from pool.abc import BitPoolABC
import pytest, typing as ty


def _test_bit_pool_core_api(pool: BitPoolABC):
    from itertools import chain

    mid = pool.size // 2

    # Set all bits to 0
    pool.write_bits(map(lambda i: (i, False), range(0, pool.size)))
    assert pool.used == 0
    assert not pool.read_bit(mid)
    # Set middle bit to 1
    assert pool.flip_bit(mid)
    assert pool.used == 1
    # Flipping all bits leaves the middle bit to 0 and the rest to 1
    assert not all(pool.flip_bits(range(0, pool.size)))
    # All bits except the middle one, [0,mid)U(mid,pool.size), should be 1
    assert all(pool.read_bits(chain(range(0, mid), range(mid + 1, pool.size))))
    # The middle bit should be 0
    assert not pool.read_bit(mid)
    # Now set the middle bit to 1
    pool.write_bit(mid, True)
    # All bits should be 1 by now, hence all are used
    assert pool.used == pool.size
    # Check if this lines up with the counted 1 bits
    assert all(pool.read_bits(range(0, pool.size)))
    # Test negative indices
    # Set last bit to 0 using size index
    pool.write_bit(pool.size - 1, False)
    # Confirm that the last bit is 0 using -1
    assert not pool.read_bit(-1)
    assert pool.flip_bit(-1)

    # Set the last half of the bits to 0
    assert not any(pool.flip_bits(range(-mid, 0)))
    # Make sure they are all 0's
    assert not any(pool.read_bits(range(mid, pool.size)))

    # check invalid indices access throws error appropriately.
    with pytest.raises(IndexError):
        pool.read_bit(pool.size)
    with pytest.raises(IndexError):
        pool.write_bit(-pool.size - 1, False)


def _test_bit_pool_py_api(pool: BitPoolABC):
    mid = pool.size // 2

    # Set all bits to 0
    pool[:] = False

    assert +pool == 0
    assert -pool == pool.size
    assert not pool[mid]
    pool[mid] = True
    assert pool[mid]

    assert len(pool) == pool.size

    for index in range(pool.size):
        assert pool.read_bit(index) == pool[index]

    assert list(pool) == list(pool.read_bits(range(pool.size)))
    indices = map(lambda i: -i, range(1, pool.size + 1))
    assert list(reversed(pool)) == list(pool.read_bit(i) for i in indices)

    from copy import deepcopy

    new_pool = deepcopy(pool)
    assert new_pool is not pool
    assert new_pool == pool
    new_pool[mid] = not new_pool[mid]
    assert new_pool != pool

    new_pool[:] = True
    assert new_pool > pool and pool < new_pool
    new_pool[:] = pool
    assert new_pool >= pool and pool >= new_pool and new_pool == pool

    for index in range(pool.size):
        new_pool[index] = not pool[index]

    pool[:] = ~pool
    assert pool == new_pool

    assert list(pool[:mid]) == list(reversed(pool))[-mid:]

    from random import shuffle

    indices = list(range(pool.size))
    shuffle(indices)
    assert list(pool[:3]) == list(pool[0, 1, 2])
    assert list(pool[-3:]) == list(pool[-3, -2, -1])

    assert list(pool[*indices, mid, 0:mid, -1, 0, -3:]) == list(
        new_pool.read_bit(i) for i in (*indices, mid, *range(0, mid), -1, 0, -3, -2, -1)
    )

    new_pool[:] = True
    new_pool[:mid] = False
    assert +new_pool == mid
    assert +new_pool + -new_pool == new_pool.size

    new_pool[::2] = False
    new_pool[1::2] = True

    from itertools import cycle

    seq = cycle([False, True])
    assert all(map(lambda a, b: a == b, seq, new_pool))
    pool[:] = cycle([False, True])
    assert new_pool == pool

    quad = pool.size // 4
    values = [next(seq) for _ in range(quad)]
    shuffle(values)
    pool[1 : quad + 1] = values
    assert list(pool[1 : quad + 1]) == values

    new_pool[:] = ~pool

    assert all(map(lambda a, b: a != b, new_pool, pool))

    with pytest.raises(IndexError):
        pool[pool.size]
    with pytest.raises(IndexError):
        pool[-pool.size - 1] = False


def _test_bit_pool(Pool: ty.Callable[[int], BitPoolABC]):
    for size in map(lambda i: i * 100, range(1, 5)):
        pool = Pool(size)
        _test_bit_pool_core_api(pool)
        _test_bit_pool_py_api(pool)


def test_integer_bitpool():
    from pool.int_pool import IntBitPool

    _test_bit_pool(IntBitPool)


def test_bytes_bitpool():
    from pool.bytes_pool import BytesBitPool

    _test_bit_pool(BytesBitPool)


def test_bloom_filter():
    from bloom import BloomFilter
    from pool.int_pool import IntBitPool

    # Use my hasher implementation due to
    # extreme randomness and produces very
    # bid numbers which work very well with
    # this test but it is slow so small
    # input lenths will be considered
    from mhash import my_hasher as hasher

    # Make sure it is big enough to run our
    # test, 2048 bits should be enough
    pool = IntBitPool(2048)
    bloom = BloomFilter(pool, hasher)
    data = (*range(10, 20), "Simon", "Nganga", "NGANGA", "nganga", "simon.")
    others = ("SIMON", "Njoroge", "Nganga.", " NGANGA", "simon", *range(20, 30))
    bloom.extend(data)  # Insert all inputs into our bloom filter
    assert all(bloom.has(d) for d in data), repr(bloom)
    assert not any(bloom.has(d) for d in others), repr(bloom)
