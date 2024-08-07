# Sorting and Searching Algorithms.

Sorting algorithms are used to sort an array of items into ascending or descending orders.
Searching algorithms are used to find items in a given array.

## Sorting algorithms

1. [Selection sort](#selection-sort)
1. [Insertion sort](#insertion-sort)
1. [Merge sort](#merge-sort)
1. [Quick sort](#quick-sort)
1. [Heap sort](#heap-sort)
1. [Bubble sort](#bubble-sort)

## Searching algorithms

1. [Simple search](#simple-search)
1. [Binary search](#binary-search)

## Algorithms

### Simple search

As the name says, this is a simple search algorithm that finds items in given arrays by checking each and every one of them until one is found.

The time taken to find an element grows as the size of the array grows.

### Binary search

It needs the input array to be sorted. It works by dividing the array in two at the middle element, if the item to be found is less than the middle element, then the right half is discarded and the left half becomes the new input array, it does this again until the middle array is the item to be found in which its index or the item itself is returned, or a NotFound/None is returned.

It is pretty fast as the time taken to find an item in the array is logarithmic to the size of the array.

### Selection sort

Start with an empty array and the array to be sorted, take the smallest element from the unsorted array and append it into the sorted array, do this until the unsorted array is empty and you will end up with a sorted array having all elements in descending order.

### Insertion sort

This sorting strategy works by inserting an item in its correct index in a sorted array.
First, you start with an empty array and the array to be sorted. Take an item from the unsorted array and find an index in the sorted array it would be in if it were in the array then in insert it in there.
This involves searching for an appropriate index, using binary search to find the index improves the speed of the algorithm exponentially compared to using linear (simple) search.

### Merge sort

### Quick sort

This sorting algorithm utilizes divide and conquer to sort really fast. First, it selects an item from the input array, probably the middle one, it creates three new arrays A, B and C where A will contain all items less than the chossen item, C all items greater than the chossen and B all equals.
It calls itself again two times with A and C as inputs where the base case for recursion is an array with 1, 0 or 2 elements, it will sort the array with 2 elements before returning it.
The results from input A and C are merged with B as `qsort(A) + B + qsort(C)`, which will result in the elements being sorted as this process is done again for A and C. The final output is a sorted array with all elements in the original array.

### Heap sort

This is a fast algorithm that utilizes heap property to sort a sequence of data. For a `min-heap`, the most minimum element is at the root and popping it off takes `log(n)` steps, which is one of the reasons for its speed. The most expensive operations is heapification of the sequence (`O(n)`), to sort, we just keep popping the most minimum element while adding it to a sorted array. By the end of the operation, you will end up with a sorted array. Hence doing `n` pops each costing `log(n)` to form a total of `nlog(n)`, which is the worst case; `O(nlog(n))`

### Bubble sort

This algorithm sorts an array by bubbling up a value to its correct position. It does this for all items in the array leading to `n * n` comparisons. This does not scale very well for large arrays.

## Analysis

| Algorithm      | Big-O        | Info                |
| -------------- | ------------ | ------------------- |
| Binary Search  | O(log(n))    |                     |
| Simple Search  | O(n)         |                     |
| Bubble Sort    | O(n^2)       |                     |
| Insertion Sort | O(n^2)       | Simple index search |
| Insertion Sort | O(log(n!))   | Binary index search |
| Selection Sort | O(n^2)       |                     |
| Quick Sort     | O(n\*log(n)) |                     |
| Heap Sort      | O(n\*log(n)) |                     |

> It can be proven that `log(n!) < n^2`, hence, `O(log(n!)) < O(n^2)`.
