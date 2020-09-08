
from __future__ import annotations
from deprecated import deprecated
import itertools
from multimethod import multimethod
import math
import numpy as np
from typing import Any, Collection, Optional

from LinkedList.LinkedListABC import AbstractLinkedList


class UnrolledNode:
    """Node implementation for unrolled linked list"""

    def __init__(self, node_capacity: int, iterable: Collection = None) -> None:
        """
        Unrolled linked list initializer

        :param iterable: Collection of values to initially fill node
        :param node_capacity: Maximum number of values node can hold
        :return: None
        """
        super(UnrolledNode, self).__init__()

        # Checking for valid arguments
        if not type(node_capacity) != int:
            raise TypeError('capacity must be of type int')
        if node_capacity <= 0:
            raise ValueError('capacity must be positive')
        if len(iterable) > node_capacity:
            raise ValueError('The number of values for initialization must not exceed capacity')

        # Assigning attributes
        self.__node_capacity = node_capacity
        self.__array = np.full(shape=(self.__node_capacity,), fill_value=np.nan, dtype=Any)

        # Initializing values from iterable
        for index, item in enumerate(iterable=iterable, start=0):
            self.__array[index] = item

    def __eq__(self, other: UnrolledNode) -> bool:
        """
        Check for equality between this and another unrolled node.

        :param other: Another unrolled node to compare to for equality
        :return: True if attribute values match and elements in array match stepwise, otherwise False
        """
        if not isinstance(other, UnrolledNode):
            return False
        if self.__node_capacity != other.__node_capacity:
            return False
        if self.__array.size != other.__array.size:
            return False
        for item1, item2 in zip(self.__array, other.__array):
            if item1 != item2:
                return False
        return True

    def __len__(self) -> int:
        """
        Gets the number of values stored in array.

        :return: Integer counting the number of values currently stored
        """
        return len([element for element in itertools.takewhile(predicate=lambda x: x is not np.nan, iterable=self.__array)])

    def __getitem__(self, item):

    # PROPERTIES
    @property
    def array(self) -> np.ndarray:
        """
        Gets entire array of values in UnrolledNode

        :return: Values stored in UnrolledNode
        """
        return self.__array

    @array.setter
    def array(self, new_array: Collection) -> None:
        """
        Sets new array of values in UnrolledNode

        :param new_array: New array of values to replace current array in UnrolledNode
        :return: None
        """
        # Check for valid arguments
        if not isinstance(new_array, Collection):
            raise TypeError('new_val must be of type Collection')
        if len(new_array) == 0:
            raise ValueError('new_val must have at least one element')
        self.__array = new_array


    @property
    def next(self) -> Optional[UnrolledNode]:
        """
        Gets next node sequentially in linked list

        :return: Node referenced by next property, otherwise None if current node is tail
        """
        if self.__index == self.__node_capacity - 1:
            if self._next is None:
                return None
            self._next.__index = 0
            return self._next
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
        self._next = new_next

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

    # ACCESSORS
    def contains(self, val: Any) -> bool:
        """
        Checks whether given value exists in unrolled node

        :param val: Value to check for existence
        :return: True if value in unrolled node array shows equality to val
        """
        return any([item == val for item in self.__array])


class UnrolledLinkedList(AbstractLinkedList):
    """Linked list implemented as sequence of arrays of contiguous nodes"""

    # METHODS
    def __init__(self, vals: Collection = None, capacity: int = None, node_capacity: int = 10,
                 loadfactor: int = 0.5) -> None:
        """
        Unrolled linked list initializer

        :param vals: Collection of values to append to unrolled linked list
        :param capacity: Maximum number of unrolled nodes allowed
        :param node_capacity: Uniform capacity of values per unrolled node in array
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
        self.__node_count = 0
        self.__loadfactor = loadfactor
        self.__head = self.__tail = None
        if vals is not None and len(vals) > 0:
            # mean number of values per node array during initialization
            mean_vals_per_node = int(self.__loadfactor * self.__node_capacity + 1)
            self._size = len(vals)  # Number of values
            self.__node_count = np.amax(a=[len(self) // mean_vals_per_node, 1], axis=None)
            remainder = math.remainder(__x=len(self), __y=mean_vals_per_node)
            self.__head = UnrolledNode(vals=vals[mean_vals_per_node + int(remainder != 0)], node_capacity=node_capacity)

            # Creating unrolled nodes after head
            curr = self.__head
            vals_index = mean_vals_per_node + int(remainder != 0)  # index corresponding to given vals collection
            for node_index in np.arange(1, self.__node_count):
                # Distributing one value extra due to non-zero remainder of leftover values after distributing values
                # evenly amongst nodes
                curr._next = UnrolledNode(vals=vals[vals_index: mean_vals_per_node + int(node_index < remainder)],
                                          node_capacity=node_capacity)
                vals_index += mean_vals_per_node + int(node_index < remainder)
                curr = curr._UnrolledNode_next
            self.__tail = curr

    # PROPERTIES
    @property
    def head(self) -> Optional[UnrolledNode]:
        """
        Head of linked list

        :return: First node of linked list, if not empty, otherwise None
        """
        return self.__head

    @property
    def tail(self) -> Optional[UnrolledNode]:
        """
        Tail of linked list

        :return: Last node of linked list, if not empty, otherwise None
        """
        return self.__tail

    @property
    def node_count(self) -> int:
        """
        Get the number of UnrolledNode objects linked list is composed from

        :return: Integer denoting the count of nodes
        """
        return self.__node_count

    # ACCESSORS
    @multimethod
    def contains(self, node: UnrolledNode) -> bool:
        """
        Checks whether given node is a contained reference in linked list

        :param node: Node to check for existence
        :return: True if node exists in linked list, otherwise False
        """
        # Checking for valid arguments
        if not isinstance(node, UnrolledLinkedList):
            raise TypeError('node must be of type SinglyLinkedNode')

        # Edge case
        if self.is_empty():
            return False

        # Searching for node in linked list
        curr = self.__head
        while curr is not None:
            if curr is node:
                return True
            curr = curr.next
        return False

    @multimethod
    def contains(self, val: Any) -> bool:
        """
        Checks whether given value is in some contained node reference in linked list

        :param val: Value to check for existence
        :return: True if node with val exists in linked list, otherwise False
        """
        # Edge case
        if self.is_empty():
            return False

        # Searching for node in linked list
        curr = self.__head
        while curr is not None:
            if curr.contains(val=val):
                return True
            curr = curr.next
        return False

    @multimethod
    def contains(self, nodes: Collection[UnrolledNode]) -> bool:
        """
        Checks whether each node in nodes exists in linked list.

        :param nodes: Collection of nodes
        :return: True if each node in given collection of nodes is in linked list, otherwise False
        """
        return all([self.contains(node=node) for node in nodes])

    @multimethod
    def contains(self, vals: Collection[Any]) -> bool:
        """
        Checks whether each value in vals exists in any node in linked list

        :param vals: Collection of values of any type
        :return: True if each value in given collection of values is in any node in linked list, otherwise False
        """
        return all([self.contains(val=val) for val in vals])

    def is_empty(self) -> bool:
        """
        Check if there are currently no nodes in linked list

        :return: True if no nodes exist yet in linked list, otherwise False
        """
        return self.__head is None

    # MUTATORS
    @multimethod
    @deprecated(version='1.0.0',
                reason='The concept of an individual "node" is repressented by a value stored in array')
    def push_back(self, node: UnrolledNode) -> None:
        """
        Appends given node to end of linked list. Linked list is not modified if node already belongs
        to this linked list or another linked list.

        :param node: Node to append
        :return: None
        """
        pass

    @multimethod
    def push_back(self, val: Any) -> None:
        """
        Appends new node with given value to end of linked list.

        :param val: Value to append
        :return: None
        """
        # Check for valid arguments
        if isinstance(val, UnrolledNode):
            raise TypeError('val can be of any type except Node or any derived classes')

        # Edge case
        if self.is_empty():
            self.__head = self.__tail = UnrolledNode(vals=[val], node_capacity=self.__node_capacity)

        # There is still space left before capacity is filled for unrolled node
        arr = self.__tail._UnrolledNode__array
        if len(arr) < self.__node_capacity:
            arr[len(arr)] = val

        # Array in unrolled node already filled up, leading to creation of new unrolled node ahead
        else:
            # index in tail array to start shifting final half of filled values to new unrolled node later pushed back
            start_index = int(self.__node_capacity * 0.5 + int(self.__node_capacity % 2 == 1))
            node = UnrolledNode(vals=arr[start_index:], node_capacity=self.__node_capacity)
            node._UnrolledNode__array[int(self.__node_capacity * 0.5)] = val

            # Replace originally shifted elements with None
            arr[start_index : self.__node_capacity] = np.repeat(a=[None], repeats=int(self.__node_capacity * 0.5), axis=None)
            self.__tail._UnrolledNode_next = node
            self.__tail = node

    @multimethod
    @deprecated(version='1.0.0', reason='The concept of an individual "node" is repressented by a value stored in array')
    def push_front(self, node: UnrolledNode) -> None:
        """
        Prepends given node to front of linked list. Linked list is not modified if node already belongs
        to this linked list or another linked list.

        :param node: Node to prepend
        :return: None
        """
        pass

    @multimethod
    def push_front(self, val: Any) -> None:
        """
        Prepends new node with given value to front of linked list.

        :param val: Value to prepend
        :return: None
        """
        # Checking for valid arguments
        if isinstance(val, UnrolledNode):
            raise TypeError('val can be of any type except Node or any derived classes')

        # Edge case
        if self.is_empty():
            self.__head = self.__tail = UnrolledNode(vals=[val], node_capacity=self.__node_capacity)

        # There is still space left before capacity is filled for unrolled node
        arr = self.__head._UnrolledNode__array
        if len(self.__head) < self.__node_capacity:
            for index in np.arange(len(self.__head), 1, -1):
                arr[index] = arr[index - 1]
            arr[0] = val

        # Array in unrolled node already filled up, leading to creation of new unrolled node ahead
        else:
            end_index = int(self.__node_capacity * 0.5)  # index after final element to be shifted left to prepended node
            node = UnrolledNode(vals=[val], node_capacity=self.__node_capacity)
            node._UnrolledNode__array[1 : end_index + 1] = arr[:end_index]
            arr[:end_index] = arr[end_index : self.__node_capacity]
            arr[end_index : self.__node_capacity] = np.repeat(a=[None],
                                                              repeats=self.__node_capacity - end_index,
                                                              axis=None)
            node._UnrolledNode_next = self.__head
            self.__head = node

    @deprecated(version='1.0.0', reason='move methods not supported for unrolled linked list structure')
    def move_before(self, node_to_move: UnrolledNode, node_referenced: UnrolledNode) -> None:
        """
        Move node existing in linked list to right before another node existing in the same linked list.
        Linked list is not modified if either node does not exist within the linked list.

        :param node_to_move: Node to be moved
        :param node_referenced: Node marking location where the other node moves before
        :return: None
        """
        pass

    @deprecated(version='1.0.0', reason='move methods not supported for unrolled linked list structure')
    def move_after(self, node_to_move: UnrolledNode, node_referenced: UnrolledNode) -> None:
        """
        Move node existing in linked list to right after another node existing in the same linked list.
        Linked list is not modified if either node does not exist within the linked list.

        :param node_to_move: Node to be moved
        :param node_referenced: Node marking location where the other node moves after
        :return: None
        """
        pass

    @multimethod
    @deprecated(version='1.0.0', reason='inserting relative to node position not supported for unrolled linked list structure')
    def insert_before(self, node_to_insert: UnrolledNode, node_referenced: UnrolledNode, **kwargs) -> None:
        """
        Insert node which does not belong to any linked list right before some existing node in linked list.
        Linked list is not modified if the node intended for insertion is already part of another linked list.

        :param node_to_insert: Node to be inserted
        :param node_referenced: Node marking location where the other node moves after
        :return: None
        """
        pass

    @multimethod
    @deprecated(version='1.0.0', reason='inserting relative to node position not supported for unrolled linked list structure')
    def insert_before(self, val: Any, node_referenced: UnrolledNode, **kwargs) -> None:
        """
        Insert new node with given value right before some existing node in linked list.

        :param val: Value to insert
        :param node_referenced: Node marking location where the other node moves after
        :return: None
        """
        pass

    @multimethod
    @deprecated(version='1.0.0', reason='inserting relative to node position not supported for unrolled linked list structure')
    def insert_after(self, node_to_insert: UnrolledNode, node_referenced: UnrolledNode, **kwargs) -> None:
        """
        Insert node which does not belong to any linked list right after some existing node in linked list.
        Linked list is not modified if the node intended for insertion is already part of another linked list.

        :param node_to_insert: Node to be inserted
        :param node_referenced: Node marking location where the other node moves after
        :return: None
        """
        pass

    @multimethod
    @deprecated(version='1.0.0', reason='inserting relative to node position not supported for unrolled linked list structure')
    def insert_after(self, val: Any, node_referenced: UnrolledNode , **kwargs) -> None:
        """
        Insert new node with given value right after some existing node in linked list.

        :param val: Value to insert
        :param node_referenced: Node marking location where the other node moves after
        :return: None
        """
        pass

    def swap(self, node1: UnrolledNode, node2: UnrolledNode) -> None:
        """
        Swap values for two existing nodes in linked list. If one or both nodes do not exist in the linked list,
        the linked list is not modified.

        :param node1: First node
        :param node2: Second node
        :return: None
        """
        temp = node2.val
        node2.val = node1.val
        node1.val = temp

