from bst import BinarySearchTree
from sys import setrecursionlimit
from typing import Callable
# from faker import Faker
from mpack import timer
from random import choices, shuffle

timer.FUNCTION_CALL_STR = "[{function_name}({args}, {kwargs})]"
timer.TAKEN_TIME_STR = "{target}: Took {lapse._time} seconds."


Searcher = Callable[[str], timer.TimeitResult]


def linear_search(things: list[str]) -> tuple[str, Searcher]:
    @timer.timer_sync
    def searcher(thing: str):
        for t in things:
            if t == thing:
                return True

    return "Linear", searcher


def binary_search(things: list[str]) -> tuple[str, Searcher]:
    things = sorted(things)

    @timer.timer_sync
    def searcher(thing: str):
        if not things:
            return
        high, low = len(things), 0
        while True:
            mid = ((high - low) // 2) + low
            current = things[mid]
            if current == thing:
                return True
            elif current < thing:
                low = mid
            else:
                high = mid

    return "Binary", searcher


def bst_search(things: list[str]) -> tuple[str, Searcher]:
    bst = BinarySearchTree(things)

    @timer.timer_sync
    def searcher(thing: str):
        return bst.find(thing)

    return "BST", searcher


def take_things(things: list[str], n: int) -> list[str]:
    return choices(things, k=n)


def average_speed(name: str, searcher: Searcher, things: list[str]):
    average = sum(searcher(thing).lapse._time for thing in things)
    return f"{name} search took {average} seconds."


def main():
    things = list(map(str, range(10_000_000)))
    shuffle(things)
    searchers = [
        # linear_search(things),
        binary_search(things),
        bst_search(things),
    ]
    print("Loaded")
    tofind = take_things(things, 10)
    for name, searcher in searchers:
        print(average_speed(name, searcher, tofind))


if __name__ == "__main__":
    main()
