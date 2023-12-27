import abc, typing as ty


class LinkedListABC(abc.ABC):
    nodetype: type
    size: int
    head: ty.Any

    @abc.abstractmethod
    def empty(self):
        ...

    @abc.abstractmethod
    def popleft(self):
        ...

    @abc.abstractmethod
    def popright(self):
        ...

    @abc.abstractmethod
    def pushleft(self, node):
        ...

    @abc.abstractmethod
    def pushright(self, node):
        ...

    @abc.abstractmethod
    def addat(self, index, node):
        ...

    @abc.abstractmethod
    def popnode(self, index) -> "BaseNode":
        ...

    @abc.abstractmethod
    def getnode(self, index) -> ty.Any:
        ...

    @abc.abstractmethod
    def shift(self, value):
        ...

    @abc.abstractmethod
    def fromiter(self, iterable) -> tuple[ty.Any, int]:
        ...


class BaseNode:
    value: ty.Any
    next: ty.Any

    @abc.abstractmethod
    def clear(self):
        ...


class LinkedListOpsABC(LinkedListABC, ty.MutableSequence):
    def __len__(self) -> int:
        return self.size

    def empty(self):
        return self.size == 0

    def __bool__(self):
        return self.size > 0

    def _iter(self, getnext, start):
        head = start
        while head is not None:
            yield head.value
            head = getnext(head)

    def __reversed__(self):
        return self._iter(lambda node: node.prev, self.getnode(-1))

    def __iter__(self):
        return self._iter(lambda node: node.next, self.head)

    def __getitem__(self, index):
        return self.getnode(index).value

    def __setitem__(self, index, value):
        node = self.getnode(index)
        node.value = value

    def __delitem__(self, index):
        self.popnode(index)

    def append(self, value):
        self.pushright(self.nodetype(value))

    def pop(self, index=-1):
        return self.popnode(index).value

    def remove(self, value):
        index = self.index(value)
        return self.popnode(index).value

    def insert(self, index, value) -> None:
        self.addat(index, self.nodetype(value))

    def __add__(self, values):
        tail, size = self.fromiter(values)
        self.size += size
        if self.head is None:
            self.head = tail
            return
        self._addtail(tail)

    def _addtail(self, tail):
        raise NotImplementedError

    def clear(self):
        self.head = None

    def index(self, value, start: int = 0, stop: int = -1) -> int:
        for index, svalue in enumerate(self, start=start):
            if index == stop:
                break
            if svalue == value:
                return index
        raise ValueError

    def count(self, value):
        return sum(v == value for v in self)

    def __contains__(self, value) -> bool:
        return bool(self.count(value))

    def __str__(self) -> str:
        return "<" + ", ".join(f"{item!r}" for item in self) + ">"

    def extend(self, values) -> None:
        tail, size = self.fromiter(values)
        self._addtail(tail)
        self.size += size
