import typing as ty
import dataclasses as dt


class _LT(ty.Protocol):
    def __lt__(self, other) -> bool: ...


class _LE(ty.Protocol):
    def __le__(self, other) -> bool: ...


class _GT(ty.Protocol):
    def __gt__(self, other) -> bool: ...


class _GE(ty.Protocol):
    def __ge__(self, other) -> bool: ...


class _EQ(ty.Protocol):
    def __eq__(self, other) -> bool: ...


class Ordered(_LT, _LE, _EQ, _GT, _GE): ...


T = ty.TypeVar("T", bound=Ordered)


@dt.dataclass(slots=True)
class Node(ty.Generic[T]):
    key: T
    priority: float
    parent: "Node[T] | None" = None
    left: "Node[T] | None" = None
    right: "Node[T] | None" = None


def _rotate_right(node: Node[T]):
    if node.right is not None:
        node.right.parent = node.parent
    if node.parent is not None:
        assert node.parent.left is node
        grand_parent = node.parent.parent
        node.parent.left = node.right
        node.parent.parent = node
        node.right = node.parent
        node.parent = grand_parent
        if grand_parent is not None:
            grand_parent.left = node
    return node


def _rotate_left(node: Node[T]):
    if node.left is not None:
        node.left.parent = node.parent
    if node.parent is not None:
        assert node.parent.right is node
        grand_parent = node.parent.parent
        node.parent.right = node.left
        node.parent.parent = node
        node.left = node.parent
        node.parent = grand_parent
        if grand_parent is not None:
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
        if tree.key >= node.key:
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

@dt.dataclass(slots=True)
class Treap(ty.Generic[T]):
    _root: Node[T] | None = dt.field(default=None, init=False)
    _size: int = dt.field(default=0, init=False)

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

    def _delete(self, key: T) -> Node[T]:
        ...
