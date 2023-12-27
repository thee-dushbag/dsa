from .base import BaseLinkedList
from .node import ForwardNode


class SinglyLinkedList(BaseLinkedList):
    nodetype = ForwardNode

    @staticmethod
    def _init(node, snode):
        snode.next = node

    @staticmethod
    def _fromiter(temp, nextnode):
        temp.next = nextnode

    def pushright(self, node):
        self._pushright(node, self._init)

    def pushleft(self, node):
        self._pushleft(node, self._init)

    def popnode(self, index):
        def popper(index):
            if index == 0:
                node = self.head
                self.head = self.head.next
            else:
                pnode = self.getnode(index - 1)
                node = pnode.next
                pnode.next = node.next
            return node

        return self._popnode(index, popper)

    def __reversed__(self):
        return self.__class__(reversed(list(self)))

    def addat(self, index, node):
        def adder(index, node):
            pnode = self.getnode(index - 1)
            node.next = pnode.next
            pnode.next = node

        self._addat(index, node, adder)

    def shift(self, value):
        if self.head is None:
            return
        shifter = lambda node: node.next
        if value < 0:
            value = self.size + value
        value = value % self.size
        firstnode = self.head
        lastnode = None
        while value:
            lastnode = firstnode
            firstnode = shifter(firstnode)
            value -= 1
        if lastnode:
            lastnode.next = None
        self.head = firstnode

    def _addtail(self, tail):
        lastnode = self.getnode(-1)
        lastnode.next = tail
