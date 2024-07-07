import typing as ty
import dataclasses as dt

__all__ = "Treap", "Node"


class _Ordered(ty.Protocol):
    def __gt__(self, other: ty.Any, /) -> bool: ...


@dt.dataclass(slots=True)
class Node[T]:
    key: T
    priority: float
    parent: "Node[T] | None" = dt.field(default=None, repr=False)
    left: "Node[T] | None" = dt.field(default=None, repr=False)
    right: "Node[T] | None" = dt.field(default=None, repr=False)


def _rotate_right[T](node: Node[T]):
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


def _rotate_left[T](node: Node[T]):
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


def _siftup[T](node: Node[T]):
    while node.parent is not None:
        if node.priority < node.parent.priority:
            if node.parent.left is node:
                _rotate_right(node)
            else:
                _rotate_left(node)
        else:
            break


def _siftdown[T](node: Node[T]):
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


def _siftdown_leaf[T](node: Node[T]):
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


def _insert_bst[T: _Ordered](tree: Node[T], node: Node[T]):
    while True:
        if tree.key > node.key:
            if tree.left is None:
                tree.left = node
                break
            tree = tree.left
        else:
            if tree.right is None:
                tree.right = node
                break
            tree = tree.right
    node.parent = tree


def _find_bst[T: _Ordered](tree: Node[T], key: T) -> Node[T] | None:
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


def _max[T](tree: Node[T]) -> Node[T]:
    while tree.right is not None:
        tree = tree.right
    return tree


def _min[T](tree: Node[T]) -> Node[T]:
    while tree.left is not None:
        tree = tree.left
    return tree


def _len[T](tree: Node[T] | None) -> int:
    total: int = 0
    stack = [tree]
    while stack:
        node = stack.pop()
        if node is None:
            continue
        total += 1
        stack.append(node.left)
        stack.append(node.right)
    return total


type _Order[T] = ty.Callable[[Node[T]], ty.Iterable[Node[T] | None]]


def _inorder_generic[T](tree: Node[T] | None, order: _Order[T]):
    if tree is None:
        return
    stack = [None, *order(tree)]
    while True:
        child = stack.pop()
        if child is not None:
            stack.extend(order(child))
            continue
        parent = stack.pop()
        if parent is None:
            break
        yield parent


def _inorder[T](tree: Node[T] | None) -> ty.Iterable[Node[T]]:
    return _inorder_generic(tree, lambda n: (n.right, n, n.left))


def _rinorder[T](tree: Node[T] | None) -> ty.Iterable[Node[T]]:
    return _inorder_generic(tree, lambda n: (n.left, n, n.right))


def _height[T](node: Node[T] | None) -> int:
    stack: list[tuple[Node[T] | None, bool, int]] = [(node, False, 0)]
    while True:
        node, expanded, height = stack.pop()
        if expanded:
            if not stack:
                break
            other, oexpanded, oheight = stack.pop()
            if oexpanded:
                parent, _, _ = stack.pop()
                new_height = max(oheight, height) + 1
                stack.append((parent, True, new_height))
            else:
                stack.append((node, True, height))
                stack.append((other, False, 0))
        else:
            stack.append((node, True, 0))
            if node is not None:
                stack.append((node.left, False, 0))
                stack.append((node.right, False, 0))
    return height


@dt.dataclass(slots=True)
class Treap[T: _Ordered]:
    _root: Node[T] | None = dt.field(default=None, init=False, repr=False)
    _size: int = dt.field(default=0, init=False)

    def __len__(self) -> int:
        return self._size

    __bool__ = __len__

    def __iter__(self) -> ty.Iterator[tuple[T, float]]:
        return map(lambda n: (n.key, n.priority), _inorder(self._root))

    def __reversed__(self) -> ty.Iterator[tuple[T, float]]:
        return map(lambda n: (n.key, n.priority), _rinorder(self._root))

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
            raise KeyError
        return _max(self._root).key

    def min(self) -> T:
        if self._root is None:
            raise KeyError
        return _min(self._root).key

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

    def extend(self, items: ty.Iterable[tuple[T, float]]):
        for key, priority in items:
            self.insert(key, priority)

    def clear(self):
        self._root = None
        self._size = 0

    def _insert(self, node: Node[T]):
        if self._root is None:
            self._root = node
            return
        _insert_bst(self._root, node)
        _siftup(node)
        if node.parent is None:
            self._root = node

    def _delete(self, node: Node[T]):
        # capture all immediate neighbors to select a new root if necessary
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

    def _deletetop(self) -> Node[T]:
        if self._root is None:
            raise ValueError
        return self._delete(self._root)
