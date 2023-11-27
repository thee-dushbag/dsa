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


# Test linked lists
def test_forward_list():
    from ldsa.linked_list import ForwardList, Node
    items = [1, 2, 3, 4]
    flist = ForwardList.fromiter(items)
    assert list(flist) == items, '__iter__ failed.'
    assert list(reversed(items)) == list(reversed(flist)), '__reversed__ error'
    assert flist.lastnode().value == items[-1], 'faild last element'
    items.append(5)
    flist.append(Node(5))
    assert flist.lastnode().value == items[-1], 'append failed.'
    items.insert(0, 10)
    flist.insert(Node(10), 0)
    assert flist[0] == items[0], 'insert failed.'
    assert flist[-1] == items[-1], f'Check last element index.'
    items.insert(3, 100)
    flist.insert(Node(100), 3)
    assert flist[3] == items[3], 'insert failed.'
    items.pop(3)
    flist.delete(3)
    assert list(flist) == items, 'delete failed.'
    items.pop(2)
    del flist[2]
    assert list(flist) == items, 'delete failed.'


def test_bilist():
    from ldsa.linked_list import List, BiNode
    items = [1, 2, 3, 4]
    flist = List.fromiter(items)
    assert list(flist) == items, '__iter__ failed.'
    assert flist.lastnode().value == items[-1], 'faild last element'
    assert list(reversed(items)) == list(reversed(flist)), '__reversed__ error'
    items.append(5)
    flist.append(BiNode(5))
    assert flist.lastnode().value == items[-1], 'append failed.'
    items.insert(0, 10)
    flist.insert(BiNode(10), 0)
    assert flist[0] == items[0], 'insert failed.'
    assert flist[-1] == items[-1], f'Check last element index.'
    items.insert(3, 100)
    flist.insert(BiNode(100), 3)
    assert flist[3] == items[3], 'insert failed.'
    items.pop(3)
    flist.delete(3)
    assert list(flist) == items, 'delete failed.'
    items.pop(2)
    del flist[2]
    assert list(flist) == items, 'delete failed.'