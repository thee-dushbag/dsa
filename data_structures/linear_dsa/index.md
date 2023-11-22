# Linear Data Structures.

## Introduction.
In linear data structures, the elements are arranged in sequence one after the other.
There are multiple linear data structures, they are.

- [Queue](#queue)
- [Array](#array)
- [Stack](#stack)
- [Linked List](#linked-list)
- [Hash Table](#hash-table)
- [Heap](#heap)
- [Fibbonacci Heap](#fibbonacci-heap)

### Queue
### Array
### Stack
### Linked List
### Hash Table
### Heap
![Heap Data Structure](/assets/heap-dsa-picture.jpg)

Heap data structure is a complete binary tree that satisfies the heap property, where any given node is
- always greater than its child node/s and the key of the root node is the largest among all other nodes. This property is also called max heap property.
- always smaller than the child node/s and the key of the root node is the smallest among all other nodes. This property is also called min heap property.

My implementations are a bit extended from the basic heap we know of, ontop of the two types, I added the mineq-heap and maxeq-heap. They differ from the normal min-heap and max-heap in that, if two values in the heap are equal, in my implementation, they are switched therefore the newest values will be popped first in the heappop operation therefore they portray a stack like container unlike the formers that behave like queues.

###### Oprations
Operations that can be done on a heap include:
- heapify the heap, convert an ordinary array to a heap
- remove an item from the heap, (ie heappop if removing the first element)
- add an item to the heap
###### Analysis
###### Implementations
- [__Python__](./ldsa/heap.py)
### Fibbonacci Heap