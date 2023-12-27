from .abc_ import BaseNode, ty


class _NextNodeStr:
    next: ty.Any
    value: ty.Any

    def __str__(self) -> str:
        items, node = [], self
        while node:
            items.append(node)
            node = node.next
        return "[" + " -> ".join(f"{node!r}" for node in items) + "]"

    def __repr__(self) -> str:
        # return f"{self.__class__.__name__}(value={self.value}, id={hex(id(self))})"
        return f"{self.__class__.__name__}({self.value})"


class ForwardNode(BaseNode, _NextNodeStr):
    def __init__(self, value=None) -> None:
        self.value = value
        self.next = None

    def clear(self):
        self.next = None


class Node(BaseNode, _NextNodeStr):
    def __init__(self, value=None) -> None:
        self.value = value
        self.next = None
        self.prev = None

    def clear(self):
        self.next = None
        self.prev = None
