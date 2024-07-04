import typing as ty
import dataclasses as dt

__all__ = "Treap", "T", "Node"


class _LT(ty.Protocol):
    def __lt__(self, other, /) -> bool: ...


class _LE(ty.Protocol):
    def __le__(self, other, /) -> bool: ...


class _GT(ty.Protocol):
    def __gt__(self, other, /) -> bool: ...


class _GE(ty.Protocol):
    def __ge__(self, other, /) -> bool: ...


class _EQ(ty.Protocol):
    def __eq__(self, other, /) -> bool: ...


class _Ordered(_LT, _LE, _EQ, _GT, _GE, ty.Protocol): ...


T = ty.TypeVar("T", bound=_Ordered)


@dt.dataclass(slots=True)
class Node(ty.Generic[T]):
    key: T
    priority: float
    parent: "Node[T] | None" = dt.field(default=None, repr=False)
    left: "Node[T] | None" = dt.field(default=None, repr=False)
    right: "Node[T] | None" = dt.field(default=None, repr=False)


def _rotate_right(node: Node[T]):
    if node.parent is None:
        raise ValueError("node lacks parent", node)
    assert node.parent.left is node, node

    grand_parent = node.parent.parent
    old_parent = node.parent

    old_parent.left = node.right
    if node.right is not None:
        node.right.parent = old_parent

    node.right = old_parent
    old_parent.parent = node

    node.parent = grand_parent
    if grand_parent is not None:
        if grand_parent.left is old_parent:
            grand_parent.left = node
        else:
            grand_parent.right = node

    return node


def _rotate_left(node: Node[T]):
    if node.parent is None:
        raise ValueError("node lacks parent", node)
    assert node.parent.right is node, node

    grand_parent = node.parent.parent
    old_parent = node.parent

    old_parent.right = node.left
    if node.left is not None:
        node.left.parent = old_parent

    old_parent.parent = node
    node.left = old_parent

    node.parent = grand_parent
    if grand_parent is not None:
        if grand_parent.left is old_parent:
            grand_parent.left = node
        else:
            grand_parent.right = node

    return node


def _siftup(node: Node[T]):
    while node.parent is not None:
        if node.priority < node.parent.priority:
            if node.parent.left is node:
                _rotate_right(node)
            else:
                _rotate_left(node)
        else:
            break
    return node


def _siftdown(node: Node[T]):
    while True:
        if node.left is not None and node.right is not None:
            child, rotate_child = node.right, _rotate_left
            if node.left.priority <= node.right.priority:
                child, rotate_child = node.left, _rotate_right
            if child.priority < node.priority:
                rotate_child(child)
            else:
                break
        elif node.left is not None:
            if node.left.priority < node.priority:
                _rotate_right(node.left)
            else:
                break
        elif node.right is not None:
            if node.right.priority < node.priority:
                _rotate_left(node.right)
            else:
                break
        else:
            break


def _siftdown_leaf(node: Node[T]):
    while True:
        if node.left is not None and node.right is not None:
            if node.left.priority <= node.right.priority:
                _rotate_right(node.left)
            else:
                _rotate_left(node.right)
        elif node.left is not None:
            _rotate_right(node.left)
        elif node.right is not None:
            _rotate_left(node.right)
        else:
            break
    return node


def _insert_bst(tree: Node[T], node: Node[T]):
    while True:
        if tree.key <= node.key:
            if tree.right is None:
                tree.right = node
                break
            tree = tree.right
        else:
            if tree.left is None:
                tree.left = node
                break
            tree = tree.left
    node.parent = tree
    return node


def _find_bst(tree: Node[T], key: T) -> Node[T] | None:
    while True:
        if tree.key == key:
            return tree
        elif tree.key > key:
            if tree.right is None:
                return
            tree = tree.right
        else:
            if tree.left is None:
                return
            tree = tree.left


def _max(tree: Node[T]) -> Node[T]:
    while tree.right is not None:
        tree = tree.right
    return tree


def _min(tree: Node[T]) -> Node[T]:
    while tree.left is not None:
        tree = tree.left
    return tree


def _inorder(tree: Node[T] | None):
    if tree is None:
        return
    yield from _inorder(tree.left)
    yield tree
    yield from _inorder(tree.right)


def _rinorder(tree: Node[T] | None):
    if tree is None:
        return
    yield from _rinorder(tree.right)
    yield tree
    yield from _rinorder(tree.left)


def _height(tree: Node[T] | None):
    if tree is None:
        return 0
    left_height = _height(tree.left) + 1
    right_height = _height(tree.right) + 1
    return max(left_height, right_height)


@dt.dataclass(slots=True)
class Treap(ty.Generic[T]):
    _root: Node[T] | None = dt.field(default=None, init=False)
    _size: int = dt.field(default=0, init=False)

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> ty.Iterator[tuple[T, float]]:
        return map(lambda n: (n.key, n.priority), _inorder(self._root))

    def __reversed__(self) -> ty.Iterator[tuple[T, float]]:
        return map(lambda n: (n.key, n.priority), _rinorder(self._root))

    def __str__(self) -> str:
        return f"Treap(len={self._size}, height={self.height()})"

    __repr__ = __str__

    def height(self) -> int:
        return _height(self._root)

    def left_height(self) -> int:
        if self._root is None:
            return 0
        return _height(self._root.left)

    def right_height(self) -> int:
        if self._root is None:
            return 0
        return _height(self._root.right)

    def height_diff(self) -> int:
        return abs(self.left_height() - self.right_height())

    def balanced(self) -> bool:
        return self.height_diff() < 2

    def max(self) -> T:
        if self._root is None:
            raise ValueError
        return _max(self._root).key

    def min(self) -> T:
        if self._root is None:
            raise ValueError
        return _min(self._root).key

    def _insert(self, node: Node[T]):
        if self._root is None:
            self._root = node
            return
        _insert_bst(self._root, node)
        _siftup(node)
        if node.parent is None:
            self._root = node

    def insert(self, key: T, priority: float):
        self._insert(Node(key, priority))
        self._size += 1

    def update(self, key: T, new_priority: float):
        node = self._find(key)
        old_priority = node.priority
        node.priority = new_priority
        if old_priority == new_priority:
            return
        elif old_priority > new_priority:
            _siftup(node)
        else:
            _siftdown(node)

    def _delete(self, node: Node[T]):
        left, right, parent = node.left, node.right, node.parent
        # push node down till it is a leaf
        _siftdown_leaf(node)
        if parent is None:  # deleting a root node
            # either left or right is the new root
            if left is not None and left.parent is None:
                self._root = left
            elif right is not None and right.parent is None:
                self._root = right
            else:
                # or none of them if there was only one node in the treap
                self._root = None
        if node.parent is not None:
            # delete link from parent to node
            if node.parent.left is node:
                node.parent.left = None
            else:
                node.parent.right = None
            # delete link from node to parent
            node.parent = None
        # node is completely detached from the treap
        return node

    def _find(self, key: T) -> Node[T]:
        if self._root is None:
            raise KeyError(key)
        target = _find_bst(self._root, key)
        if target is None:
            raise KeyError(key)
        return target

    def contains(self, key: T) -> bool:
        if self._root is None:
            return False
        return _find_bst(self._root, key) is not None

    def delete(self, key: T) -> tuple[T, float]:
        node = self._delete(self._find(key))
        self._size -= 1
        return node.key, node.priority

    def top(self) -> tuple[T, float]:
        if self._root is None:
            raise ValueError
        return self._root.key, self._root.priority

    def pop(self) -> tuple[T, float]:
        node = self._deletetop()
        self._size -= 1
        return node.key, node.priority

    def _deletetop(self) -> Node[T]:
        if self._root is None:
            raise ValueError
        return self._delete(self._root)

    def extend(self, items: ty.Iterable[tuple[T, float]]):
        for key, priority in items:
            self.insert(key, priority)

    def clear(self):
        self._root = None
        self._size = 0
