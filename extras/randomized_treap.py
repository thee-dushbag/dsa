import dataclasses as dt
import typing as ty
import random
import treap

__all__ = "RandomizedTreap", "seed"

try:
    _rand = random.SystemRandom()
except Exception:
    _rand = random.Random()


def seed(seed: float | int | bytes | bytearray | str | None = None):
    _rand.seed(seed)


@dt.dataclass(slots=True)
class RandomizedTreap[T: treap._Ordered]:
    _tree: treap.Treap[T] = dt.field(default_factory=treap.Treap, init=False)

    def contains(self, item: T) -> bool:
        return self._tree.contains(item)

    def insert(self, item: T):
        self._tree.insert(item, _rand.random())

    def max(self) -> T:
        return self._tree.max()

    def min(self) -> T:
        return self._tree.min()

    def __len__(self) -> int:
        return len(self._tree)

    def delete(self, item: T):
        self._tree.delete(item)

    def __iter__(self):
        return (key for key, _ in self._tree)

    def __reversed__(self):
        return (key for key, _ in reversed(self._tree))

    def height(self) -> int:
        return self._tree.height()

    def height_diff(self) -> int:
        return self._tree.height_diff()

    def balanced(self) -> bool:
        return self._tree.balanced()

    def extend(self, iterable: ty.Iterable[T]):
        for item in iterable:
            self.insert(item)

    seed = staticmethod(seed)

    def __str__(self) -> str:
        return f"RandomizedTreap(len={len(self)}, height={self.height()})"

    __repr__ = __str__
