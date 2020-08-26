
from __future__ import annotations
import copy
from multimethod import multimethod
from typing import Any, Collection, Optional, Sized

from LinkedList.LinkedListABC import LinkedList, Node


class SinglyLinkedNode(Node):
    """Node for singly linked list"""

    # METHODS
    def __init__(self, val: Any) -> None:
        """Node initializer"""
        # Check for valid arguments
        self.__val = val
        self.__next = None
        self.__linkedlist = None

    def __repr__(self) -> str:
        """
        Representation of node

        :return: official str representation of node
        """
        return f'Node(val={str(self.__val)}, next=self.__next)'

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
    def next(self) -> Optional[SinglyLinkedNode]:
        """
        Gets next node sequentially in linked list

        :return: Node referenced by next property, otherwise None if current node is tail
        """
        return self.__next

    @next.setter
    def next(self, new_next_node: SinglyLinkedNode) -> None:
        """
        Sets new node to be the next node

        :param new_next: New node for the next attribute
        :return: None
        """
        # Checking for valid arguments
        if new_next_node is None:
            raise ValueError('new_next cannot be None')
        if isinstance(new_next_node, SinglyLinkedNode):
            raise TypeError('new_node must be of type Node')
        self.__next = new_next_node

    @property
    def linkedlist(self) -> Optional[SinglyLinkedList]:
        """
        Gets any linked list that owns the node

        :return: True if node is not part of any linked list, otherwise False
        """
        return self.__linkedlist

    # MUTATORS
    def __set_linkedlist(self, ll: LinkedList) -> None:
        """
        Sets a new linked list as owner of the node

        :param ll: Linked list owner
        :return: None
        """
        # Checking for valid arguments
        if not isinstance(ll, SinglyLinkedList):
            raise TypeError('ll must be of type SinglyLinkedList')
        self.__linkedlist = ll


class SinglyLinkedList(LinkedList):
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
        for _ in range(self.__size):
            if curr != curr_other:
                return False
            curr = curr.__next
            curr_other = curr_other.__next
        return True

    # PROPERTIES
    @property
    def head(self) -> Optional[Node]:
        """
        Head of linked list

        :return: First node of linked list, if not empty, otherwise None
        """
        return self.__head

    @property
    def tail(self) -> Optional[Node]:
        """
        Tail of linked list

        :return: Last node of linked list, if not empty, otherwise None
        """
        return self.__tail

    @property
    def capacity(self) -> int:
        """
        Gets the capacity of the linked list

        :return: The maximum number of allowed nodes, or None if no capacity was set during initialization
        """
        return self.__capacity

    # ACCESSORS
    @multimethod
    def contains(self, node: SinglyLinkedNode) -> bool:
        """
        Checks whether given node is a contained reference in linked list

        :param node: Node to check for existence
        :return: True if node exists in linked list, otherwise False
        """
        if not isinstance(node, SinglyLinkedNode):
            raise TypeError('node must be of type SinglyLinkedNode')
        if self.is_empty():
            return False

        # Searching for node in linked list
        curr = self.__head
        while curr is not None:
            if curr is node:
                return True
            curr = curr.__next
        return False

    @multimethod
    def contains(self, val: Any) -> bool:
        """
        Checks whether given value is in some contained node reference in linked list

        :param val: Value to check for existence
        :return: True if node with val exists in linked list, otherwise False
        """
        if self.is_empty():
            return False

        # Searching for node in linked list
        curr = self.__head
        while curr is not None:
            if curr.__val == val:
                return True
            curr = curr.__next
        return False

    @multimethod
    def contains(self, nodes: Collection[SinglyLinkedNode]) -> bool:
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
    def push_back(self, node: SinglyLinkedNode) -> None:
        """
        Appends given node to end of linked list. Linked list is not modified if node already belongs
        to this linked list or another linked list.

        :param node: Node to append
        :return: None
        """
        # Checking for valid arguments
        if not isinstance(node, SinglyLinkedNode):
            raise TypeError('node must be of type Node')
        if self.is_empty():
            self.__head = self.__tail = node
        else:
            self.__tail.__next = node
            self.__tail = node
        self.__size += 1

    @multimethod
    def push_back(self, val: Any) -> None:
        """
        Appends new node with given value to end of linked list.

        :param val: Value to append
        :return: None
        """
        # Checking for valid arguments
        if self.is_empty():
            self.__head = self.__tail = SinglyLinkedNode(val=val)
        else:
            self.__tail.__next = SinglyLinkedNode(val=val)
            self.__tail = self.__tail.__next
        self.__size += 1

    @multimethod
    def push_front(self, node: SinglyLinkedNode) -> None:
        """
        Prepends given node to front of linked list. Linked list is not modified if node already belongs
        to this linked list or another linked list.

        :param node: Node to prepend
        :return: None
        """
        # Checking for valid arguments
        if not isinstance(node, SinglyLinkedNode):
            raise TypeError('node must be of type Node')
        if node.__next is not None:
            raise ValueError('node is already part of some linked list')
        if self.is_empty():
            self.__head = self.__tail = node
        else:
            node.__next = self.__head
            self.__head = node
        self.__size += 1

    @multimethod
    def push_front(self, val: Any) -> None:
        """
        Prepends new node with given value to front of linked list

        :param val: Value to prepend
        :return: None
        """
        # Checking for valid arguments
        if self.is_empty():
            self.__head = self.__tail = SinglyLinkedNode(val=val)
        else:
            node = SinglyLinkedNode(val=val)
            node.__next = self.__head
            self.__head = node
        self.__size += 1

    def move_before(self, node_to_move: SinglyLinkedNode, node_referenced: SinglyLinkedNode) -> None:
        """
        Move node existing in linked list to right before another node existing in the same linked list.
        Linked list is not modified if either node does not exist within the linked list.

        :param node_to_move: Node to be moved
        :param node_referenced: Node marking location where the other node moves before
        :return: None
        """
        # Checking for valid arguments
        if self.is_empty():
            raise ValueError('linked list is empty')
        if not isinstance(node_to_move, SinglyLinkedNode):
            raise TypeError('node_to_move must be of type SinglyLinkedNode')
        if not isinstance(node_referenced, SinglyLinkedNode):
            raise TypeError('node_referenced must be of type SinglyLinkedNode')
        if node_to_move is node_referenced:
            raise ValueError('node_to_move must be different than node_referenced')
        if node_to_move.linkedlist is not self:
            raise ValueError('node_to_move does not exist in linked list')
        if node_referenced.linkedlist is not self:
            raise ValueError('node_referenced does not exist in linked list')

        # Moving nodes
        before_node_to_move = None if node_to_move is self.__head else -1  # Node prior to node to be moved
        before_node_referenced = None if node_referenced is self.__head else -1  # Node prior to node referenced
        curr = self.__head
        while before_node_to_move == -1 or before_node_referenced == -1:
            if curr.__next is node_to_move:
                before_node_to_move = curr
            if curr.__next is node_referenced:
                before_node_referenced = curr
            if curr.__next is None:
                raise ValueError('One or both of node to be moved and node referenced does not exist in linked list')
            curr = curr.__next

        # head is node to move
        if node_to_move is self.__head:
            self.__head = self.__head.__next
            node_to_move.__next = node_referenced
            before_node_referenced.__next = node_to_move

        # head is node referenced
        elif node_referenced is self.__head:
            before_node_to_move.__next = node_to_move.__next
            node_to_move.__next = node_referenced
            self.__head = node_to_move

        else:
            before_node_to_move.__next = node_to_move.__next
            before_node_referenced.__next = node_to_move
            node_to_move.__next = node_referenced

    def move_after(self, node_to_move: SinglyLinkedNode, node_referenced: SinglyLinkedNode) -> None:
        """
        Move node existing in linked list to right after another node existing in the same linked list.
        Linked list is not modified if either node does not exist within the linked list.

        :param node_to_move: Node to be moved
        :param node_referenced: Node marking location where the other node moves after
        :return: None
        """
        # Checking for valid arguments
        if self.is_empty():
            raise ValueError('linked list is empty')
        if not isinstance(node_to_move, SinglyLinkedNode):
            raise TypeError('node_to_move must be of type SinglyLinkedNode')
        if not isinstance(node_referenced, SinglyLinkedNode):
            raise TypeError('node_referenced must be of type SinglyLinkedNode')
        if node_to_move is node_referenced:
            raise ValueError('node_to_move must be different than node_referenced')
        if node_to_move.linkedlist is not self:
            raise ValueError('node_to_move does not exist in linked list')
        if node_referenced.linkedlist is not self:
            raise ValueError('node_referenced does not exist in linked list')

        # Moving nodes
        before_node_to_move = None if node_to_move is self.__head else -1  # Node prior to node to be moved
        before_node_referenced = None if node_referenced is self.__head else -1  # Node prior to node referenced
        curr = self.__head
        while before_node_to_move == -1 or before_node_referenced == -1:
            if curr.__next is node_to_move:
                before_node_to_move = curr
            if curr.__next is node_referenced:
                before_node_referenced = curr
            if curr.__next is None:
                raise ValueError('One or both of node to be moved and node referenced does not exist in linked list')
            curr = curr.__next

        # head is node to move
        if node_to_move is self.__head:
            self.__head = self.__head.__next
            node_to_move.__next = node_referenced.__next
            node_referenced.__next = node_to_move

        # head is node referenced
        elif node_referenced is self.__head:
            before_node_to_move.__next = node_to_move.__next
            node_to_move.__next = self.__head.__next
            self.__head.__next = node_to_move

        else:
            before_node_to_move.__next = node_to_move.__next
            node_to_move.__next = node_referenced.__next
            node_referenced.__next = node_to_move

    @multimethod
    def insert_before(self, node_to_insert: SinglyLinkedNode, node_referenced: SinglyLinkedNode, **kwargs) -> None:
        """
        Insert node which does not belong to any linked list right before some existing node in linked list.
        Linked list is not modified if the node intended for insertion is already part of another linked list.

        :param node_to_insert: Node to be inserted
        :param node_referenced: Node marking location where the other node moves after
        :return: None
        """
        # Checking for valid arguments
        if self.is_empty():
            raise ValueError('linked list is empty')
        if not isinstance(node_to_insert, SinglyLinkedNode):
            raise TypeError('node_to_insert must be of type SinglyLinkedNode')
        if not isinstance(node_referenced, SinglyLinkedNode):
            raise TypeError('node_referenced must be of type SinglyLinkedNode')
        if node_to_insert is node_referenced:
            raise ValueError('node_to_insert must be different than node_referenced')
        if node_to_insert.linkedlist is not None:
            raise ValueError('node_to_insert must not yet exist any linked list')
        if node_referenced.linkedlist is not self:
            raise ValueError('node_referenced does not exist in linked list')

        # Inserting node
        # Node referencing location is head
        if node_referenced is self.__head:
            self.push_front(node=node_to_insert)
        else:
            curr = self.__head
            while True:
                if curr.__next is node_referenced:
                    before_node_referenced = curr
                    break
                if curr.__next is None:
                    raise ValueError('One or both of node to be moved and node referenced does not exist in linked list')
                curr = curr.__next

            node_to_insert.__next = node_referenced
            before_node_referenced.__next = node_to_insert

    @multimethod
    def insert_before(self, val: Any, node_referenced: SinglyLinkedNode, **kwargs) -> None:
        """
        Insert new node with given value right before some existing node in linked list.

        :param val: Value to insert
        :param node_referenced: Node marking location where the other node moves after
        :return: None
        """
        # Checking for valid arguments
        if isinstance(val, Node):
            raise TypeError('val can be of any type except Node or any derived classes')
        self.insert_before(node_to_insert=SinglyLinkedNode(val=val), node_referenced=node_referenced)

    def insert_after(self, node_to_insert: SinglyLinkedNode, node_referenced: SinglyLinkedNode, **kwargs) -> None:
        """
        Insert node which does not belong to any linked list right after some existing node in linked list.
        Linked list is not modified if the node intended for insertion is already part of another linked list.

        :param node_to_insert: Node to be inserted
        :param node_referenced: Node marking location where the other node moves after
        :return: None
        """
        # Checking for valid arguments
        if self.is_empty():
            raise ValueError('linked list is empty')
        if not isinstance(node_to_insert, SinglyLinkedNode):
            raise TypeError('node_to_insert must be of type SinglyLinkedNode')
        if not isinstance(node_referenced, SinglyLinkedNode):
            raise TypeError('node_referenced must be of type SinglyLinkedNode')
        if node_to_insert is node_referenced:
            raise ValueError('node_to_insert must be different than node_referenced')
        if node_to_insert.linkedlist is not None:
            raise ValueError('node_to_insert must not yet exist any linked list')
        if node_referenced.linkedlist is not self:
            raise ValueError('node_referenced does not exist in linked list')

        # Inserting node
        # Node referencing location is tail
        if node_referenced is self.__tail:
            self.push_back(node=node_to_insert)
        else:
            node_to_insert.__next = node_referenced.__next
            node_referenced.__next = node_to_insert

    @multimethod
    def insert_after(self, val: Any, node_referenced: SinglyLinkedNode, **kwargs) -> None:
        """
        Insert new node with given value right after some existing node in linked list.

        :param val: Value to insert
        :param node_referenced: Node marking location where the other node moves after
        :return: None
        """
        # Checking for valid arguments
        if isinstance(val, Node):
            raise TypeError('val can be of any type except Node or any derived classes')
        self.insert_after(node_to_insert=SinglyLinkedNode(val=val), node_referenced=node_referenced)

    def swap(self, node1: Node, node2: Node) -> None:
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

