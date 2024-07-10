import typing as ty

_T = ty.TypeVar("_T")


class NodeABC(ty.Generic[_T]):
    value: _T
    next: "NodeABC[_T] | None"
    prev: "NodeABC[_T] | None"

    def clear(self) -> ty.Any:
        ...


class ListABC(ty.Protocol[_T]):
    def nodefactory(self, value: _T) -> NodeABC[_T]:
        ...

    def getnode(self, index: int) -> NodeABC[_T]:
        ...

    def empty(self) -> bool:
        ...

    def insert(self, index: int, node: NodeABC[_T]):
        ...

    def size(self) -> int:
        ...

    def delnode(self, index: int) -> NodeABC[_T]:
        ...

    def clear(self):
        ...

    def __iter__(self) -> ty.Iterator[NodeABC[_T]]:
        ...

    def __reversed__(self) -> ty.Iterator[NodeABC[_T]]:
        ...

    def extend(self, iterable: ty.Iterable):
        ...
