
from __future__ import annotations
from multimethod import multimethod
import math
import numpy as np
from typing import Any, Collection, Optional

from LinkedList.LinkedListABC import Node, LinkedList


class UnrolledNode(Node):
    """Node implementation for unrolled linked list"""

    def __init__(self, vals: Collection, capacity: int = 10) -> None:
        """
        Unrolled linked list initializer

        :param vals: Collection of values to initilly fill node
        :param capacity: Maximum number of values node can hold
        :return: None
        """
        super().__init__()

        # Checking for valid arguments
        if not type(capacity) != int:
            raise TypeError('capacity must be of type int')
        if capacity <= 0:
            raise ValueError('capacity must be positive')
        if len(vals) > capacity:
            raise ValueError('The number of values for initialization must not exceed capacity')

        # Assigning attributes
        self.__capacity = capacity
        self.__array = np.empty(shape=(self.__capacity,), dtype=Any)
        self.__index = 0

        for index, item in enumerate(iterable=vals, start=0):
            self.__array[index] = item

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

    # METHODS
    def __init__(self, vals: Collection = None, capacity: int = None, node_capacity: int = 10, loadfactor: int = 0.5) -> None:
        """
        Unrolled linked list initializer

        :param vals: Collection of values to append to unrolled linked list
        :param capacity: Uniform capacity of values per unrolled node
        :param loadfactor: The minimum ratio of capacity filled up in a node at all times, otherwise modifications to
        unrolled linked list are made to re-satisfy the condition
        :return: None
        """
        super().__init__()

        # Check for valid arguments
        if vals is not None and not isinstance(vals, Collection):
            raise TypeError('vals must be of type Iterable')
        if capacity is not None and type(capacity) != int:
            raise TypeError('capacity must be of type int')
        if type(loadfactor) != float:
            raise TypeError('loadfactor must be of type float')
        if loadfactor <= 0 or loadfactor > 0.5:
            raise ValueError('loadfactor must be more than 0 and less than or equal to 0.5 for efficiency reasons')

        self._capacity = capacity
        self.__node_capacity = node_capacity
        self._size = 0
        self.__loadfactor = loadfactor
        self.__head = None
        if vals is not None and len(vals) > 0:
            mean_vals_per_node = self.__loadfactor * self.__node_capacity + 1
            self._size = len(vals) // int(mean_vals_per_node)
            remainder =math.remainder(__x=len(self), __y=int(self.__node_capacity / 2 + 1))
            self.__head = UnrolledNode(vals=vals[mean_vals_per_node + 1])
            for node_index in range(1, len(self)):
                pass

    # PROPERTIES
    @property
    @abstractmethod
    def head(self) -> Optional[Node]:
        """
        Head of linked list

        :return: First node of linked list, if not empty, otherwise None
        """
        pass

    @property
    @abstractmethod
    def tail(self) -> Optional[Node]:
        """
        Tail of linked list

        :return: Last node of linked list, if not empty, otherwise None
        """
        pass

    # ACCESSORS
    @abstractmethod
    @multimethod
    def contains(self, node: Node) -> bool:
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
    def contains(self, nodes: Collection[Node]) -> bool:
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
    def push_back(self, node: Node) -> None:
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
    def push_front(self, node: Node) -> None:
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
    def move_before(self, node_to_move: Node, node_referenced: Node) -> None:
        """
        Move node existing in linked list to right before another node existing in the same linked list.
        Linked list is not modified if either node does not exist within the linked list.

        :param node_to_move: Node to be moved
        :param node_referenced: Node marking location where the other node moves before
        :return: None
        """
        pass

    @abstractmethod
    def move_after(self, node_to_move: Node, node_referenced: Node) -> None:
        """
        Move node existing in linked list to right after another node existing in the same linked list.
        Linked list is not modified if either node does not exist within the linked list.

        :param node_to_move: Node to be moved
        :param node_referenced: Node marking location where the other node moves after
        :return: None
        """
        pass

    @abstractmethod
    @multimethod
    def insert_before(self, node_to_insert: Node, node_referenced: Node, **kwargs) -> None:
        """
        Insert node which does not belong to any linked list right before some existing node in linked list.
        Linked list is not modified if the node intended for insertion is already part of another linked list.

        :param node_to_insert: Node to be inserted
        :param node_referenced: Node marking location where the other node moves after
        :return: None
        """
        pass

    @abstractmethod
    @multimethod
    def insert_before(self, val: Any, node_referenced: Node, **kwargs) -> None:
        """
        Insert new node with given value right before some existing node in linked list.

        :param val: Value to insert
        :param node_referenced: Node marking location where the other node moves after
        :return: None
        """
        pass

    @abstractmethod
    @multimethod
    def insert_after(self, node_to_insert: Node, node_referenced: Node, **kwargs) -> None:
        """
        Insert node which does not belong to any linked list right after some existing node in linked list.
        Linked list is not modified if the node intended for insertion is already part of another linked list.

        :param node_to_insert: Node to be inserted
        :param node_referenced: Node marking location where the other node moves after
        :return: None
        """
        pass

    @abstractmethod
    @multimethod
    def insert_after(self, val: Any, node_referenced: Node, **kwargs) -> None:
        """
        Insert new node with given value right after some existing node in linked list.

        :param val: Value to insert
        :param node_referenced: Node marking location where the other node moves after
        :return: None
        """
        pass

    @abstractmethod
    def swap(self, node1: Node, node2: Node) -> None:
        """
        Swap values for two existing nodes in linked list. If one or both nodes do not exist in the linked list,
        the linked list is not modified.

        :param node1: First node
        :param node2: Second node
        :return: None
        """
        pass
