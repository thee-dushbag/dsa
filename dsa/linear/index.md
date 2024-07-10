# Linear Data Structures.

## Introduction.

In linear data structures, the elements are arranged in sequence one after the other.
There are multiple linear data structures, they are.

- [Queue](#queue)
- [Array](#array)
- [Linked List](#linked-list)
- [Heap](#heap)
- [Set](#set)
- [Hash Table](#hash-table)
- [Fibbonacci Heap](#fibbonacci-heap)

### Queue

The queue is a data structure that has two operations, `push` and `pop`.  
It is also known as `FIFOQueue` because the first element in is the first out.
`push` at the back and `pop` at the front.

#### Stack

It is a type of queue where the last element in is the last out. Also known as the `LIFOQueue`

#### Priority Queue

It is a type of queue where the element with the highest priority is
the first out, it is implemented using the heap data structure with the heappush operation
always ensuring the highest priority is the root element in which the `pop` operation
can easily access and remove hence first out.

#### Deque

Also a variant of the Queue with a few additions where you can `push` and `pop` on
either side of the Queue. It is implemented using the circular doubly linked list data
structure due to its fast insertion and deletions at the front and back.

###### Implementations

- [**Python**](./queue.py)

### Array

An Array in C/C++ is represented as a block of memory divided into slots by the size of the type to be stored in them. Arrays have O(0) insertion and deletion. The size remains the same from construction to destruction.  
An Implementation in python will be more helpful than in c/c++ due to the extreme ease to create there.

###### Implementations

- [**Python**](./array.py)

### Linked List

![Linked list Picture][linked_list_picture]

A linked list is a linear data structure that includes a series of connected nodes. Here, each node stores the data and the address/reference of the next/previous node.
Each node holds a value and the address/reference of the next/previous node

###### Types os linked list.

- Singly Linked list.
- Doubly Linked list.
- Circular Doubly Linked list.

###### Operations

- insertion - insert an element at a specified index.
- deletion - delete an element at a certain index.
- get an element - get an element at a specified index.

**NOTE:** `index` as used in this section means the `nth` node in the linked list where `n = index`.

###### Analysis

| Operation | Worst Case |
| --------- | ---------- |
| Insertion | **O(1)**   |
| Deletion  | **O(1)**   |
| GetIndex  | **O(n)**   |

If an node in the list has already been found, deleting it from the list takes constant time as well as inserting a new node, while getting a node at a specified index, at worst case, has to traverse the whole list to get to the node.

###### Implementations

- [**Python**](./linked_list/__init__.py) - only implemented the doubly and singly linked list.

### Heap

![Heap Data Structure][heap_picture]

Heap data structure is a complete binary tree that satisfies the heap property, where any given node is

- always greater than its child node/s and the key of the root node is the largest among all other nodes. This property is also called max heap property.
- always smaller than the child node/s and the key of the root node is the smallest among all other nodes. This property is also called min heap property.

My implementations are a bit extended from the basic heap we know of, ontop of the two types, I added the mineq-heap and maxeq-heap. They differ from the normal min-heap and max-heap in that, if two values in the heap are equal, in my implementation, they are switched therefore the newest values will be popped first in the heappop operation therefore they portray a stack like container unlike the formers that behave like queues.

###### Operations

Operations that can be done on a heap include:

- heapify the heap, convert an ordinary array to a heap
- remove an item from the heap, (ie heappop if removing the first element)
- add an item to the heap

###### Analysis

###### Implementations

- [**Python**](./heap.py)

### Set

A set is a data structure that stores data in a way that can be accessed in contant time.
Unlike a list or other collections, it cannot store duplicates. It uses hashing to know where to store and find a value in the array it uses as the container. By hashing a value to some unique hash value, an integer, we can compute the appropriate index where the value should go or can be found if it is in the set.
In the case of collisions, we can create a linked list on the slot where the collision happened and chain the values there, allocate more space in the array if this list grows too long.

###### Analysis

###### Implementations

- [**Python**](./set.py)

### Hash Table

This is pretty similar to the set except that, instead of hashing the value, we hash some key that produces an index where we can store the value. With this, we get an association of the key to a value. With some key, you can lookup a value in the hash table.

###### Analysis

###### Implementations

- [**Python**](./hash_table.py)

### Fibbonacci Heap

[linked_list_picture]: /assets/linked-list-dsa-picture.jpg
[heap_picture]: /assets/heap-dsa-picture.jpg
