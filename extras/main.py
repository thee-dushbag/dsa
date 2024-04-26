def test_bit_hashes():
    from bloom import bit_hashes

    mhash = bit_hashes((67, 3), (90, 5), (123, 8))
    data = range(1000, 3000)
    assert all(map(lambda h: mhash(h, 64).bit_count() <= 3, map(str, data)))
    mhash = bit_hashes((67, 3), (32, 7))
    assert all(map(lambda h: mhash(h, 64).bit_count() <= 2, map(str, data)))
    mhash = bit_hashes((29, 11))
    assert all(map(lambda h: mhash(h, 64).bit_count() <= 1, map(str, data)))


def test_bloom_filter():
    from bloom import BloomFilter

    # Make sure it is big enough to run our
    # test, 2048 bits should be enough
    bloom = BloomFilter(2048)
    data = (*range(10, 20), "Simon", "Nganga", "NGANGA", "nganga", "simon.")
    others = ("SIMON", "Njoroge", "Nganga.", " NGANGA", "simon", *range(20, 30))
    bloom.extend(data)  # Insert all inputs into our bloom filter
    assert all(bloom.has(d) for d in data), repr(bloom)
    # Assuming everything went well, the configuration
    # is correct and also that our test is small enough,
    # we really don't have to worry about any bit collisions.
    # Therefore, the values in `others` should not mark
    # as contained in the bloom filter.
    # NOTE: This is not reliable.
    # for d in others:
    #     if bloom.has(d):
    #         print("FalseAlarm: %r" % d)
    assert not any(bloom.has(d) for d in others), repr(bloom)
