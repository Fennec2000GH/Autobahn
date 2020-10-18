
import asyncio
from multimethod import multimethod
import numpy as np
from typing import Callable, Collection, Iterable, Sized, Optional, Union


class BatchedQueue:
    """
        Implementation of priority queue that pops top k elements as a batch (iterable). By top k, the ordering goes by the order
        comparing individual elements, optionally via a custom function.
    """

    # METHODS
    def __init__(self, batch_size: int = 1, func: Callable = None, maxsize: int = 0) -> None:
        """
        Initializes BatchedPriorityQueue attributes

        Parameters:
        :exception TypeError: batch_size must be of type int
        :exception ValueError: batch_size must be positive
        :param batch_size: The rank or batch size
        :param maxsize: Maximum size allowed for queue data structure
        :return: None
        """
        # Checking for valid arguments
        if type(batch_size) != int:
            raise TypeError('batch_size must be of type int.')
        if batch_size <= 0:
            raise ValueError('batch_size must be nonnegative.')

        # Setting attributes
        self.__batch_size = batch_size
        self.__pqGroup = np.repeat(a=[asyncio.PriorityQueue()], repeats=batch_size, axis=None)
        self.__size = 0

    def __del__(self) -> None:
        """Cleaning up when deleting queue"""
        del self.__pqGroup
        del self

    def __len__(self) -> int:
        """
        Gets the number of individual elements.

        :return: The size of batched priority queue elements.
        """
        return self.__size

    # PROPERTIES
    @property
    def batch_size(self) -> int:
        """
        Gets the size of batch
        :return: Current size of batch
        """
        return self.__batch_size

    async def resize(self, new_batch_size: int, keep: bool = True) -> None:
        """
        Sets new size of batch.

        :exception TypeError: new_batch_size must be of type int
        :exception ValueError: new_batch_size must be positive
        :param new_batch_size: New size for batch
        :param keep: True if new batch size is smaller than current batch size and elements past the new size are to be
        re-inserted into earlier priority queues. Otherwise, False.
        :return: None
        """
        # Checking for valid arguments
        if type(new_batch_size) != int:
            raise TypeError('new_batch_size must be of type int.')
        if new_batch_size < 0:
            raise ValueError('new_batch_size must be positive.')

        lock = asyncio.Lock()
        async with lock:
            # Priority queue list is shrunken
            if new_batch_size < self.__batch_size:
                if not keep:
                    self.__pqGroup = np.delete(arr=self.__pqGroup, obj=np.arange(new_batch_size, self.__batch_size), axis=None)
                else:
                    # Removing all elements in priority queues out of range for new batch size
                    removed_elements = list()
                    for pq in self.__pqGroup[new_batch_size:]:
                        while not pq.empty():
                            removed_elements.append(pq.get())
                    self.__pqGroup = np.delete(arr=self.__pqGroup, obj=np.arange(new_batch_size, self.__batch_size), axis=None)

                    # Re-inserting removed elements to remaining priority queues
                    await asyncio.gather(*[self.__pqGroup[0].put(element) for element in removed_elements])
                    await self.rebalance()

            # Priority queue list is expanded
            else:
                diff = new_batch_size - self.__batch_size
                self.__pqGroup = np.append(arr=self.__pqGroup, values=np.repeat(a=[asyncio.PriorityQueue()], repeats=diff, axis=None), axis=None)
                await self.rebalance()

        self.__batch_size = new_batch_size

    # ACCESSORS
    async def available_batch_size(self) -> int:
        """
        Finds the number of individual priority queues that are non-empty.

        :return: Number of priority queues with available elements for popping.
        """
        lock = asyncio.Lock()
        async with lock:
            num_available = np.count_nonzero(a=[int(pq.empty()) for pq in self.__pqGroup], axis=None)
        return num_available

    async def clear(self) -> None:
        """
        Removes all elements currently in queue without deleting self.

        :return: None
        """
        lock = asyncio.Lock()
        with lock:
            await lock.acquire()
            self.__pqGroup = np.repeat(a=[asyncio.PriorityQueue()], repeats=self.__batch_size, axis=None)
            lock.release()

    async def is_empty(self) -> bool:
        """
        Checks whether the queue is empty or not.

        :return: True if there is at least one available element in queue, otherwise False.
        """
        lock = asyncio.Lock()
        async with lock:
            await lock.acquire()

        return np.all(a=[pq.empty() for pq in self.__pqGroup], axis=None) or self.__pqGroup.size == 0

    def size(self) -> int:
        """
        Gets the number of available elements in queue. The same as len(self)

        :return: The size of queue.
        """
        return len(self)

    # MUTATORS
    async def rebalance(self) -> None:
        """
            Re-distributes existing elements as uniformly as possible across current batch size.

            :return: None
        """
        lock = asyncio.Lock()
        async with lock:
            average_pq_size = len(self) / self.__batch_size
            extra_elements = list()

            # Collecting over the top elements
            for pq in self.__pqGroup:
                while pq.qsize() > average_pq_size:
                    extra_elements.append(pq.get())

            # Re-inserting extra elements into priority heaps missing elements
            for pq in self.__pqGroup:
                while pq.qsize() < average_pq_size:
                    pq.put(extra_elements.pop())

            # Re-inserting any remaining extra elements
            for index in np.arange(self.__batch_size):
                if len(extra_elements) > 0:
                    self.__pqGroup[index].put(extra_elements.pop())
                else:
                    break

    async def pop(self, block: bool = False, timeout: Optional[int] = None) -> Iterable:
        """
        Gets top k elements from queue. If there is less than k available, queue becomes emptied. If enforce is True and
        less than k elements are available, a ValueError will be thrown.

        :param block: Default value is False.
        :return: An iterable containing the top k elements in queue.
        """
        return [await pq.get(block=block, timeout=timeout) for pq in self.__pqGroup]

    @multimethod
    async def put(self, element) -> None:
        """
        Pushes new element to smallest priority queue available. If maxsize is nonzero and size of queue already reached
        maxsize, a ValueError is thrown. Element can be of any type.

        :param element: Object to insert into queue.
        :exception ValueError: maxsize is nonzero and capacity of queue is reached.
        :return: None
        """
        pq_min = min(*[pq for pq in self.__pqGroup], key=lambda pq: await pq.qsize())
        await pq_min.put(element)

    @multimethod
    async def put(self, elements: Union[Collection, Iterable, Sized]) -> None:
        """
        Pushes all elements from an iterable into queue. If the remaining capacity of queue is not enough to accomodate
        the size of the element iterable, a ValueError is raised.

        :exception ValueError: Remaining capacity of queue cannot accommodate all elements given.
        :param elements: Iterable of elements to insert into queue
        :return: None
        """
        def func(el) -> None:
            await self.put(el)
        await asyncio.gather(*[func(el) for el in elements])
