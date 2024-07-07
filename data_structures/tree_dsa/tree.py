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


Node = ty.TypeVar("Node", bound=INode)
type _Orderer[Node: INode] = ty.Callable[[Node], ty.Iterable[Node | None]]


def _inorder(tree: Node | None, order: _Orderer[Node]) -> ty.Iterable[Node]:
    if tree is None:
        return
    stack: list[Node | None] = [None, *order(tree)]
    while True:
        child = stack.pop()
        if child is not None:
            stack.extend(order(child))
            continue
        parent = stack.pop()
        if parent is None:
            break
        yield parent


def _breadth(tree: Node | None, order: _Orderer[Node]) -> ty.Iterable[Node]:
    from collections import deque

    queue = deque[Node | None]((tree,))
    while queue:
        node = queue.popleft()
        if node is not None:
            queue.extend(order(node))
            yield node


def _preorder(tree: Node | None, order: _Orderer[Node]) -> ty.Iterable[Node]:
    stack: list[Node | None] = [tree]
    while stack:
        node = stack.pop()
        if node is not None:
            stack.extend(order(node))
            yield node


def _postorder(tree: Node | None, order: _Orderer[Node]) -> ty.Iterable[Node]:
    stack: list[tuple[Node | None, bool]] = [(tree, False)]
    ex_order = True, False, False
    while stack:
        node, expanded = stack.pop()
        if node is not None:
            if expanded:
                yield node
                continue
            stack.extend(zip(order(node), ex_order))


def inorder(tree: Node | None) -> ty.Iterable[Node]:
    return _inorder(tree, lambda n: (n.right, n, n.left))


def rinorder(tree: Node | None) -> ty.Iterable[Node]:
    return _inorder(tree, lambda n: (n.left, n, n.right))


def preorder(tree: Node | None) -> ty.Iterable[Node]:
    return _preorder(tree, lambda n: (n.right, n.left))


def rpreorder(tree: Node | None) -> ty.Iterable[Node]:
    return _preorder(tree, lambda n: (n.left, n.right))


def postorder(tree: Node | None) -> ty.Iterable[Node]:
    return _postorder(tree, lambda n: (n, n.right, n.left))


def rpostorder(tree: Node | None) -> ty.Iterable[Node]:
    return _postorder(tree, lambda n: (n, n.left, n.right))


def breadth(tree: Node | None) -> ty.Iterable[Node]:
    return _breadth(tree, lambda n: (n.left, n.right))


def rbreadth(tree: Node | None) -> ty.Iterable[Node]:
    return _breadth(tree, lambda n: (n.right, n.left))


def rightmost(tree: Node) -> Node:
    while True:
        if tree.right is None:
            return tree
        tree = tree.right


def leftmost(tree: Node) -> Node:
    while True:
        if tree.left is None:
            return tree
        tree = tree.left


def walk(tree: Node | None, guide: ty.Callable[[Node], bool]) -> Node | None:
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


type _Connector[Node] = ty.Callable[[Node, Node, Node | None], None]
type _Creator[Node, T] = ty.Callable[[T], Node]


def nodify[
    Node, T
](
    connect: _Connector[Node],
    create: _Creator[Node, T],
    iterable: ty.Iterable[T],
    n: int | None = None,
) -> Node:
    from collections import deque
    import math as m

    if n is None:
        iterable = list(iterable)
        n = len(iterable)
    if n <= 0:
        raise ValueError(f"Invalid iterable size value {n=}, expected n > 0")

    def manage_extras(iterable: ty.Iterable[T], extras: ty.MutableSequence[T]):
        extra_count = n - 2 ** m.floor(m.log2(n + 1)) + 1
        iterator = iter(iterable)
        for _ in range(extra_count):
            extras.append(next(iterator))
            yield next(iterator)
        yield from iterator

    extras: deque[T] = deque()
    iterator = manage_extras(iterable, extras)
    leaf, sentinel = create(next(iterator)), object()
    children: list[tuple[Node, int]] = [(leaf, 0)]
    leaves: deque[Node] = deque((leaf,))
    parents: list[T] = []

    while True:
        while parents:
            rnode, rheight = children[-1]
            lnode, lheight = children[-2]
            if rheight != lheight:
                break
            parent = create(parents.pop())
            connect(parent, lnode, rnode)
            children.pop()
            children.pop()
            children.append((parent, lheight + 1))

        new_parent: T = next(iterator, sentinel) # type: ignore
        if new_parent is sentinel:
            break
        parents.append(new_parent)
        new_child = create(next(iterator))
        children.append((new_child, 0))
        leaves.append(new_child)

    while extras:
        parent = leaves.popleft()
        left = create(extras.popleft())
        right = create(extras.popleft()) if extras else None
        connect(parent, left, right)

    return children.pop()[0]
