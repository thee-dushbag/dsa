import typing as ty
import dataclasses as dt
import dsa.tree.generic as generic


class Comparable(ty.Protocol):
    def __lt__(self, other, /) -> bool: ...
    def __gt__(self, other, /) -> bool: ...
    def __eq__(self, other, /) -> bool: ...
    def __le__(self, other, /) -> bool: ...
    def __ge__(self, other, /) -> bool: ...
    def __ne__(self, other, /) -> bool: ...


T = ty.TypeVar("T", bound=Comparable)


@dt.dataclass(slots=True)
class Node(ty.Generic[T]):
    value: T
    left: "Node[T] | None" = None
    right: "Node[T] | None" = None
    parent: "Node[T] | None" = None

    @classmethod
    def none(cls) -> "Node[T]":
        return cls(ty.cast(T, None))

    def isnone(self) -> bool:
        return self.value is None

    __bool__ = isnone


def nodify(items: list[T], parent: Node[T] | None = None) -> Node[T] | None:
    if not items:
        return None
    mid = len(items) // 2
    root = Node(items[mid], parent=parent)
    root.left = nodify(items[:mid], root)
    root.right = nodify(items[mid + 1 :], root)
    return root


def inorder(node: Node[T] | None) -> ty.Iterator[T]:
    iterator = ty.cast(ty.Iterable[Node[T]], generic.inorder(node))
    return (n.value for n in iterator)


def rinorder(node: Node[T] | None) -> ty.Iterator[T]:
    iterator = ty.cast(ty.Iterable[Node[T]], generic.rinorder(node))
    return (n.value for n in iterator)


def _connect(parent: Node[T], left: Node[T] | None, right: Node[T] | None):
    if right is not None:
        right.parent = parent
        parent.right = right
    if left is not None:
        left.parent = parent
        parent.left = left


class BinarySearchTree(ty.Generic[T]):
    def __init__(self, iterable: ty.Iterable[T] | None = None, /) -> None:
        self._tree: Node[T] = ty.cast(Node[T], None)
        self._size = 0
        if iterable is not None:
            self.extend(iterable)

    def __bool__(self):
        return self._size > 0

    def __len__(self):
        return self._size

    def _insert(self, node: Node[T]):
        root = self._tree
        while True:
            if root.value >= node.value:
                if root.left is None:
                    node.parent = root
                    root.left = node
                    return
                root = root.left
            else:
                if root.right is None:
                    node.parent = root
                    root.right = node
                    return
                root = root.right

    def insert(self, node: Node[T], /):
        if self:
            self._insert(node)
        else:
            self._tree = node
        self._size += 1

    def extend(self, iterable: ty.Iterable[T], /):
        v = list(iterable)
        v.sort()
        self._size = n = len(v)
        self._tree = generic.nodify(_connect, Node[T], v, n)

    def __iter__(self):
        return inorder(self._tree)

    def __reversed__(self):
        return rinorder(self._tree)

    def min(self) -> T:
        if self._tree is None:
            raise ValueError("Empty Container")
        return generic.leftmost(self._tree).value

    def max(self) -> T:
        if self._tree is None:
            raise ValueError("Empty Container")
        return generic.rightmost(self._tree).value

    def balance(self):
        if not self:
            return
        self._tree = generic.nodify(_connect, Node[T], self, self._size)

    def height(self) -> int:
        return generic.height(self._tree)

    def find(self, thing: T):
        def guide(node: Node[T]):
            if node.value == thing:
                raise StopIteration
            return node.value > thing

        return generic.walk(self._tree, guide) is None

    def __str__(self):
        return f"BST(len={self._size}, height={self.height()})"
