
from __future__ import annotations
import copy
from multimethod import multimethod
import param
from typing import Any, Collection, List, Optional

from LinkedList.LinkedListABC import AbstractLinkedList, AbstractNode


class XORNode(AbstractNode):
    """Node implementation for linked list"""

    # METHODS
    def __init__(self, val: Any) -> None:
        """
        Singly linked node initializer

        :param val: Value for node
        :return : None
        """
        # Check for valid arguments
        super(XORNode, self).__init__()
        self.__val = copy.deepcopy(x=val)
        self.__npx = param.Integer(default=0, allow_None=False, doc='XOR between ids of both adjacent neighbors')

    def __repr__(self) -> str:
        """
        Representation of XOR node

        :return: Official str representation of XOR node
        """
        return f'XORNode(val={str(self.__val)})'

    def __str__(self) -> str:
        """
        Representation of node as printed str

        :return: str when applying print to node
        """
        return f'{self.__val}'

    def __eq__(self, other: XORNode) -> bool:
        """
        Check for node value equality

        :param other: Another XOR node to compare for equality
        :return: True if other has an equal val attribute value as self
        """
        # Check for valid arguments
        if not isinstance(other, XORNode):
            raise TypeError('other must be of type XORNode')
        return self.__val == other.__val and self.__npx == other.__npx

    # PROPERTIES
    @property
    def val(self) -> Any:
        """
        Gets value in node

        :return: Value stored in node
        """
        return self.__val

    @val.setter
    def val(self, new_val: Any) -> None:
        """
        Sets value in node

        :param new_val: New value to replace current value in node
        :return: None
        """
        # Checking for valid arguments
        if new_val is None:
            raise ValueError('new_val cannot be None')
        self.__val = new_val

    @property
    def npx(self) -> int:
        """
        Get the XOR value stored inside XORNode

        :return: Positive integer if XORNode is bordered by at least one other XORNode, or 0
        """
        return self.__npx

    @property
    def linkedlist(self) -> Optional[LinkedList]:
        """
        Gets any linked list that owns the node

        :return: True if node is not part of any linked list, otherwise False
        """
        return self._linkedlist


class LinkedList(AbstractLinkedList):
    """Simple implementation of a single linked list"""

    def __init__(self, iterable: Collection[Any] = None, capacity: int = None) -> None:
        """Singly linked list initializer"""
        super(LinkedList, self).__init__()

        # Checking for valid arguments
        if iterable is not None and not isinstance(iterable, Collection):
            raise TypeError('iterable must be of type Iterable')
        if capacity is not None and type(capacity) != int:
            raise TypeError('capacity must be of type int')
        if capacity is not None and len(iterable) > capacity:
            raise ValueError('iterable must have a size equal to or less than capacity')

        # Assigning attributes
        self._capacity = capacity
        self._size = len(iterable)

        # Creating linked list
        self.__nodes = param.Dict(default=dict(), allow_None=False, doc='Keeps references of XORNodes by id')
        self.__head = self.__tail = None
        if iterable is not None and len(iterable) > 0:

            # Adding head
            if isinstance(iterable[0], XORNode) and iterable[0].linkedlist is not None:
                raise ValueError('Head is already part of another linked list')
            self.__head = self.__tail = iterable[0] if isinstance(iterable[0], XORNode) else XORNode(val=iterable[0])
            self.__head._linkedlist = self
            self.__nodes.update({id(self.__head) : self.__head})

            # References to adjacent pair of XORNodes for traversal
            left = None
            right = self.__head

            # Adding nodes between head and tail
            for item in iterable[1:len(iterable) - 1]:
                if isinstance(item, XORNode):
                    if item.linkedlist is not None:
                        raise TypeError('Item is already part of another linked list')
                    item_to_add = item
                else:
                    item_to_add = XORNode(val=item)
                item_to_add._linkedlist = self
                right._XORNode__npx = (0 if left is None else id(left)) ^ id(item_to_add)
                left = right
                right = item_to_add
                self.__nodes.update({id(item_to_add) : item_to_add})

            # Adding tail
            last_item = iterable[len(iterable) - 1]
            if isinstance(last_item, XORNode):
                if last_item.linkedlist is not None:
                    raise TypeError('Item is already part of another linked list')
                self.__tail = last_item
            else:
                self.__tail = XORNode(val=last_item)
            right._XORNode__npx = (0 if left is None else id(left)) ^ id(self.__tail)
            self.__tail._XORNode__npx = id(right)  # npx of tail is id of node right before tail
            self.__nodes.update({id(self.__tail) : self.__tail})

    def __eq__(self, other: LinkedList) -> bool:
        """
        Check for equality between two singly linked lists

        :return: True if each node in both linked lists match in value, otherwise False
        """
        # Edge cases
        if other is None or len(self) != len(other):
            return False
        for node_self in list(self.__nodes.values()):
            for node_other in other.__nodes:
                if node_self != node_other:
                    return False
        return True

    def __repr__(self) -> str:
        """
        Representation of XOR doubly linked list

        :return: Official str representation of XOR doubly linked list
        """
        return f'LinkedList(iterable={self.tolist()}, capacity={self._capacity})'

    def __str__(self) -> str:
        """
        Representation of linked list as printed str

        :return: str when applying print to linked list
        """
        return f'linked list of size {self._size}'

    # PROPERTIES
    @property
    def head(self) -> Optional[XORNode]:
        """
        Head of linked list

        :return: First node of linked list, if not empty, otherwise None
        """
        return self.__head

    @property
    def tail(self) -> Optional[XORNode]:
        """
        Tail of linked list

        :return: Last node of linked list, if not empty, otherwise None
        """
        return self.__tail

    @property
    def allow_loop(self) -> bool:
        """
        Checks whether the tail is allowed to form a loop with a previous node

        :return: True if loop is allowed, otherwise False
        """
        return self.__allow_loop

    # ACCESSORS
    @multimethod
    def contains(self, node: XORNode) -> bool:
        """
        Checks whether given node is a contained reference in linked list

        :param node: Node to check for existence
        :return: True if node exists in linked list, otherwise False
        """
        # Checking for valid arguments
        if not isinstance(node, XORNode):
            raise TypeError('node must be of type SinglyLinkedNode')

        # Edge case
        if self.is_empty():
            return False

        # Searching for node in linked list
        return node in self.__nodes

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
        return any([node.val == val for node in self.__nodes])

    @multimethod
    def contains(self, nodes: Collection[XORNode]) -> bool:
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
        # Edge case
        if len(vals) > len(self.__nodes):
            return False
        vals_other = set([val for val in vals])
        vals_self = set([node.val for node in self.__nodes])
        return vals_other.intersection(vals_self) == vals_other

    def is_empty(self) -> bool:
        """
        Check if there are currently no nodes in linked list

        :return: True if no nodes exist yet in linked list, otherwise False
        """
        return self.__head is None or len(self.__nodes) == 0

    # MUTATORS
    @multimethod
    def push_back(self, node: XORNode) -> None:
        """
        Appends given node to end of linked list. Linked list is not modified if node already belongs
        to this linked list or another linked list.

        :param node: Node to append
        :return: None
        """
        # Checking for valid arguments
        if not isinstance(node, XORNode):
            raise TypeError('node must be of type XORNode')
        if node.linkedlist is not None:
            raise ValueError('node must not yet exist any linked list')

        # Pushing back node
        if self.is_empty():
            self.__head = self.__tail = node
        else:
            self.__tail._XORNode__npx = self.__tail._XORNode__npx ^ id(node)
            node._XORNode__npx = id(self.__tail)
            self.__tail = node
        node._linkedlist = self
        self._size += 1

    @multimethod
    def push_back(self, val: Any) -> None:
        """
        Appends new node with given value to end of linked list.

        :param val: Value to append
        :return: None
        """
        # Check for valid arguments
        if isinstance(val, AbstractNode):
            raise TypeError('val can be of any type except AbstractNode or any derived classes')
        node = XORNode(val=val)
        self.push_back(node=node)

    @multimethod
    def push_front(self, node: XORNode) -> None:
        """
        Prepends given node to front of linked list. Linked list is not modified if node already belongs
        to this linked list or another linked list.

        :param node: Node to prepend
        :return: None
        """
        # Checking for valid arguments
        if not isinstance(node, XORNode):
            raise TypeError('node must be of type XORNode')
        if node.linkedlist is not None:
            raise ValueError('node is already part of some linked list')

        # Pushing node to front
        if self.is_empty():
            self.__head = self.__tail = node
        else:
            self.__head._XORNode__npx = id(node) ^ self.__head._XORNode__npx
            node._XORNode__npx = id(self.__head)
            self.__head = node
        node._linkedlist = self
        self._size += 1

    @multimethod
    def push_front(self, val: Any) -> None:
        """
        Prepends new node with given value to front of linked list

        :param val: Value to prepend
        :return: None
        """
        # Checking for valid arguments
        if isinstance(val, AbstractNode):
            raise TypeError('val can be of any type except Node or any derived classes')
        node = XORNode(val=val)
        self.push_front(node=node)

    def swap(self, node1: XORNode, node2: XORNode) -> None:
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

    def tolist(self) -> List[Any]:
        """
        Converts values in linked lsit in sequential order to list.

        :return: List of all values in sequential order.
        """
        # Edge cases
        if self.is_empty():
            return list()
        l = list([copy.deepcopy(x=self.__head.val)])
        if self._size == 1:
            return l

        # Normal cases
        left = self.__head
        right = self.__nodes[self.__head.npx]

        while right is not self.__tail:
            l.append(copy.deepcopy(x=right.val))
            new_right = self.__nodes.get(key=left.npx ^ right.npx, default=None)
            if new_right is None:
                raise ValueError('Error encountered in tolist function')
            left = right
            right = new_right

        l.append(copy.deepcopy(x=self.__tail.val))
        return l
