import typing as ty


class DisjointSet[T]:
    __slots__ = ("_set", "_size")

    def __init__(self, iterable: ty.Iterable[T] | None = None) -> None:
        self._set: dict[T, set[T]] = {}
        self._size: int = 0
        if iterable is not None:
            self.extend(iterable)

    @property
    def elements(self) -> int:
        return len(self._set)

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> ty.Iterator[set[T]]:
        seen: set[int] = set()
        for partition in self._set.values():
            if id(partition) not in seen:
                seen.add(id(partition))
                yield partition

    def contains(self, element: T):
        return element in self._set

    __contains__ = contains

    def add(self, element: T):
        if element in self._set:
            raise ValueError(element)
        self._set[element] = {element}
        self._size += 1

    def extend(self, iterable: ty.Iterable[T]):
        for element in iterable:
            self.add(element)

    def merge(self, e1: T, e2: T):
        p1 = self._set[e1]
        p2 = self._set[e2]
        if p1 is p2:
            return
        if len(p1) > len(p2):
            p1, p2 = p2, p1
        for e in p1:
            self._set[e] = p2
        p2 |= p1
        self._size -= 1

    def merge_all(self, e1: T, *e2s: T):
        for e2 in e2s:
            self.merge(e1, e2)

    def merge_if(self, predicate: ty.Callable[[T], object | bool]):
        targets = filter(predicate, self._set)
        sentinel = object()
        e1 = ty.cast(T, next(targets, sentinel))
        if e1 is not sentinel:
            for e2 in targets:
                self.merge(e1, e2)

    def same(self, e1: T, e2: T):
        return self._set[e1] is self._set[e2]

    def disjoint(self, e1: T, e2: T):
        return self._set[e1] is not self._set[e2]

    def clear(self):
        self._set.clear()

    def partition(self, element: T):
        return self._set[element]

    def remove(self, element: T):
        self._set[element].remove(element)
        del self._set[element]

    def remove_partition(self, element: T):
        for elem in self._set[element]:
            del self._set[elem]
        self._size -= 1

    def unique(self, element: T):
        self.remove(element)
        self.add(element)
