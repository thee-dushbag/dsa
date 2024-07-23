import typing as ty
import dataclasses as dt


@dt.dataclass(slots=True)
class Node:
    value: str
    key_node: bool = dt.field(default=False)
    children: dict[str, "Node"] = dt.field(default_factory=dict, init=False, repr=False)


def _contains(root: Node, string: str) -> bool:
    for char in string:
        if char in root.children:
            root = root.children[char]
            continue
        break
    else:
        return root.key_node
    return False


def _insert(root: Node, string: str) -> bool:
    striter = iter(string)
    for char in striter:
        if char in root.children:
            root = root.children[char]
            continue
        root.children[char] = root = Node(char)
        break
    else:
        if root.key_node:
            return False

    for node in map(Node, striter):
        root.children[node.value] = root = node

    root.key_node = True
    return True


def _iterate(root: Node, prefix: str) -> ty.Iterator[str]:
    prefix += root.value
    if root.key_node:
        yield prefix
    for child in root.children.values():
        yield from _iterate(child, prefix)


@dt.dataclass(slots=True)
class Trie:
    _root: Node = dt.field(default_factory=lambda: Node(""), init=False)
    _size: int = dt.field(init=False, default=0)

    def __len__(self) -> int:
        return self._size

    def __contains__(self, string: str) -> bool:
        assert isinstance(
            string, str
        ), f"Expected a string, got {type(string).__name__}"
        return _contains(self._root, string)

    def __str__(self) -> str:
        return f"Trie(size={self._size})"

    def __repr__(self) -> str:
        return f"<Trie size={self._size} at {hex(id(self))}>"

    def insert(self, string: str):
        inserted = _insert(self._root, string)
        self._size += inserted
        return inserted

    def __iter__(self) -> ty.Iterator[str]:
        return _iterate(self._root, "")


trie = Trie()
trie.insert("cement")
trie.insert("cemetry")
trie.insert("chair")
trie.insert("cent")
trie.insert("change")
trie.insert("changes")
trie.insert("apple")
trie.insert("applet")
trie.insert("ape")
trie.insert("c")
trie.insert("")

print(len(trie), list(trie), trie)
