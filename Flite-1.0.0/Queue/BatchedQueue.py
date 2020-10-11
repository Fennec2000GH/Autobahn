
from multimethod import multimethod
import numpy as np
from typing import Iterable, Sized, Union


class BatchedQueue:
    """
        Implementation of queue that pops top k elements as a batch (iterable). By top k, the ordering goes by the order
        of insertion into the queue rather than comparing individual elements.
    """

    # METHODS
    def __init__(self, batch_size: int = 1, maxsize: int = 0) -> None:
        """
        Initializes BatchedQueue attributes

        Parameters:
        :param batch_size: The rank or batch size
        :param maxsize: Maximum size allowed for queue data structure
        :return: None
        """
        # Checking for valid arguments
        if type(batch_size) != int:
            raise TypeError('k must be of type int.')
        if batch_size <= 0:
            raise ValueError('k must be nonnegative.')

        # Setting attributes
        self.__start_index = 0  # Index in self.__queue marking the front
        self.__batch_size = batch_size
        self.__queue = np.array([])

    def __del__(self) -> None:
        """Cleaning up when deleting queue"""
        del self.__queue
        del self

    def __len__(self) -> int:
        """
        Gets the length of the queue.

        :return: The size of the queue.
        """
        return self.__queue.size - self.__start_index

    # PROPERTIES
    @property
    def batch_size(self) -> int:
        """
        Gets the size of batch
        :return: Current size of batch
        """
        return self.__batch_size

    @batch_size.setter
    def batch_size(self, new_batch_size: int) -> None:
        """
        Sets new size of batch.

        :exception TypeError: new_batch_size must be of type int
        :exception ValueError: new_batch_size must be nonnegative
        :param new_batch_size: New size for batch
        :return: None
        """
        # Checking for valid arguments
        if type(new_batch_size) != int:
            raise TypeError('new_batch_size must be of type int.')
        if new_batch_size <= 0:
            raise ValueError('new_batch_size must be nonnegative.')

        self.__batch_size = new_batch_size

    # ACCESSORS
    def clear(self) -> None:
        """
        Removes all elements currently in queue without deleting self.

        :return: None
        """
        self.__start_index = len(self)

    def is_empty(self) -> bool:
        """
        Checks whether the queue is empty or not.

        :return: True if there is at least one available element in queue, otherwise False.
        """
        if self.__start_index == len(self):
            return True
        return False

    def size(self) -> int:
        """
        Gets the number of available elements in queue. The same as len(self)

        :return: The size of queue.
        """
        return len(self)

    # MUTATORS
    def pop(self, enforce: bool = False) -> Iterable:
        """
        Gets top k elements from queue. If there is less than k available, queue becomes emptied. If enforce is True and
        less than k elements are available, a ValueError will be thrown.

        :param enforce: Whether or not to strictly enforce popping k elements together. Default value is False.
        :return: An iterable containing the top k elements in queue.
        """
        if enforce and len(self) < self.__batch_size:
            raise ValueError('There are not enough elements left in queue to meet batch size.')
        self.__start_index += self.__batch_size
        return self.__queue[self.__start_index - self.__batch_size:self.__start_index]

    @multimethod
    def push(self, element) -> None:
        """
        Pushes new element to queue. If maxsize is nonzero and size of queue already reached maxsize, a ValueError is
        thrown. Element can be of any type.

        :param element: Object to insert into queue.
        :exception ValueError: maxsize is nonzero and capacity of queue is reached.
        :return: None
        """
        # Checking for valid state
        if 0 < self.__batch_size == len(self):
            raise ValueError('maxsize is nonzero and capacity of queue is reached.')

        self.__queue = np.append(arr=self.__queue, values=element, axis=None)

    @multimethod
    def push(self, elements: Union[Iterable, Sized]) -> None:
        """
        Pushes all elements from an iterable into queue. If the remaining capacity of queue is not enough to accomodate
        the size of the element iterable, a ValueError is raised.

        :exception ValueError: Remaining capacity of queue cannot accommodate all elements given.
        :param elements: Iterable of elements to insert into queue
        :return: None
        """
        # Checking for valid state
        if self.__batch_size > 0 and len(self) - self.__batch_size > len(elements):
            raise ValueError('Remaining capacity of queue cannot accommodate all elements given.')

        for el in elements:
            if isinstance(el, (Iterable, Sized)):
                self.__queue = np.append(arr=self.__queue, values=el, axis=None)
                continue
            self.push(el)
