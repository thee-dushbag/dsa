import dataclasses as dt
import math
import typing as ty
import random
import treap

__all__ = "RandomizedTreap", "seed"

try:
    _rand = random.SystemRandom()
except Exception:
    _rand = random.Random()
_rand = random.Random()


def seed(seed: float | int | bytes | bytearray | str | None = None):
    _rand.seed(seed)


@dt.dataclass(slots=True)
class RandomizedTreap(ty.Generic[treap.T]):
    _tree: treap.Treap[treap.T] = dt.field(
        default_factory=treap.Treap[treap.T], init=False
    )

    def contains(self, item: treap.T) -> bool:
        return self._tree.contains(item)

    def insert(self, item: treap.T):
        self._tree.insert(item, _rand.random() ** 2)

    def max(self) -> treap.T:
        return self._tree.max()

    def min(self) -> treap.T:
        return self._tree.min()

    def __len__(self) -> int:
        return len(self._tree)

    def delete(self, item: treap.T):
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

    def extend(self, iterable: ty.Iterable[treap.T]):
        for item in iterable:
            self.insert(item)

    seed = staticmethod(seed)

    def __str__(self) -> str:
        return f"RandomizedTreap(len={len(self)}, height={self.height()})"

    __repr__ = __str__

    def try_balance(self):
        values = list(self)
        ideal_height = math.ceil(math.log2(len(values)))
        indices = _bstindices(ideal_height)
        self._tree.clear()
        for index in indices:
            try:
                self.insert(values[index])
            except IndexError:
                ...


if __name__ == "__main__":
    rt = RandomizedTreap[int]()
    rt.extend(range(1, 1))
    print(rt)
    # assert rt._tree._root is not None
    # print("left :", rt._tree.left_height(), treap._len(rt._tree._root.left))
    # print("right:", rt._tree.right_height(), treap._len(rt._tree._root.right))
    # rt.try_balance()
    # print("left :", rt._tree.left_height(), treap._len(rt._tree._root.left))
    # print("right:", rt._tree.right_height(), treap._len(rt._tree._root.right))
    # print(rt.min(), rt.max())
    print(list(reversed(rt)))
