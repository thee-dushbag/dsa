import typing as ty


class Comparable(ty.Protocol):
    def __lt__(self, other: ty.Any, /) -> ty.Any: ...
    def __gt__(self, other: ty.Any, /) -> ty.Any: ...
    def __eq__(self, other: ty.Any, /) -> ty.Any: ...
    def __le__(self, other: ty.Any, /) -> ty.Any: ...
    def __ge__(self, other: ty.Any, /) -> ty.Any: ...
    def __ne__(self, other: ty.Any, /) -> ty.Any: ...


T = ty.TypeVar("T", bound=Comparable)


class Node(ty.Generic[T]):
    def __init__(
        self,
        value: T,
        *,
        left: "Node[T] | None" = None,
        right: "Node[T] | None" = None,
        parent: "Node[T] | None" = None,
    ) -> None:
        self.value = value
        self.left = left
        self.right = right
        self.parent = parent

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"<Node value={self.value!r}>"

    @classmethod
    def none(cls) -> "Node[T]":
        return cls(ty.cast(T, None))

    def isnone(self) -> bool:
        return self.value is None

    __bool__ = isnone


def inorder(tree: Node[T] | None) -> ty.Generator[T, None, None]:
    if tree is None:
        return
    yield from inorder(tree.left)
    yield tree.value
    yield from inorder(tree.right)


def rinorder(tree: Node[T] | None) -> ty.Generator[T, None, None]:
    if tree is None:
        return
    yield from inorder(tree.right)
    yield tree.value
    yield from inorder(tree.left)


def preorder(tree: Node[T] | None) -> ty.Generator[T, None, None]:
    if tree is None:
        return
    yield tree.value
    yield from preorder(tree.left)
    yield from preorder(tree.right)


def _height(tree: Node[T] | None) -> int:
    if tree is None:
        return 0
    left = _height(tree.left)
    right = _height(tree.right)
    return max(left, right) + 1


def nodify(items: list[T], parent: Node[T] | None = None) -> Node[T] | None:
    if not items:
        return None
    mid = len(items) // 2
    root = Node(items[mid], parent=parent)
    root.left = nodify(items[:mid], root)
    root.right = nodify(items[mid + 1 :], root)
    return root


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
        tree = nodify((s := sorted(iterable)))
        self._size = len(s)
        self._tree = ty.cast(Node[T], tree)

    def __iter__(self):
        return inorder(self._tree)

    def __reversed__(self):
        return rinorder(self._tree)

    def min(self) -> T:
        if not self:
            raise ValueError("Empty Container")
        root = self._tree
        while root.left is not None:
            root = root.left
        return root.value

    def max(self) -> T:
        if not self:
            raise ValueError("Empty Container")
        root = self._tree
        while root.right is not None:
            root = root.right
        return root.value

    def balance(self):
        tree = nodify(list(self))
        self._tree = ty.cast(Node[T], tree)

    def height(self) -> int:
        return _height(self._tree)

    def find(self, thing: T):
        root = self._tree
        while root:
            if root.value == thing:
                return True
            elif root.value < thing:
                root = root.right
            else:
                root = root.left

    def __str__(self):
        values = list(preorder(self._tree))
        return f"BST({values}, len={self._size})"
