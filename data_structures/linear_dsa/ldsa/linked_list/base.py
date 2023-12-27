from .abc_ import LinkedListOpsABC


class BaseLinkedList(LinkedListOpsABC):
    def __init__(self, iterable=None):
        self.head, self.size = self.fromiter(iterable)

    def fromiter(self, iterable):
        if iterable is None:
            return None, 0
        head, size = self.nodetype(), 0
        temp = head
        for value in iterable:
            self._fromiter(temp, self.nodetype(value))
            temp = temp.next
            size += 1
        return head.next, size

    @staticmethod
    def _fromiter(temp, nextnode):
        raise NotImplementedError

    def _nodeiter(self):
        head = self.head
        while head is not None:
            yield head
            head = head.next

    def getnode(self, index):
        if index < 0:
            index = self.size + index
        if index < self.size:
            for cindex, node in enumerate(self._nodeiter()):
                if cindex == index:
                    return node
        raise IndexError

    def _push(self, node1, node2, init):
        node1.clear()
        if self.empty():
            self.head = node1
            return
        init(node1, node2())
        self.size += 1

    def _pushright(self, node, init):
        self._push(node, lambda: self.getnode(-1), init)

    def _pushleft(self, node, init):
        self._push(node, lambda: self.head, init)

    def popleft(self):
        return self.popnode(0)

    def popright(self):
        return self.popnode(-1)

    def _addat(self, index, node, adder):
        try:
            if index == 0:
                self.pushleft(node)
            else:
                self.size += 1
                adder(index, node)
        except IndexError:
            self.pushright(node)

    def _popnode(self, index, popper):
        if self.empty():
            raise IndexError
        node = popper(index)
        node.clear()
        self.size -= 1
        return node
