# Extras

![ExtrasPicture][extras_picture]

## Introduction.

In here, you will find algorithms that are either very advanced or are heavily math oriented. They could involve mathematical functions to generate prime numbers or experimenting with encryption/decryption, if I come across such algorithms.

## Contents

- [Bloom Filter](#bloom-filter)

### Bloom Filter

A bloom filter functions very much like a set with a catch, it occupies so little space. The idea is that you have a bit pool (integer or some allocated memory block) with some of some size N. At the start, the bloom filter bit pool is all set to zero's, to add a value you hash the value and mod by N to get M, M acts like an index in the bit pool, set the Mth bit in the bit pool to one.

Here is the amazing part, to check if a value is in the bloom, check if the corresponding bit is set. Since multiple values can mod to the same Mth bit this means that if the bit is set then their is a possibility for the value to have been added. If the Mth bit is off then the value was definately not added.

With this, we can conclude that the bloom filter is probabilistic and that the size of the bloom is the same as the bit pool (a basic version would use a 64 bit interger) which most of the time is way less compared to the cumulative size of values at hand.

Bloom filters work best as somekind of caching system (example reduce confirmation requests sent over the network to confirm if something is present, you can simply cache them in the bloom then issue a request when the bloom says it might have seen the value before). With this kind of power comes a great decision to be made; bit pool size and hash marker count.

To increase Performance and capacity, choose a big bit pool size and 3 to 5 hash functions. A big pool of bits can store more values and multiple hash functions can make false positives rarer.

Let C be the ratio between the number of bits that are on in the bit pool to the total number of bits in the pool. As C approaches 1, the bloom filter approaches uselessness. When C is equal to 1, the filter is totally useless.

#### Implementation

- [Python](./bloom.py)

#### Analysis

[extras_picture]: /assets/extras-intro-picture.jpg
