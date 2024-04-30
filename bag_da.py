# Name: Mark Bastion-Cavnar
# OSU Email: bastionm@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment 2: Dynamic Array and ADT Implementation
# Due Date: 4/26/2024
# Description: This is a BAG ADT that uses classes from DynamicArray for the underlying storage of the bag data.


from dynamic_array import *


class Bag:
    def __init__(self, start_bag=None):
        """
        Init new bag based on Dynamic Array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._da = DynamicArray()

        if start_bag is not None:
            for value in start_bag:
                self.add(value)

    def __str__(self) -> str:
        """
        Return content of stack in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = "BAG: " + str(self._da.length()) + " elements. ["
        out += ', '.join([str(self._da.get_at_index(_))
                          for _ in range(self._da.length())])
        return out + ']'

    def size(self) -> int:
        """
        Return total number of items currently in the bag
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._da.length()

    # -----------------------------------------------------------------------

    def add(self, value: object) -> None:
        """
        Add a new element to the bag. It is implemented with O(1) amortized
        runtime complexity by utilizing the 'append' method of the DynamicArray.
        """
        self._da.append(value)

    def remove(self, value: object) -> bool:
        """
        Remove any one element from the bag that matches the provided value object.
        Return True if some object was actually removed from the bag, False otherwise.
        Implemented with O(N) runtime complexity.
        """
        for index in range(self._da.length()):
            if self._da.get_at_index(index) == value:
                self._da.remove_at_index(index)  # Use the provided method
                return True
        return False

    def count(self, value: object) -> int:
        """
        Count occurrences of value in the dynamic array.
        """
        count = 0
        for index in range(self._da.length()):
            if self._da.get_at_index(index) == value:
                count += 1
        return count

    def clear(self) -> None:
        """
        Clears the contents of the dynamic array.
        """
        self._da.resize(0)

    def equal(self, second_bag: 'Bag') -> bool:
        """
        Compares the contents of a bag with the contents of a second bag.
        Returns True if the bags are equal, otherwise False.
        """
        if self._da.length() != second_bag._da.length():
            return False

        visited = DynamicArray()
        for _ in range(second_bag._da.length()):
            visited.append(False)

        for i in range(self._da.length()):
            found = False
            for j in range(second_bag._da.length()):
                if self._da.get_at_index(i) == second_bag._da.get_at_index(j) and not visited.get_at_index(j):
                    visited.set_at_index(j, True)
                    found = True
                    break
            if not found:
                return False

        return True

    def __iter__(self):
        self._index = 0
        return self


    def __next__(self):
        if self._index < self._da.length():
            value = self._da.get_at_index(self._index)
            self._index += 1
            return value
        else:
            raise StopIteration




# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print("\n# add example 1")
    bag = Bag()
    print(bag)
    values = [10, 20, 30, 10, 20, 30]
    for value in values:
        bag.add(value)
    print(bag)

    print("\n# remove example 1")
    bag = Bag([1, 2, 3, 1, 2, 3, 1, 2, 3])
    print(bag)
    print(bag.remove(7), bag)
    print(bag.remove(3), bag)
    print(bag.remove(3), bag)
    print(bag.remove(3), bag)
    print(bag.remove(3), bag)

    print("\n# count example 1")
    bag = Bag([1, 2, 3, 1, 2, 2])
    print(bag, bag.count(1), bag.count(2), bag.count(3), bag.count(4))

    print("\n# clear example 1")
    bag = Bag([1, 2, 3, 1, 2, 3])
    print(bag)
    bag.clear()
    print(bag)

    print("\n# equal example 1")
    bag1 = Bag([10, 20, 30, 40, 50, 60])
    bag2 = Bag([60, 50, 40, 30, 20, 10])
    bag3 = Bag([10, 20, 30, 40, 50])
    bag_empty = Bag()

    print(bag1, bag2, bag3, bag_empty, sep="\n")
    print(bag1.equal(bag2), bag2.equal(bag1))
    print(bag1.equal(bag3), bag3.equal(bag1))
    print(bag2.equal(bag3), bag3.equal(bag2))
    print(bag1.equal(bag_empty), bag_empty.equal(bag1))
    print(bag_empty.equal(bag_empty))
    print(bag1, bag2, bag3, bag_empty, sep="\n")

    bag1 = Bag([100, 200, 300, 200])
    bag2 = Bag([100, 200, 30, 100])
    print(bag1.equal(bag2))

    print("\n# __iter__(), __next__() example 1")
    bag = Bag([5, 4, -8, 7, 10])
    print(bag)
    for item in bag:
        print(item)

    print("\n# __iter__(), __next__() example 2")
    bag = Bag(["orange", "apple", "pizza", "ice cream"])
    print(bag)
    for item in bag:
        print(item)
