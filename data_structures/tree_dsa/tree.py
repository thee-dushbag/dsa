from dataclasses import dataclass
import typing as ty

T = ty.TypeVar('T')

@dataclass
class Node(ty.Generic[T]):
    data: T
    left: "Node | None" = None
    right: "Node | None" = None

    @property
    def height(self) -> int:
        if self.left and self.right:
            return max(self.left.height, self.right.height) + 1
        elif self.left:
            return self.left.height
        elif self.right:
            return self.right.height
        return 0
