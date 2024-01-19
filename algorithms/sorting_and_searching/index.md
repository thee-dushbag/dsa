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

### Insertion sort

### Merge sort

### Quick sort

### Heap sort

### Bubble sort

This algorithm sorts an array by bubbling up a value to its correct position. It does this for all items in the array leading to `size * size` comparisons. This does not scale very well for large arrays.

## Analysis

| Algorithm     | Big-O     |
| ------------- | --------- |
| Binary Search | O(log(n)) |
| Simple Search | O(n)      |
| Bubble Sort   | O(n^2)    |
