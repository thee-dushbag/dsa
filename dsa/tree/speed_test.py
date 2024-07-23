import dataclasses as dt, typing as ty
from . import generic as t, traversal as tr

nodify_loop = t.nodify
nodify_loop.__name__ = "nodify_loop"


@dt.dataclass(slots=True, order=False)
class Node[T]:
    value: T
    left: "Node[T] | None" = dt.field(repr=False, default=None)
    right: "Node[T] | None" = dt.field(repr=False, default=None)

    def values(self):
        return (node.value for node in t.inorder(self))

    __len__ = t.length


def connect[T](parent: Node[T], left: Node[T] | None, right: Node[T] | None):
    parent.left = left
    parent.right = right


def _nodify_helper[
    Node, T
](connect: t.Connector[Node], create: t.Creator[Node, T], values: ty.Sequence[T]) -> (
    Node | None
):
    if not values:
        return
    mid = round(len(values) / 2)
    left = _nodify_helper(connect, create, values[:mid])
    right = _nodify_helper(connect, create, values[mid + 1 :])
    parent = create(values[mid])
    connect(parent, left, right)
    return parent


def nodify_recursion[
    Node, T
](
    connect: t.Connector[Node],
    create: t.Creator[Node, T],
    iterable: ty.Iterable[T],
    size: int | None = None,
) -> Node:
    iterable = list(iterable)
    if size is not None and size != len(iterable):
        raise ValueError(size)
    root = _nodify_helper(connect, create, iterable)
    if root is None:
        raise ValueError(size)
    return root


def test_nodifiers(n: int = 20):
    iterable = range(n)
    root1 = nodify_loop(connect, Node[int], iterable, n)
    root2 = nodify_recursion(connect, Node[int], iterable, n)
    assert list(root1.values()) == list(root2.values())
    root2r = ty.cast(tr.Node[int], root2)
    assert t.height(root2r) == tr.height(root2r)
    assert t.length(root2r) == tr.length(root2r)


@dt.dataclass(slots=True)
class TimerResult[T]:
    results: list[T]
    lapse: float
    runs: int

    @property
    def average(self) -> float:
        return self.lapse / self.runs


def timer[
    **P, T
](function: ty.Callable[P, T], n: int | None = None) -> ty.Callable[P, TimerResult[T]]:
    n = 3 if n is None else n
    assert n > 0, n

    def _timeit(*args: P.args, **kwargs: P.kwargs) -> TimerResult[T]:
        from time import perf_counter

        results: list[T] = []
        total_lapse: float = 0
        for _ in range(n):
            start = perf_counter()
            result = function(*args, **kwargs)
            lapse = perf_counter() - start
            results.append(result)
            total_lapse += lapse
        return TimerResult(results, total_lapse, n)

    return _timeit


def timeit[
    **P
](runs: int, function: ty.Callable[P, object], *args: P.args, **kwargs: P.kwargs):
    r = timer(function, runs)(*args, **kwargs)
    print(f"{function.__name__} took: Average: {r.average}s, Total: {r.lapse}s")


def nodify_speed_test(n: int, runs: int):
    timeit(runs, nodify_recursion, connect, Node[int], range(n), n)
    timeit(runs, nodify_loop, connect, Node[int], range(n), n)


type _Orderer[Node: t.INode] = ty.Callable[[Node | None], ty.Iterable[Node]]
type Orderer[T] = _Orderer[Node[T]]
type Orderers[T] = ty.Sequence[_Orderer[Node[T]]]


def _order_speed_test[T](tree: Node[T], runs: int, orderer: Orderer[T]):
    def func(node: Node[T] | None) -> list[Node[T]]:
        return list(orderer(node))

    func.__name__ = orderer.__name__
    timeit(runs, func, tree)


def _[**P, T](func: ty.Callable[P, T]) -> ty.Callable[P, T]:
    func.__name__ = f"{func.__module__}.{func.__name__}"
    return func


def order_speed_test(n: int, runs: int):
    root = t.nodify(connect, Node[int], range(n), n)
    orderers = (
        _(t.inorder),
        _(tr.inorder),
        _(t.preorder),
        _(tr.preorder),
        _(t.postorder),
        _(tr.postorder),
    )
    orderers = ty.cast(ty.Iterable[Orderer[int]], orderers)

    for orderer in orderers:
        _order_speed_test(root, runs, orderer)


def height_speed_test(n: int, runs: int):
    root = t.nodify(connect, Node[int], range(n), n)
    root = ty.cast(tr.Node[int], root)
    timeit(runs, _(t.height), root)
    timeit(runs, _(tr.height), root)
    timeit(runs, _(t.length), root)
    timeit(runs, _(tr.length), root)


if __name__ == "__main__":
    # order_speed_test(1_500_000, 10)
    # height_speed_test(5_000_000, 2)
    # order_speed_test(2_500_000, 10)
    nodify_speed_test(5_000_000, 5)
