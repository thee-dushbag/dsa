# Greedy Algorithms.

Greedy algorithms are algorithms that pick the best local decision while solving a problem.

They oftenly produce optimal, if not best, solutions; which is their selling point as they are fast.

Some of the well know greedy algorithms are:
- [Huffman codes algorithm](./huffman.py) - it is a compression algorithm that tries to assign less bits to most frequent charcters hence reducing the size of the input string considerably. It is generally fast and a high compression rate for huge input strings with significantly few unique characters. Example, the string `"aaaaaaaabbbb"` occupies 12 bytes (96 bits), when compressed it reduces to 1.5 bytes (12 bits); here a `0` represents `a` and `1` represents `b`, therefore the output is the bit sequence `000000001111`, this is an `87.5%` size reduction.
