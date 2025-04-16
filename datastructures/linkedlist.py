from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Optional, Sequence
from datastructures.ilinkedlist import ILinkedList, T


class LinkedList[T](ILinkedList[T]):

    @dataclass
    class Node:
        data: T
        next: Optional[LinkedList.Node] = None
        previous: Optional[LinkedList.Node] = None

    def __init__(self, data_type: type = object) -> None:
        self.head: Optional[LinkedList.Node] = None
        self.tail: Optional[LinkedList.Node] = None
        self.count: int = 0
        self.data_type = data_type
        self._iter_node: Optional[LinkedList.Node] = None

    @staticmethod
    def from_sequence(sequence: Sequence[T], data_type: type=object) -> LinkedList[T]:
        linkedlist = LinkedList(data_type)
        for item in sequence:
            linkedlist.append(item)
        return linkedlist

    def append(self, item: T) -> None:
        if not isinstance(item, self.data_type):
            raise TypeError(f"Expected {self.data_type}, got {type(item)}.")
        
        new_node = LinkedList.Node(data = item)
        if self.head is None:
            self.head = self.tail = new_node
        else:
            assert self.tail is not None
            self.tail.next = new_node
            new_node.previous = self.tail
            self.tail = new_node
        self.count += 1

    def prepend(self, item: T) -> None:
        if not isinstance(item, self.data_type):
            raise TypeError(f"Expected {self.data_type}, got {type(item)}.")
        
        new_node = LinkedList.Node(data = item)
        if self.head is None:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.previous = new_node
            self.head = new_node
        self.count += 1

    def insert_before(self, target: T, item: T) -> None:
        if not isinstance(item, self.data_type) or not isinstance(target, self.data_type):
            raise TypeError(f"Expected {self.data_type}.")
        
        current = self.head
        while current:
            if current.data == target:
                new_node = LinkedList.Node(data = item, next = current, previous = current.previous)
                if current.previous:
                    current.previous.next = new_node
                else:
                    self.head = new_node
                current.previous = new_node
                self.count += 1
                return
            current = current.next
        raise ValueError(f"{target} is not in the list.")

    def insert_after(self, target: T, item: T) -> None:
        if not isinstance(item, self.data_type) or not isinstance(target, self.data_type):
            raise TypeError(f"Expected {self.data_type}.")
        
        current = self.head
        while current:
            if current.data == target:
                new_node = LinkedList.Node(data = item, previous = current, next = current.next)
                if current.next:
                    current.next.previous = new_node
                else:
                    self.tail = new_node
                current.next = new_node
                self.count += 1
                return
            current = current.next
        raise ValueError(f"{target} is not in the list.")

    def remove(self, item: T) -> None:
        if not isinstance(item, self.data_type):
            raise TypeError(f"Expected {self.data_type}.")
        
        current = self.head
        while current:
            if current.data == item:
                if current.previous:
                    current.previous.next = current.next
                else:
                    self.head = current.next
                if current.next:
                    current.next.previous = current.previous
                else:
                    self.tail = current.previous
                self.count -= 1
                return
            current = current.next
        raise ValueError(f"{item} is not in the list.")

    def remove_all(self, item: T) -> None:
        if not isinstance(item, self.data_type):
            raise TypeError(f"Expected {self.data_type}.")
        
        current = self.head
        while current:
            next_node = current.next
            if current.data == item:
                if current.previous:
                    current.previous.next = current.next
                else:
                    self.head = current.next
                if current.next:
                    current.next.previous = current.previous
                else:
                    self.tail = current.previous
                self.count -= 1
            current = next_node

    def pop(self) -> T:
        if self.tail is None:
            raise IndexError("You cannot pop from an empty list.")
        
        data = self.tail.data
        if self.tail.previous:
            self.tail = self.tail.previous
            self.tail.next = None
        else:
            self.head = self.tail = None
        self.count -= 1
        return data

    def pop_front(self) -> T:
        if self.head is None:
            raise IndexError("You cannot pop from an empty list.")
        
        data = self.head.data
        if self.head.next:
            self.head = self.head.next
            self.head.previous = None
        else:
            self.head = self.tail = None
        self.count -= 1
        return data

    @property
    def front(self) -> T:
        if self.head is None:
            raise IndexError("The list is empty.")
        return self.head.data

    @property
    def back(self) -> T:
        if self.tail is None:
            raise IndexError("The list is empty.")
        return self.tail.data

    @property
    def empty(self) -> bool:
        return self.count == 0

    def __len__(self) -> int:
        return self.count

    def clear(self) -> None:
        self.head = None
        self.tail = None
        self.count = 0
        self._iter_node = None

    def __contains__(self, item: T) -> bool:
        current = self.head
        while current:
            if current.data == item:
                return True
            current = current.next
        return False

    def __iter__(self) -> ILinkedList[T]:
        self._iter_node = self.head
        return self

    def __next__(self) -> T:
        if self._iter_node is None:
            raise StopIteration
        data = self._iter_node.data
        self._iter_node = self._iter_node.next
        return data
    
    def __reversed__(self) -> ILinkedList[T]:
        current = self.tail
        reversed_list = LinkedList(self.data_type)
        while current:
            reversed_list.append(current.data)
            current = current.previous
        return reversed_list
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ILinkedList):
            return False
        if len(self) != len(other):
            return False
        return all(a == b for a, b in zip(self, other)) # Compares each pair of elements from both lists using zip(). If all corresponding elements are equal, the lists are considered equal.

    def __str__(self) -> str:
        items = []
        current = self.head
        while current:
            items.append(repr(current.data))
            current = current.next
        return '[' + ', '.join(items) + ']'

    def __repr__(self) -> str:
        items = []
        current = self.head
        while current:
            items.append(repr(current.data))
            current = current.next
        return f"LinkedList({' <-> '.join(items)}) Count: {self.count}"


if __name__ == '__main__':
    filename = os.path.basename(__file__)
    print(f'OOPS!\nThis is the {filename} file.\nDid you mean to run your tests or program.py file?\nFor tests, run them from the Test Explorer on the left.')
