from .circular_list import CircularDoublyList
from .sequence import MutableSequenceMixin
from .singly_list import SinglyList
from .doubly_list import DoublyList
import typing as ty

_T = ty.TypeVar("_T")


class SinglyLinkedList(MutableSequenceMixin[_T]):
    def __init__(self, iterable: ty.Iterator[_T] | None = None, /) -> None:
        super().__init__(SinglyList(iterable))


class DoublyLinkedList(MutableSequenceMixin[_T]):
    def __init__(self, iterable: ty.Iterator[_T] | None = None, /) -> None:
        super().__init__(DoublyList(iterable))


class CirDoublyLinkedList(MutableSequenceMixin[_T]):
    def __init__(self, iterable: ty.Iterator[_T] | None = None, /) -> None:
        super().__init__(CircularDoublyList(iterable))
