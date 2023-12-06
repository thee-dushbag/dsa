from .._none import NONE, Optional
import typing as _ty

__all__ = "Node", "ForwardNode", "_hasvalue", "_isnone"

_T = _ty.TypeVar("_T", contravariant=True)
OptNode = Optional["Node[_T]"]
OptValue = Optional[_T]


class Node(_ty.Generic[_T]):
    def __init__(
        self, value: OptValue[_T], *, next: OptNode[_T] = NONE, prev: OptNode[_T] = NONE
    ) -> None:
        self._next = next
        self._prev = prev
        self._value = value

    @property
    def value(self) -> OptValue[_T]:
        return self._value

    @value.setter
    def value(self, value: OptValue[_T]) -> None:
        self._value = value

    @property
    def next(self) -> OptNode[_T]:
        return self._next

    @next.setter
    def next(self, node: OptNode[_T]) -> None:
        self._next = node

    @property
    def prev(self) -> OptNode[_T]:
        return self._prev

    @prev.setter
    def prev(self, node: OptNode[_T]) -> None:
        self._prev = node

    def clear(self) -> None:
        self._next = NONE
        self._prev = NONE

    def has_value(self) -> bool:
        return self.value is not NONE

    def __bool__(self) -> bool:
        return self.has_value()


class ForwardNode(Node, _ty.Generic[_T]):
    def __init__(self, value: OptValue[_T] = NONE, *, next: OptNode[_T] = NONE) -> None:
        super().__init__(value, next=next)

    @property
    def prev(self) -> OptNode[_T]:
        raise NotImplementedError("prev node is not implemented for this node type")


def _hasvalue(node: Node[_T]) -> _ty.TypeGuard[_T]:
    return node.has_value()


def _isnone(node: OptNode[_T]) -> _ty.TypeGuard[Node[_T]]:
    return node is NONE
