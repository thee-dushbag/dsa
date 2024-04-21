import random as rd

offset = 17
data_pool = list(range(offset, 10000))  # Sorted


def _test_searching(searcher):
    for _ in range(50):
        tofind = rd.choice(data_pool)
        index = searcher(data_pool, tofind)  # Sorted input for BS
        assert index == tofind - offset
    tofind = -1  # Not in array
    assert searcher(data_pool, tofind) is None


def _test_sorting(sorter):
    for _ in range(250):
        # Hopefully, this is enough a test
        data = rd.choices(data_pool, k=250)
        sorted_data = sorted(data)  # Create a new sorted list
        sorter(data)  # InPlace Sort
        assert data == sorted_data


def test_insertion_sort_simple_search():
    from sorting import insertion_sort

    _test_sorting(insertion_sort)


def test_insertion_sort_binary_search():
    from sorting import insertion_sort_bst

    _test_sorting(insertion_sort_bst)


def test_selection_sort():
    from sorting import selection_sort

    _test_sorting(selection_sort)


def test_bubble_sort():
    from sorting import bubble_sort

    _test_sorting(bubble_sort)


def test_quick_sort():
    from sorting import quick_sort

    _test_sorting(quick_sort)


def test_binary_search():
    from searching import binary_search

    _test_searching(binary_search)


def test_simple_search():
    from searching import simple_search

    _test_searching(simple_search)  # Not Much Effect if Array is Sorted


def test_heap_sort():
    from sorting import heap_sort

    _test_sorting(heap_sort)


def test_bst_edge1():
    from searching import binary_search

    data = [1, 2, 3, 5, 6, 7, 8, 9, 10]
    index = binary_search(data, 4)
    assert index is None, index
