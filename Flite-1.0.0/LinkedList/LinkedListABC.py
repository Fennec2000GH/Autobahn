from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Sized


class Node(ABC):
    """Abstract class for linked list node"""

    @abstractmethod
    def __init__(self, __iterable: Sized = None, capacity: int = None) -> None:
        pass

    @property
    @abstractmethod
    def node(self) -> Node:
        pass

    @node.setter
    @abstractmethod
    def node(self, new_node: Node) -> None:
        pass

    @property
    @abstractmethod
    def next(self) -> Node:
        pass

    @next.setter
    @abstractmethod
    def next(self, new_next: Node) -> None:
        pass
