
from __future__ import annotations
from abc import ABC, abstractmethod
from multimethod import multimethod
from typing import Any, Collection, Optional


class AbstractNode(ABC):
    """Abstract class for linked list node"""

    # METHODS
    def __init__(self) -> None:
        """
        Node initializer simply holds protected linked list attribute.

        :return: None
        """
        self._linkedlist = None

    # PROPERTIES
    @property
    @abstractmethod
    def val(self) -> Any:
        """
        Gets value in node

        :return: Value stored in node
        """
        pass

    @val.setter
    @abstractmethod
    def val(self, new_val: Any) -> None:
        """
        Sets value in node

        :param new_val: New value to replace current value in node
        :return: None
        """
        pass

    @property
    @abstractmethod
    def linkedlist(self) -> Optional[AbstractLinkedList]:
        """
        Gets any linked list that owns the node

        :return: True if node is not part of any linked list, otherwise False
        """
        pass


class AbstractLinkedList(ABC):
    """Abstract class for linked list"""

    # METHODS
    def __init__(self) -> None:
        """
        Linked list initializer simply holds protected size and capacity attributes.

        :return: None
        """
        self._capacity = None
        self._size = 0

    def __len__(self) -> int:
        """
        Gets number of elements in linked list

        :return: Integer denoting the size of linked list
        """
        return self._size

    # PROPERTIES
    @property
    def capacity(self) -> Optional[int]:
        """
        Gets the capacity

        :return: None if no capacity was set during initialization, otherwise a positive integer
        """
        return self._capacity

    # ACCESSORS
    @abstractmethod
    @multimethod
    def contains(self, node: AbstractNode) -> bool:
        """
        Checks whether given node is a contained reference in linked list

        :param node: Node to check for existence
        :return: True if node exists in linked list, otherwise False
        """
        pass

    @abstractmethod
    @multimethod
    def contains(self, val: Any) -> bool:
        """
        Checks whether given value is in some contained node reference in linked list

        :param val: Value to check for existence
        :return: True if node with val exists in linked list, otherwise False
        """
        pass

    @abstractmethod
    @multimethod
    def contains(self, nodes: Collection[AbstractNode]) -> bool:
        """
        Checks whether each node in nodes exists in linked list.

        :param nodes: Collection of nodes
        :return: True if each node in given collection of nodes is in linked list, otherwise False
        """
        pass

    @abstractmethod
    @multimethod
    def contains(self, vals: Collection[Any]) -> bool:
        """
        Checks whether each value in vals exists in any node in linked list

        :param vals: Collection of values of any type
        :return: True if each value in given collection of values is in any node in linked list, otherwise False
        """
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        """
        Check if there are currently no nodes in linked list

        :return: True if no nodes exist yet in linked list, otherwise False
        """
        pass

    # MUTATORS
    @abstractmethod
    @multimethod
    def push_back(self, node: AbstractNode) -> None:
        """
        Appends given node to end of linked list. Linked list is not modified if node already belongs
        to this linked list or another linked list.

        :param node: Node to append
        :return: None
        """
        pass

    @abstractmethod
    @multimethod
    def push_back(self, val: Any) -> None:
        """
        Appends new node with given value to end of linked list.

        :param val: Value to append
        :return: None
        """
        pass

    @abstractmethod
    @multimethod
    def push_front(self, node: AbstractNode) -> None:
        """
        Prepends given node to front of linked list. Linked list is not modified if node already belongs
        to this linked list or another linked list.

        :param node: Node to prepend
        :return: None
        """
        pass

    @abstractmethod
    @multimethod
    def push_front(self, val: Any) -> None:
        """
        Prepends new node with given value to front of linked list.

        :param val: Value to prepend
        :return: None
        """
        pass

    @abstractmethod
    def swap(self, node1: AbstractNode, node2: AbstractNode) -> None:
        """
        Swap values for two existing nodes in linked list. If one or both nodes do not exist in the linked list,
        the linked list is not modified.

        :param node1: First node
        :param node2: Second node
        :return: None
        """
        pass
