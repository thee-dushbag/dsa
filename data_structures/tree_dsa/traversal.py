"""
There are three standard ways of traversing a
tree data structure. These are preorder, inorder
and postorder.
1. The preorder consumes a node's data first then
the left childs then the right's. (mnemonic: PLR)
2. The inorder consumes the left child's data then
the node's the lastly the right child's. (mnemonic: LPR)
3. The postorder consumes the left child's data then the
right childs and lastly the node's data. (mnemonic: LRP)
"""

import typing as ty
import dataclasses as dt

T = ty.TypeVar("T")

@dt.dataclass(slots=True)
class Node[T]:
    data: T
    left: "Node[T] | None" = None
    right: "Node[T] | None" = None

    from tree import height


DataStream = ty.Generator[T, None, None]
Traverser = ty.Callable[[Node | None], DataStream[T]]


def preorder(tree: Node[T] | None) -> DataStream[Node[T]]:
    if tree is None:
        return
    yield tree
    yield from preorder(tree.left)
    yield from preorder(tree.right)


def inorder(tree: Node[T] | None) -> DataStream[Node[T]]:
    if tree is None:
        return
    yield from inorder(tree.left)
    yield tree
    yield from inorder(tree.right)


def postorder(tree: Node[T] | None) -> DataStream[Node[T]]:
    if tree is None:
        return
    yield from postorder(tree.left)
    yield from postorder(tree.right)
    yield tree


def rpreorder(tree: Node[T] | None) -> DataStream[Node[T]]:
    if tree is None:
        return
    yield tree
    yield from rpreorder(tree.right)
    yield from rpreorder(tree.left)


def rinorder(tree: Node[T] | None) -> DataStream[Node[T]]:
    if tree is None:
        return
    yield from rinorder(tree.right)
    yield tree
    yield from rinorder(tree.left)


def rpostorder(tree: Node[T] | None) -> DataStream[Node[T]]:
    if tree is None:
        return
    yield from rpostorder(tree.right)
    yield from rpostorder(tree.left)
    yield tree


def main():
    a = Node(1)
    b = Node(2)
    c = Node(3, a, b)
    a = Node(4)
    b = Node(5)
    d = Node(6, a, b)
    root = Node(7, c, d)

    print(f"{root.height() = }")
    print(f"{c.height() = }")
    print(f"{d.height() = }")
    print(f"{a.height() = }")
    print(f"{b.height() = }")

    def chain(root: Node, traverser: Traverser, sep: str = " -> ") -> str:
        return sep.join(map(lambda node: str(node.data), traverser(root)))

    # Forward traversals
    postorder_path = chain(root, postorder)
    preorder_path = chain(root, preorder)
    inorder_path = chain(root, inorder)

    # Reversed traversals
    rpostorder_path = chain(root, rpostorder)
    rpreorder_path = chain(root, rpreorder)
    rinorder_path = chain(root, rinorder)

    print(f"preorder   = {preorder_path}")
    print(f"rpostorder = {rpostorder_path}")
    print(f"inorder    = {inorder_path}")
    print(f"rinorder   = {rinorder_path}")
    print(f"postorder  = {postorder_path}")
    print(f"rpreorder  = {rpreorder_path}")


if __name__ == "__main__":
    main()
