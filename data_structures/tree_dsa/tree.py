import typing as ty

__all__ = (
    "INode",
    "inorder",
    "rinorder",
    "preorder",
    "rpreorder",
    "postorder",
    "rpostorder",
    "breadth",
    "rbreadth",
    "height",
    "rightmost",
    "leftmost",
    "walk",
    "length",
)


class INode(ty.Protocol):
    @property
    def left(self) -> "INode | None": ...
    @property
    def right(self) -> "INode | None": ...


class mINode(ty.Protocol):
    left: "mINode | None"
    right: "mINode | None"


type _Orderer = ty.Callable[[INode], ty.Iterable[INode | None]]


def _inorder(tree: INode | None, order: _Orderer) -> ty.Iterable[INode]:
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


def _breadth(tree: INode | None, order: _Orderer) -> ty.Iterable[INode]:
    from collections import deque

    queue = deque[INode | None]((tree,))
    while queue:
        node = queue.popleft()
        if node is not None:
            queue.extend(order(node))
            yield node


def _preorder(tree: INode | None, order: _Orderer) -> ty.Iterable[INode]:
    stack: list[INode | None] = [tree]
    while stack:
        node = stack.pop()
        if node is not None:
            stack.extend(order(node))
            yield node


def _postorder(tree: INode | None, order: _Orderer) -> ty.Iterable[INode]:
    stack: list[tuple[INode | None, bool]] = [(tree, False)]
    ex_order = True, False, False
    while stack:
        node, expanded = stack.pop()
        if node is not None:
            if expanded:
                yield node
                continue
            stack.extend(zip(order(node), ex_order))


def inorder(tree: INode | None):
    return _inorder(tree, lambda n: (n.right, n, n.left))


def rinorder(tree: INode | None):
    return _inorder(tree, lambda n: (n.left, n, n.right))


def preorder(tree: INode | None):
    return _preorder(tree, lambda n: (n.right, n.left))


def rpreorder(tree: INode | None):
    return _preorder(tree, lambda n: (n.left, n.right))


def postorder(tree: INode | None):
    return _postorder(tree, lambda n: (n, n.right, n.left))


def rpostorder(tree: INode | None):
    return _postorder(tree, lambda n: (n, n.left, n.right))


def breadth(tree: INode | None):
    return _breadth(tree, lambda n: (n.left, n.right))


def rbreadth(tree: INode | None):
    return _breadth(tree, lambda n: (n.right, n.left))


def rightmost(tree: INode) -> INode:
    while True:
        if tree.right is None:
            return tree
        tree = tree.right


def leftmost(tree: INode) -> INode:
    while True:
        if tree.left is None:
            return tree
        tree = tree.left


def walk(tree: INode | None, guide: ty.Callable[[ty.Any], bool]) -> INode | None:
    try:
        while tree is not None:
            tree = tree.right if guide(tree) else tree.left
    except StopIteration:
        return tree


def height(node: INode | None) -> int:
    stack: list[tuple[INode | None, bool, int]] = [(node, False, 0)]
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


def length(tree: INode | None) -> int:
    total: int = 0
    stack = [tree]
    while stack:
        tree = stack.pop()
        if tree is None:
            continue
        total += 1
        stack.append(tree.left)
        stack.append(tree.right)
    return total


def bstindices(layers: int) -> ty.Generator[int, None, None]:
    from collections import deque

    size: int = 2**layers - 1
    queue = deque[int]((size // 2,))
    step: int = 2 ** (layers - 2)
    nqueue = deque[int]()
    while layers != 0:
        root = queue.popleft()
        yield root
        nqueue.append(root - step)
        nqueue.append(root + step)
        if not queue:
            layers, step = layers - 1, step // 2
            queue, nqueue = nqueue, queue
