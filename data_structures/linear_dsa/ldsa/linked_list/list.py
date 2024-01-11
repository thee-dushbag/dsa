from .circular_list import CircularDoublyList as _CircularDoublyList
from .sequence import MutableSequenceMixin as _MutableSequenceMixin
from .singly_list import SinglyList as _SinglyList
from .doubly_list import DoublyList as _DoublyList
import typing as ty

_T = ty.TypeVar("_T")
__all__ = "SinglyLinkedList", "CirDoublyLinkedList", "DoublyLinkedList"


class SinglyLinkedList(_MutableSequenceMixin[_T]):
    def __init__(self, iterable: ty.Iterator[_T] | None = None, /) -> None:
        super().__init__(_SinglyList(iterable))


class DoublyLinkedList(_MutableSequenceMixin[_T]):
    def __init__(self, iterable: ty.Iterator[_T] | None = None, /) -> None:
        super().__init__(_DoublyList(iterable))


class CirDoublyLinkedList(_MutableSequenceMixin[_T]):
    def __init__(self, iterable: ty.Iterator[_T] | None = None, /) -> None:
        super().__init__(_CircularDoublyList(iterable))
