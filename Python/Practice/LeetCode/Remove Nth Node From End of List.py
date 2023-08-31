# Given the head of a linked list, remove the nth node from the end of the list and return its head.

class Node(object):
    def __init__(self, val=None, next_=None):
        self.data = val
        self.next = next_


class LinkedList(object):
    def __init__(self):
        self.head = None

    def printer(self):
        ptr = self.head
        while ptr:
            print(ptr.data)
            ptr = ptr.next_


