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

![Linked list Picture][linked_list_picture]

A linked list is a linear data structure that includes a series of connected nodes. Here, each node stores the data and the address/reference of the next/previous node.
Each node holds a value and the address/reference of the next/previous node

###### Types os linked list.
- Singly Linked list.
- Doubly Linked list.
- Circular Singly Linked list.
- Circular Doubly Linked list.

###### Operations
- insertion - insert an element at a specified index.
- deletion - delete an element at a certain index.
- get an element - get an element at a specified index.

**NOTE:** `index` as used in this section means the `nth` node in the linked list where `n = index`.

###### Analysis
| Operation | Worst Case |
| --------- | ---------- |
| Insertion | __O(1)__   |
| Deletion  | __O(1)__   |
| GetIndex  | __O(n)__   |

If an node in the list has already been found, deleting it from the list takes constant time as well as inserting a new node, while getting a node at a specified index, at worst case, has to traverse the whole list to get to the node.

###### Implementations
- [__Python__](./ldsa/linked_list.py) - only implemented the doubly and singly linked list.

### Hash Table
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
- [__Python__](./ldsa/heap.py)
### Fibbonacci Heap

[linked_list_picture]: /assets/linked-list-dsa-picture.jpg
[heap_picture]: /assets/heap-dsa-picture.jpg