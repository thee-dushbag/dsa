import dataclasses as dt
import typing as ty
import heapq
import enum

type FreqTable = ty.Mapping[str, int]
type CodesTable = ty.Mapping[str, str]


def build_freq_table(string: str) -> FreqTable:
    return ty.Counter(string)


@dt.dataclass(slots=True, order=True)
class Node:
    freq: int = dt.field(compare=True)
    chars: set[str] = dt.field(compare=False)
    left: ty.Union["Node", None] = dt.field(compare=False, default=None)
    right: ty.Union["Node", None] = dt.field(compare=False, default=None)


def build_freq_tree(freq_table: FreqTable) -> Node:
    pqueue: list[Node] = [Node(freq, {char}) for char, freq in freq_table.items()]
    heapq.heapify(pqueue)
    while len(pqueue) > 1:
        right = heapq.heappop(pqueue)
        left = heapq.heappop(pqueue)
        parent = Node(left.freq + right.freq, left.chars | right.chars, left, right)
        heapq.heappush(pqueue, parent)
    return pqueue.pop()


class LeftRight(enum.StrEnum):
    NONE = ""
    LEFT = "0"
    RIGHT = "1"


def build_codes_table(tree: Node) -> CodesTable:
    codes: dict[str, str] = {}
    lr = LeftRight.LEFT if len(tree.chars) == 1 else LeftRight.NONE
    stack: list[tuple[Node, tuple[LeftRight, ...]]] = [(tree, (lr,))]
    while stack:
        node, lr = stack.pop()
        if node.left is None and node.right is None:
            codes[node.chars.pop()] = "".join(lr)
            continue
        if node.left is not None:
            stack.append((node.left, (*lr, LeftRight.LEFT)))
        if node.right is not None:
            stack.append((node.right, (*lr, LeftRight.RIGHT)))
    return codes


def encode_str_bits(string: str, codes: CodesTable) -> str:
    return "".join(codes[char] for char in string)


def decode_str_bits(compressed: str, codes: CodesTable) -> str:
    charcodes = {code: char for char, code in codes.items()}
    buffer, deflated = "", list[str]()
    for bit in compressed:
        buffer += bit
        try:
            deflated.append(charcodes[buffer])
        except KeyError:
            ...
        else:
            buffer = ""
    if buffer:
        raise KeyError("Missing character for code %r" % buffer)
    return "".join(deflated)


def main(text: str):
    freq_table = build_freq_table(text)
    node = build_freq_tree(freq_table)
    codes = build_codes_table(node)
    compressed = encode_str_bits(text, codes)
    original = "".join(map(lambda b: bin(b)[2:].rjust(8, "0"), text.encode()))
    length = len(original)
    clength = len(compressed)
    deflated = decode_str_bits(compressed, codes)
    print(f"InputTextSize: {length} bits")
    print(f"CompressedSize: {clength} bits")
    print(f"SpaceSaving: {round((length - clength) / length * 100, 2)}%")
    assert deflated == text, "mismatch: %r != %r" % (text, deflated)


if __name__ == "__main__":
    # text = "aaaaabbbbcccdde"
    import sys

    text = sys.stdin.buffer.read()
    main(ascii(text))
