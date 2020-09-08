
import math
import numpy as np
from typing import Any, Collection


class HashedArrayTree:
    """Implementation of hashed array tree efficient list data structure"""

    # METHODS
    def __init__(self, power: int, capacity: int = None, iterable: Collection = None) -> None:
        """Initializes HAT attributes"""
        super(HashedArrayTree, self).__init__()

        # Checking for valid arguments
        if type(power) != int:
            raise TypeError('power must be of type int')
        if power <= 0:
            raise ValueError('power must be a positive integer')
        if capacity <= int(math.pow(2, power)):
            raise ValueError('capacity must be more than 2^power')
        if math.floor(math.log(x=capacity, base=2)) != math.log(x=capacity, base=2):
            raise ValueError('capacity must be a perfect power of 2')

        # Setting attributes
        self.__power = power
        self.__hat = np.full(shape=(power, power), fill_value=np.nan, dtype=Any)
        self.__capacity = capacity
        self.__size = 0
        self.__append_index = 0  # index where to append new element

        # Appending initial elements from given collection
        if iterable is not None and len(iterable) > 0:
            self.__power = int(max([self.__power, math.ceil(math.log(x=len(iterable), base=2))]))
            for element in iterable:
                self.append(element)

    def __len__(self) -> int:
        """
        Gets number of elements in HAT

        :return: Integer denoting the size of HAT
        """
        return self.__size

    def __getitem__(self, index: int) -> Any:
        """
        Gets element associated with index. For negative index, this works the same as traditional list or numpy array
        by wrapping around the other end.

        :param index: 0-based index that is an integer
        :return: Element stored at given index, or None if no element exists at the index
        """
        # Checking for valid arguments
        if index >= self.__capacity or index < -self.__capacity:
            raise IndexError('index is out of bounds; it must be in [-capacity, capacity - 1]')

        top_index = index >> self.__power
        leaf_index = index & (self.__capacity - 1)
        return self.__hat[top_index][leaf_index]

    def __setitem__(self, index: int, element: Any) -> None:
        """
        Sets new element at given index

        :param index: 0-based index that is an integer
        :param element:
        :return: Element to replace existing value at given index
        """
        # Checking for valid arguments
        if index >= self.__capacity or index < -self.__capacity:
            raise IndexError('index is out of bounds; it must be in [-capacity, capacity - 1]')

        top_index = index >> self.__power
        leaf_index = index & (self.__capacity - 1)
        if self.__getitem__(index=index) is None:
            self.__size += 1
        self.__hat[top_index][leaf_index] = element

    # PROPERTIES
    def capacity(self) -> int:
        """
        Gets the capacity of HAT.

        :return: Integer denoting the maximum number of elements allowed in HAT
        """
        return self.__capacity

    def power(self) -> int:
        """
        Gets the current power reflecting the size of the HAT

        :return: power
        """
        return self.__power

    # ACCESSORS
    def contains(self, val: Any) -> bool:
        """
        Checks whether given value is in HAT

        :param val: Value to check for existence
        :return: True if val exists in HAT, otherwise False
        """
        return np.any(a=[np.any(a=[element == val for element in leaf]) for leaf in self.__hat])

    def is_full(self) -> bool:
        """
        Checks whether current capacity is fully filled

        :return: True if size equals capacity, otherwise False
        """
        return self.__size == self.__capacity

    # MUTATORS
    def __resize(self) -> None:
        """
        Hidden function that automatically expands HAT by factor of 4 upon filling up and reorganizes existing elements

        :return: None
        """
        new_power = self.__power + 1

        # Resizing leaf arrays
        for leaf in self.__hat:
            leaf.resize(int(math.pow(2, new_power)))

        # Redistributing existing elements to compact newly resized HAT
        for top_index in np.arange(1, self.__power):
            new_top_index = top_index // 2
            if top_index % 2 == 0:
                self.__hat[new_top_index][:self.__power] = self.__hat[top_index][:self.__power]
            else:
                self.__hat[new_top_index][self.__power:] = self.__hat[top_index][self.__power:]
            self.__hat[top_index].fill(value=np.nan)

        # Adding new empty leaf arrays to make HAT square again
        for _ in np.arange(self.__power):
            self.__hat = np.append(arr=self.__hat, values=np.full(shape=(new_power), value=np.nan, dtype=Any))
        self.__power = new_power

    def append(self, val: Any) -> None:
        """
        Appends new element sequentially to HAT. If an older element at supposed insertion index already exists due to
        setting the older element by index rather than append, the new element will be attempted to insert repeatedly
        in the next cell until an empty cell is encountered.

        :param val: Element to append
        :return: None
        """
        # Checking for valid arguments
        if self.__size == int(math.pow(2, self.__power)):
            self.__resize()

        self.__hat[self.__append_index[0]][self.__append_index[1]] = val
        self.__size += 1
