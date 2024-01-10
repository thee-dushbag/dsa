import typing as ty
from typing import Any
from .abc import NodeABC

T = ty.TypeVar("T")


class ForwardNode(NodeABC[T]):
    def __init__(self, value: T, *, next: "ForwardNode | None" = None) -> None:
        self.value: T = value
        self.next: ForwardNode | None = next

    def clear(self):
        self.next = None


class Node(NodeABC[T]):
    def __init__(
        self, value: T, *, next: "Node|None" = None, prev: "Node|None" = None
    ) -> None:
        self.value: T = value
        self.next: Node | None = next
        self.prev: Node | None = prev

    def clear(self) -> Any:
        self.next = None
        self.prev = None


class CircularNode(ty.Generic[T]):
    def __init__(
        self,
        value: T,
        *,
        next: "CircularNode | None" = None,
        prev: "CircularNode | None" = None
    ) -> None:
        self.value: T = value
        self.next: CircularNode = next or self
        self.prev: CircularNode = prev or self

    def clear(self) -> Any:
        self.next = self
        self.prev = self
