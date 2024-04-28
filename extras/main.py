import pytest
from pool import BitPool


def _test_bit_pool(pool: BitPool):
    from itertools import chain

    mid = pool.size // 2

    # Set all bits to 0
    pool.write_bits(map(lambda i: (i, False), range(0, pool.size)))
    assert pool.used == 0
    assert not pool.read_bit(mid)
    # Set middle bit to 1
    pool.flip_bit(mid)
    assert pool.used == 1
    assert pool.read_bit(mid)
    # Flipping all bits leaves the middle bit to 0 and the rest to 1
    assert not all(pool.flip_bits(range(0, pool.size)))
    # All bits except the middle one, [0,mid)U(mid,pool.size], should be 1
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

    # flip the first half bits from 1 to 0
    pool.write_zeros(range(0, mid))
    # confirm that all are now 0
    assert not any(pool.read_bits(range(0, pool.size)))
    # flip all bits to 1 from 0
    pool.write_ones(range(0, pool.size))
    # confirm all are 1
    assert all(pool.read_bits(range(0, pool.size)))

    # check invalid indices access throw errors appropriately
    with pytest.raises(IndexError):
        pool.read_bit(pool.size + 1)
    with pytest.raises(IndexError):
        pool.write_bit(-pool.size - 1, False)


def test_integer_bitpool():
    from pool import IntegerBitPool

    for size in map(lambda i: i * 100, range(1, 5)):
        _test_bit_pool(IntegerBitPool(size))


def test_bytes_bitpool():
    from pool import BytesBitPool

    for size in map(lambda i: i * 100, range(1, 5)):
        _test_bit_pool(BytesBitPool(size))


def test_bloom_filter():
    from bloom import BloomFilter
    from pool import IntegerBitPool
    # Use my hasher implementation due to
    # extreme randomness and produces very
    # bid numbers which work very well with
    # this test but it is slow so small
    # input lenths will be considered
    from mhash import my_hasher as hasher

    # Make sure it is big enough to run our
    # test, 2048 bits should be enough
    pool = IntegerBitPool(2048)
    bloom = BloomFilter(pool, hasher)
    data = (*range(10, 20), "Simon", "Nganga", "NGANGA", "nganga", "simon.")
    others = ("SIMON", "Njoroge", "Nganga.", " NGANGA", "simon", *range(20, 30))
    bloom.extend(data)  # Insert all inputs into our bloom filter
    assert all(bloom.has(d) for d in data), repr(bloom)
    assert not any(bloom.has(d) for d in others), repr(bloom)
