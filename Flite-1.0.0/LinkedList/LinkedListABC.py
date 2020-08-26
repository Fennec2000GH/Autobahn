from __future__ import annotations
from abc import ABC, abstractmethod
from multimethod import multimethod
from typing import Any, Collection, Optional


class Node(ABC):
    """Abstract class for linked list node"""

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

    # ACCESSORS
    @property
    @abstractmethod
    def next(self) -> Optional[Node]:
        """
        Gets next node sequentially in linked list

        :return: Node referenced by next property, otherwise None if current node is tail
        """
        pass

    @next.setter
    @abstractmethod
    def next(self, new_next: Node) -> None:
        """
        Sets new node to be the next node

        :param new_next: New node for the next attribute
        :return: None
        """
        pass

    @property
    @abstractmethod
    def linkedlist(self) -> Optional[Any]:
        """
        Gets any linked list that owns the node

        :return: True if node is not part of any linked list, otherwise False
        """
        pass

    # MUTATORS
    @abstractmethod
    def __set_linkedlist(self, ll: LinkedList) -> None:
        """
        Sets a new linked list as owner of the node

        :param ll: Linked list owner
        :return: None
        """
        pass


class LinkedList(ABC):
    """Abstract class doe linked list"""

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
