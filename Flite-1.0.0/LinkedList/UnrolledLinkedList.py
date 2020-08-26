
from __future__ import annotations
from multimethod import multimethod
import numpy as np
from typing import Any, Optional

from LinkedList.LinkedListABC import Node, LinkedList


class UnrolledNode(Node):
    """Node implementation for unrolled linked list"""

    def __init__(self, capacity: int = 10) -> None:
        super(Node, self).__init__()
        self.__capacity = capacity
        self.__array = np.empty(shape=(self.__capacity,), dtype=Any)
        self.__index = 0

    # PROPERTIES
    @property
    def val(self) -> Any:
        """
        Gets value in node

        :return: Value stored in node
        """
        return self.__array[self.__index]

    @val.setter
    def val(self, new_val: Any) -> None:
        """
        Sets value in node

        :param new_val: New value to replace current value in node
        :return: None
        """
        # Check for valid arguments
        if isinstance(new_val, Node):
            raise TypeError('new_val must be of any type besides Node or any subclass')
        self.__array[self.__index] = new_val

    @property
    def next(self) -> Optional[UnrolledNode]:
        """
        Gets next node sequentially in linked list

        :return: Node referenced by next property, otherwise None if current node is tail
        """
        if self.__index == self.__array.size - 1:
            if self.__next is None:
                return None
            self.__next.__index = 0
            return self.__next
        return self

    @next.setter
    def next(self, new_next: UnrolledNode) -> None:
        """
        Sets new node to be the next node

        :param new_next: New node for the next attribute
        :return: None
        """
        # Checking for valid arguments
        if not isinstance(new_next, UnrolledNode):
            raise TypeError('new_next must be of type UnrolledNode')

    @property
    def linkedlist(self) -> Optional[UnrolledLinkedList]:
        """
        Gets any linked list that owns the node

        :return: True if node is not part of any linked list, otherwise False
        """
        return self._linkedlist

    @linkedlist.setter
    def linkedlist(self, new_linkedlist: UnrolledLinkedList) -> None:
        """
        Sets a new linked list as owner of the node

        :param new_linkedlist: Linked list owner
        :return: None
        """
        # Checking for valid arguments
        if not isinstance(new_linkedlist, UnrolledLinkedList):
            raise TypeError('new_linkedlist must be of type UnrolledLinkedList')
        self._linkedlist = new_linkedlist


class UnrolledLinkedList(LinkedList):
    """Linked list implemented as sequence of arrays of contiguous nodes"""
    def __init__(self) -> None:
        pass



