from dataclasses import dataclass


@dataclass
class Node[T]:
    data: T
    left: "Node[T] | None" = None
    right: "Node[T] | None" = None

    @property
    def height(self) -> int:
        if self.left and self.right:
            return max(self.left.height, self.right.height) + 1
        elif self.left:
            return self.left.height
        elif self.right:
            return self.right.height
        return 1
