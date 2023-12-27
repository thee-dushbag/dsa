from .base import BaseLinkedList
from .node import Node


class DoublyLinkedList(BaseLinkedList):
    nodetype = Node

    @staticmethod
    def _init(node, snode):
        snode.next = node
        node.prev = snode

    @staticmethod
    def _fromiter(temp, nextnode):
        temp.next = nextnode
        nextnode.prev = temp

    def pushright(self, node):
        self._pushright(node, self._init)

    def pushleft(self, node):
        self._pushleft(node, self._init)

    def popnode(self, index):
        def popper(index):
            if index == 0:
                node = self.head
                self.head = node.next
                self.head.prev = None
            else:
                node = self.getnode(index)
                if node.prev is not None:
                    node.prev.next = node.next
                if node.next is not None:
                    node.next.prev = node.prev
            return node

        return self._popnode(index, popper)

    def addat(self, index, node):
        def adder(index, node):
            pnode = self.getnode(index)
            pnode.prev.next = node
            node.prev = pnode.prev
            pnode.prev = node
            node.next = pnode

        self._addat(index, node, adder)

    def _addtail(self, tail):
        lastnode = self.getnode(-1)
        lastnode.next = tail
        tail.prev = lastnode

    def shift(self, value):
        if self.head is None:
            return
        fshift = lambda node: node.next
        rshift = lambda node: node.prev
        shifter = rshift if value < 0 else fshift
        value = abs(value) % self.size
        lastnode = self.getnode(-1)
        firstnode = self.head
        lastnode.next = firstnode
        firstnode.prev = lastnode
        while value:
            firstnode = shifter(firstnode)
            value -= 1
        lastnode = firstnode.prev
        firstnode.prev = None
        lastnode.next = None
        self.head = firstnode
