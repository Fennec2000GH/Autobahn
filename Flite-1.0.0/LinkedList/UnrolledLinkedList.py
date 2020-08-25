
from __future__ import annotations
from multimethod import multimethod
import numpy as np
from typing import Union

from LinkedList.LinkedListABC import Node, LinkedList


class UnrolledNode(Node):
    """Node implementation for unrolled linked list"""

    def __init__(self, capacity: int = 10) -> None:
        self.__capacity = capacity
        self.__array = np.empty(shape=(self.__capacity,), dtype=object)
        self.__index = 0
        self.__next = None

    # PROPERTIES
    @property
    def val(self) -> np:
        """

        :return:
        """
    @property
    def next(self) -> UnrolledNode:
        """

        :param self:
        :return:
        """
        if self.__index == self.__array.size - 1:
            return self.__next
        self.__index += 1
        return self

    @next.setter
    @multimethod
    def next(self, new_next: UnrolledNode) -> None:
        """

        :param new_next:
        :return:
        """
        self.__next = new_next

    @next.setter
    @multimethod
    def next(self, new_next: Union[int, float, str, bool]) -> None:
        """

        :param new_next:
        :return:
        """
        if self.__index == self.__array.size - 1:
            if self.__next is None:
                self.__next = UnrolledNode(capacity=self.__capacity)
            self.__next.__array[0] = new_next


class UnrolledLinkedList(LinkedList):
    """Linked list implemented as sequence of arrays of contiguous nodes"""
    def __init__(self) -> None:
        pass



