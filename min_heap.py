# Name: Mark Bastion-Cavnar
# OSU Email: bastionm@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 8
# Due Date:5/28/2024
# Description: min heap implementation


from dynamic_array import *


class MinHeapException(Exception):
    """
    Custom exception to be used by MinHeap class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class MinHeap:
    def __init__(self, start_heap=None):
        """
        Initialize a new MinHeap
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._heap = DynamicArray()

        # populate MinHeap with initial values (if provided)
        # before using this feature, implement add() method
        if start_heap:
            for node in start_heap:
                self.add(node)

    def __str__(self) -> str:
        """
        Return MinHeap content in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        heap_data = [self._heap[i] for i in range(self._heap.length())]
        return "HEAP " + str(heap_data)

    def add(self, node: object) -> None:
        """
        Add a new element to the heap.
        """
        # Append the node to the end of the heap array.
        self._heap.append(node)

        # Initialize currentIndex as the index of the newly added node (last index of the array).
        currentIndex = self._heap.length() - 1

        # While currentIndex is not the root index:
        while currentIndex > 0:
            # Calculate parentIndex as (currentIndex - 1) // 2.
            parentIndex = (currentIndex - 1) // 2

            # If the value at parentIndex is less than or equal to the value at currentIndex:
            if self._heap.get_at_index(parentIndex) <= self._heap.get_at_index(currentIndex):
                # Break the loop (heap property is maintained).
                break

            # Swap the values at currentIndex and parentIndex.
            parent_value = self._heap.get_at_index(parentIndex)
            current_value = self._heap.get_at_index(currentIndex)
            self._heap.set_at_index(currentIndex, parent_value)
            self._heap.set_at_index(parentIndex, current_value)

            # Update currentIndex to parentIndex (move up in the heap).
            currentIndex = parentIndex

    def is_empty(self) -> bool:
        """
        Check if the heap is empty.
        """
        return self._heap.length() == 0

    def get_min(self) -> object:
        """
        Get the minimum element in the heap.
        Raises MinHeapException if the heap is empty.
        """
        if self.is_empty():
            raise MinHeapException("Heap is empty")
        return self._heap.get_at_index(0)

    def remove_min(self) -> object:
        """
        Remove and return the minimum element in the heap.
        Raises MinHeapException if the heap is empty.
        """
        if self.is_empty():
            raise MinHeapException("Heap is empty")
        min_value = self._heap.get_at_index(0)
        last_index = self._heap.length() - 1
        if last_index > 0:
            last_value = self._heap.get_at_index(last_index)
            self._heap.set_at_index(0, last_value)
        self._heap.remove_at_index(last_index)
        if self._heap.length() > 0:
            self._percolate_down(0)
        return min_value

    def _percolate_down(self, index: int) -> None:
        """
        Helper function to percolate an element down the heap to maintain the heap property.
        """
        child_index = 2 * index + 1
        value = self._heap.get_at_index(index)
        while child_index < self._heap.length():
            min_value = value
            min_index = -1
            for i in range(2):
                if child_index + i < self._heap.length():
                    if self._heap.get_at_index(child_index + i) < min_value:
                        min_value = self._heap.get_at_index(child_index + i)
                        min_index = child_index + i
            if min_value == value:
                return
            else:
                self._heap.set_at_index(index, min_value)
                self._heap.set_at_index(min_index, value)
                index = min_index
                child_index = 2 * index + 1

    def build_heap(self, da: DynamicArray) -> None:
        """
        This method receives a DynamicArray with objects in any order, and builds a proper
        MinHeap from them. The current content of the MinHeap is overwritten.
        The runtime complexity of this implementation must be amortized O(N). If the runtime
        complexity is amortized O(N log N), you will not receive any points for this portion of the
        assignment, even if your method passes Gradescope.
        """
        # Step 1: Copy the elements from da into the heap’s internal array to ensure they are not referencing the same object.
        self._heap = DynamicArray()
        for i in range(da.length()):
            self._heap.append(da.get_at_index(i))

        # Step 2: Find the index of the last parent node.
        lastParentIndex = (self._heap.length() // 2) - 1

        # Step 3: For each node starting from lastParentIndex down to 0 (inclusive):
        for index in range(lastParentIndex, -1, -1):
            self._percolate_down(index)

    def size(self) -> int:
        """
        This method returns the number of items currently stored in the heap.
        The runtime complexity of this implementation must be O(1).
        """
        # Return the length of the heap's internal array.
        return self._heap.length()

    def clear(self) -> None:
        """
        This method removes all items from the heap.
        """
        self._heap = DynamicArray()


def heapsort(arr: DynamicArray) -> None:
    """
    Sort the elements of the DynamicArray in non-ascending order using the Heapsort algorithm.
    """

    def percolate_down(arr: DynamicArray, parent: int, size: int) -> None:
        """
        Helper function to percolate an element down the heap to maintain the heap property.
        """
        child_index = 2 * parent + 1
        value = arr.get_at_index(parent)

        while child_index < size:
            max_value = value
            max_index = -1
            for i in range(2):  # Check both the left and right child
                if child_index + i < size:
                    if arr.get_at_index(child_index + i) > max_value:
                        max_value = arr.get_at_index(child_index + i)
                        max_index = child_index + i
            if max_value == value:
                return
            else:
                arr.set_at_index(parent, max_value)
                arr.set_at_index(max_index, value)
                parent = max_index
                child_index = 2 * parent + 1

    # Step 1: Convert arr into a max heap
    last_parent_index = (arr.length() // 2) - 1
    for index in range(last_parent_index, -1, -1):
        percolate_down(arr, index, arr.length())

    # Step 2: For each element in arr starting from the last element down to the second element
    for end_index in range(arr.length() - 1, 0, -1):
        # Swap the first element with the current element
        first_value = arr.get_at_index(0)
        end_value = arr.get_at_index(end_index)
        arr.set_at_index(0, end_value)
        arr.set_at_index(end_index, first_value)

        # Reduce the size of the heap by one
        size = end_index

        # Apply percolate_down from the root to the new size of the heap
        percolate_down(arr, 0, size)

    # Step 3: The array is now sorted in non-ascending order


# It's highly recommended that you implement the following optional          #
# helper function for percolating elements down the MinHeap. You can call    #
# this from inside the MinHeap class. You may edit the function definition.  #

def _percolate_down(da: DynamicArray, parent: int) -> None:
    """
    TODO: Write your implementation
    """
    pass


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == '__main__':

    print("\nPDF - add example 1")
    print("-------------------")
    h = MinHeap()
    print(h, h.is_empty())
    for value in range(300, 200, -15):
        h.add(value)
        print(h)

    print("\nPDF - add example 2")
    print("-------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    for value in ['monkey', 'zebra', 'elephant', 'horse', 'bear']:
        h.add(value)
        print(h)

    print("\nPDF - is_empty example 1")
    print("-------------------")
    h = MinHeap([2, 4, 12, 56, 8, 34, 67])
    print(h.is_empty())

    print("\nPDF - is_empty example 2")
    print("-------------------")
    h = MinHeap()
    print(h.is_empty())

    print("\nPDF - get_min example 1")
    print("-----------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    print(h.get_min(), h.get_min())

    print("\nPDF - remove_min example 1")
    print("--------------------------")
    h = MinHeap([1, 10, 2, 9, 3, 8, 4, 7, 5, 6])
    while not h.is_empty() and h.is_empty() is not None:
        print(h, end=' ')
        print(h.remove_min())

    print("\nPDF - build_heap example 1")
    print("--------------------------")
    da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    h = MinHeap(['zebra', 'apple'])
    print(h)
    h.build_heap(da)
    print(h)

    print("--------------------------")
    print("Inserting 500 into input DA:")
    da[0] = 500
    print(da)

    print("Your MinHeap:")
    print(h)
    if h.get_min() == 500:
        print("Error: input array and heap's underlying DA reference same object in memory")

    print("\nPDF - size example 1")
    print("--------------------")
    h = MinHeap([100, 20, 6, 200, 90, 150, 300])
    print(h.size())

    print("\nPDF - size example 2")
    print("--------------------")
    h = MinHeap([])
    print(h.size())

    print("\nPDF - clear example 1")
    print("---------------------")
    h = MinHeap(['monkey', 'zebra', 'elephant', 'horse', 'bear'])
    print(h)
    print(h.clear())
    print(h)

    print("\nPDF - heapsort example 1")
    print("------------------------")
    da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    print(f"Before: {da}")
    heapsort(da)
    print(f"After:  {da}")

    print("\nPDF - heapsort example 2")
    print("------------------------")
    da = DynamicArray(['monkey', 'zebra', 'elephant', 'horse', 'bear'])
    print(f"Before: {da}")
    heapsort(da)
    print(f"After:  {da}")
