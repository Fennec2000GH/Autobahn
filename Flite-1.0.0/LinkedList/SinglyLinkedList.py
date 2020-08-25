
from __future__ import annotations
import copy
from abc import ABC
from typing import Any, Sized

from LinkedList.LinkedListABC import Node


class SinglyLinkedNode(Node, ABC):
    """Node for singly linked list"""

    # METHODS
    def __init__(self, val: Any, next: SinglyLinkedNode = None) -> None:
        """Node initializer"""
        # Check for valid arguments
        if isinstance(next, SinglyLinkedNode):
            raise TypeError('next must be of type Node')
        self.__val = val
        self.__next = next

    def __repr__(self) -> str:
        """
        Representation of node

        :return: official str representation of node
        """
        return f'Node(val={str(self.__val)}, next=Node({str(self.__next.__val)}, ...)'

    def __str__(self) -> str:
        """
        Representation of node as printed str

        :return: str when applying print to node
        """
        return f'{self.__val}'

    def __eq__(self, other: SinglyLinkedNode) -> bool:
        """
        Check for node value equality

        :param other: Another node to compare for equality
        :return: True if other has an equal val attribute value as self
        """
        # Check for valid arguments
        if isinstance(other, SinglyLinkedNode):
            raise TypeError('other must be of type Node')
        return self.__val == other.__val

    # PROPERTIES
    @property
    def val(self) -> Any:
        """
        Current value of node

        :return: object in the val attribute
        """
        return self.__val

    @val.setter
    def val(self, new_val: Any) -> None:
        """
         Sets new value for val attribute

        :param new_val: New value for val attribute
        :return: None
        """
        # Checking for valid arguments
        if new_val is None:
            raise ValueError('new_val cannot be None')
        self.__val = new_val

    @property
    def next(self) -> SinglyLinkedNode:
        """
        Gets the next node in the linked list

        :return: Node object that comes next sequentially
        """
        return self.__next

    @next.setter
    def next(self, new_next: SinglyLinkedNode) -> None:
        """
        Sets new node to be the next node

        :param new_next: New node for the next attribute
        :return: None
        """
        # Checking for valid arguments
        if isinstance(new_next, SinglyLinkedNode):
            raise TypeError('new_node must be of type Node')
        self.__next = new_next


class SinglyLinkedList(object):
    """Simple implementation of a single linked list"""

    def __init__(self, __iterable: Sized = None, capacity: int = None) -> None:
        """Singly linked list initializer"""
        # Checking for valid arguments
        if __iterable is not None and not isinstance(__iterable, Sized):
            raise TypeError('__iterable must be of type Iterable')
        if capacity is not None and type(capacity) != int:
            raise TypeError('capacity must be of type int')
        if capacity is not None and len(__iterable):
            raise ValueError('__iterable must have a size equal to or less than capacity')

        # Assigning attributes
        if __iterable is None or len(__iterable) == 0:
            self.__head = None
            self.__tail = None
        else:
            self.__head = SinglyLinkedNode(val=copy.deepcopy(x=__iterable[0]))
            curr = self.__head  # Current node in linked list building
            for index in range(1, len(__iterable)):
                curr.__next = copy.deepcopy(x=__iterable[index])
                curr = curr.__next
            self.__tail = curr

        self.__capacity = capacity
        self.__size = len(__iterable)

    def __len__(self) -> int:
        """
        Gets number of elements in linked list

        :return: int denoting the size of linked list
        """
        return self.__size

    def __eq__(self, other: SinglyLinkedList) -> bool:
        """
        Check for equality between two singly linked lists

        :return: True if each node in both linked lists match in value, otherwise False
        """
        # Edge cases
        if other is None or self.__size != other.__size:
            return False
        curr = self.__head
        curr_other = other.__head
        for index in range(self.__size):
            if curr != curr_other:
                return False
        return True
