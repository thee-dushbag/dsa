# Testing data structures stored in ldsa package.

# Test Heep data structure.
def test_heap_heapify_min():
    import heapq
    from ldsa import heap
    from random import randint
    heap.setheaptype(heap.HeapType.MIN) # Set the global default Heap type
    for size in range(1, 100):
        array = tuple(randint(1, 1000) for _ in range(size))
        mheap, gheap = list(array), list(array)
        heap.heapify(mheap)
        heapq.heapify(gheap) # generates min-heap by default
        assert mheap == gheap

def test_heap_heapify_max():
    import heapq
    from ldsa import heap
    from random import randint
    heap.setheaptype(heap.HeapType.MAX) # Set the global default Heap type
    for _ in range(10):
        array = tuple(randint(1, 1000) for _ in range(100))
        mheap, gheap = list(array), list(array)
        heap.heapify(mheap)
        heapq._heapify_max(gheap)
        assert mheap == gheap

def test_heappush_min():
    import heapq
    from ldsa import heap
    from random import randint
    heap.setheaptype(heap.HeapType.MIN) # Set the global default Heap type
    for _ in range(10):
        array = tuple(randint(1, 1000) for _ in range(100))
        mheap, gheap = list(array[:-1]), list(array[:-1])
        heap.heapify(mheap)
        heapq.heapify(gheap) # generates a min-heap by default
        heap.heappush(mheap, array[-1])
        heapq.heappush(gheap, array[-1])
        assert mheap == gheap

def test_heappop_min():
    import heapq
    from ldsa import heap
    from random import randint
    heap.setheaptype(heap.HeapType.MIN) # Set the global default Heap type
    for size in range(1, 100):
        array = tuple(randint(1, 5) for _ in range(size))
        mheap, gheap = list(array), list(array)
        heap.heapify(mheap)
        heapq.heapify(gheap) # generates a min-heap by default
        heap.heappop(mheap)  # by default, removes the first element
        heapq.heappop(gheap) # Simply removes the element at index 0
        assert mheap == gheap
    custom_test = (12, 16, 47, 30, 34, 50, 48, 43, 46, 38) # Note: Min-Heap
    input_heap, target_index = list(custom_test), 1
    expected_output = [12, 30, 47, 38, 34, 50, 48, 43, 46]
    heap.heappop(input_heap, target_index)
    assert input_heap == expected_output
