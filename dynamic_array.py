# Name: Mark Bastion-Cavnar
# OSU Email: bastionm@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment 2: Dynamic Array and ADT Implementation
# Due Date: 4/29/2024
# Description:This is a DynamicArray that includes a variety of methods that can be leveraged ensure that changes (resize, insert, remove, append) can be done in a dynamic way.


from static_array import StaticArray


class DynamicArrayException(Exception):
    """
    Custom exception class to be used by Dynamic Array
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class DynamicArray:
    def __init__(self, start_array=None):
        """
        Initialize new dynamic array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._size = 0
        self._capacity = 4
        self._data = StaticArray(self._capacity)

        # populate dynamic array with initial values (if provided)
        # before using this feature, implement append() method
        if start_array is not None:
            for value in start_array:
                self.append(value)

    def __str__(self) -> str:
        """
        Return content of dynamic array in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = "DYN_ARR Size/Cap: "
        out += str(self._size) + "/" + str(self._capacity) + ' ['
        out += ', '.join([str(self._data[_]) for _ in range(self._size)])
        return out + ']'

    def __iter__(self):
        """
        Create iterator for loop
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Obtain next value and advance iterator
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        try:
            value = self[self._index]
        except DynamicArrayException:
            raise StopIteration

        self._index += 1
        return value

    def get_at_index(self, index: int) -> object:
        """
        Return value from given index position
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        return self._data[index]

    def set_at_index(self, index: int, value: object) -> None:
        """
        Store value at given index in the array
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        self._data[index] = value

    def __getitem__(self, index) -> object:
        """
        Same functionality as get_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.get_at_index(index)

    def __setitem__(self, index, value) -> None:
        """
        Same functionality as set_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.set_at_index(index, value)

    def is_empty(self) -> bool:
        """
        Return True is array is empty / False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size == 0

    def length(self) -> int:
        """
        Return number of elements stored in array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return the capacity of the array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    def print_da_variables(self) -> None:
        """
        Print information contained in the dynamic array.
        Used for testing purposes.
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        print(f"Length: {self._size}, Capacity: {self._capacity}, {self._data}")

    # -----------------------------------------------------------------------

    def resize(self, new_capacity: int) -> None:
        """
        Change the capacity of the internal static array.
        If new_capacity is less than size, method should not do anything.
        If new_capacity is not a positive integer, method should not do anything.
        """
        if new_capacity < self._size or new_capacity < 1:
            return  # Do nothing if new_capacity is invalid

        # Create a new StaticArray with the new capacity
        new_data = StaticArray(new_capacity)

        # Copy existing elements to the new StaticArray
        for i in range(self._size):
            new_data[i] = self._data[i]

        # Update the internal StaticArray and the capacity
        self._data = new_data
        self._capacity = new_capacity

    def append(self, value: object) -> None:
        """
        Add a new value at the end of the dynamic array. If the internal storage
        is full, the array's capacity is doubled.
        """
        if self._size == self._capacity:
            self.resize(self._capacity * 2)

        self._data[self._size] = value
        self._size += 1

    def insert_at_index(self, index, value):
        if index < 0 or index > self._size:
            raise DynamicArrayException("Index out of bounds")

        if self._size == self._capacity:
            self.resize(self._capacity * 2)  # Ensure resize method has the right parameter

        for i in range(self._size, index, -1):
            self._data[i] = self._data[i - 1]

        self._data[index] = value
        self._size += 1

    def remove_at_index(self, index: int) -> None:
    if index < 0 or index >= self._size:
        raise DynamicArrayException("Index out of valid range")

    # Move elements to fill the gap
    for i in range(index, self._size - 1):
        self._data[i] = self._data[i + 1]

    # Decrement size after removal
    self._size -= 1
    self._data[self._size] = None  # Clean up the dangling reference at the end

    # More aggressive resizing
    if self._size < self._capacity // 2 and self._capacity > 4:
        # New capacity should not be less than double the current size unless it is less than the minimum capacity
        new_capacity = max(4, 2 * self._size)
        self.resize(new_capacity)

    def slice(self, start_index: int, size: int) -> 'DynamicArray':
        if start_index < 0 or start_index >= self._size or size < 0 or start_index + size > self._size:
            raise DynamicArrayException("Invalid start index or size")

        new_array = DynamicArray()  # Create a new DynamicArray to store the slice
        for i in range(size):
            new_array.append(self.get_at_index(start_index + i))
        return new_array

    def map(self, map_func) -> "DynamicArray":
        """
        Applies a function to each element of the dynamic array and
        returns a new dynamic array with the modified elements.
        """
        # Create a new dynamic array to store the mapped values
        mapped_array = DynamicArray()

        # Apply the map function to each element of the current array
        for i in range(self._size):
            mapped_value = map_func(self._data[i])
            mapped_array.append(mapped_value)

        # The new dynamic array is the object returned
        return mapped_array

    def filter(self, filter_func) -> 'DynamicArray':
        """
        Create a new dynamic array populated only with those elements
        from the original array for which filter_func returns True.
        """
        result_array = DynamicArray()  # Create a new DynamicArray to store the filtered results
        for item in self:  # Iterate over current array items
            if filter_func(item):  # Apply the filter function, check if the item should be included
                result_array.append(item)  # If so, append it to the result_array
        return result_array

    def reduce(self, reduce_func, initializer=None) -> 'DynamicArray':
        """
        Sequentially apply reduce_func to all elements of the dynamic array and
        return the resulting value. If an initializer is provided, use it as the initial
        accumulator, otherwise, use the first value in the array. If the array is empty,
        return the initializer or None if not provided.
        """
        # Check if the array is empty
        if self._size == 0:
            return initializer

        # Set the initial accumulator
        accumulator = initializer if initializer is not None else self._data[0]

        # Start iterating from the second element if initializer is not provided
        start_index = 1 if initializer is None else 0
        for i in range(start_index, self._size):
            accumulator = reduce_func(accumulator, self._data[i])

        return accumulator


def chunk(arr: DynamicArray) -> DynamicArray:
    """
    Split a DynamicArray into multiple DynamicArrays, each containing a non-descending subsequence of values.
    The function operates in O(N) complexity, where N is the number of elements in the input array.
    Each chunk is then stored as an element in a new DynamicArray.

    :param arr: a DynamicArray of comparable items (numbers or strings)
    :return: a DynamicArray of DynamicArrays, each containing a non-descending subsequence from the original array
    """

    if arr.length() <= 1:
        return DynamicArray([arr])

    # Create a new DynamicArray to hold the chunks
    chunked = DynamicArray()
    current_chunk = DynamicArray()

    # Add the first value to the current chunk
    current_chunk.append(arr.get_at_index(0))

    # Iterate through the original array
    for i in range(1, arr.length()):
        # If the current element is not less than the previous, append it to the current chunk
        if arr.get_at_index(i) >= arr.get_at_index(i - 1):
            current_chunk.append(arr.get_at_index(i))
        else:
            # Otherwise, append the current chunk to the chunked array and start a new chunk
            chunked.append(current_chunk)
            current_chunk = DynamicArray()
            current_chunk.append(arr.get_at_index(i))


    if current_chunk.length() > 0:
        chunked.append(current_chunk)

    return chunked


def find_mode(arr: DynamicArray) -> tuple[DynamicArray, int]:
    if arr.is_empty():
        return DynamicArray(), 0

    mode_array = DynamicArray()
    mode_value = arr.get_at_index(0)
    mode_frequency = 1
    current_frequency = 1

    # Iterate through the array to find the mode value
    for index in range(1, arr.length()):
        if arr.get_at_index(index) == arr.get_at_index(index - 1):
            current_frequency += 1
        else:
            current_frequency = 1

        # If the current frequency is greater than the mode frequency,
        # update the mode and its frequency
        if current_frequency > mode_frequency:
            mode_value = arr.get_at_index(index - 1)
            mode_frequency = current_frequency
            mode_array = DynamicArray([mode_value])
        elif current_frequency == mode_frequency:
            # If the current value has the same frequency as the mode,
            # it is also a mode, so add it to the mode array
            if arr.get_at_index(index - 1) != mode_value:
                mode_value = arr.get_at_index(index - 1)
                mode_array.append(mode_value)

    # Check the last element
    if current_frequency == mode_frequency:
        if arr.get_at_index(arr.length() - 1) != mode_value:
            mode_array.append(arr.get_at_index(arr.length() - 1))

    return mode_array, mode_frequency


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print("\n# resize - example 1")
    da = DynamicArray()

    # print dynamic array's size, capacity and the contents
    # of the underlying static array (data)
    da.print_da_variables()
    da.resize(8)
    da.print_da_variables()
    da.resize(2)
    da.print_da_variables()
    da.resize(0)
    da.print_da_variables()

    print("\n# resize - example 2")
    da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8])
    print(da)
    da.resize(20)
    print(da)
    da.resize(4)
    print(da)

    print("\n# append - example 1")
    da = DynamicArray()
    da.print_da_variables()
    da.append(1)
    da.print_da_variables()
    print(da)

    print("\n# append - example 2")
    da = DynamicArray()
    for i in range(9):
        da.append(i + 101)
        print(da)

    print("\n# append - example 3")
    da = DynamicArray()
    for i in range(600):
        da.append(i)
    print(da.length())
    print(da.get_capacity())

    print("\n# insert_at_index - example 1")
    da = DynamicArray([100])
    print(da)
    da.insert_at_index(0, 200)
    da.insert_at_index(0, 300)
    da.insert_at_index(0, 400)
    print(da)
    da.insert_at_index(3, 500)
    print(da)
    da.insert_at_index(1, 600)
    print(da)

    print("\n# insert_at_index example 2")
    da = DynamicArray()
    try:
        da.insert_at_index(-1, 100)
    except Exception as e:
        print("Exception raised:", type(e))
    da.insert_at_index(0, 200)
    try:
        da.insert_at_index(2, 300)
    except Exception as e:
        print("Exception raised:", type(e))
    print(da)

    print("\n# insert at index example 3")
    da = DynamicArray()
    for i in range(1, 10):
        index, value = i - 4, i * 10
        try:
            da.insert_at_index(index, value)
        except Exception as e:
            print("Cannot insert value", value, "at index", index)
    print(da)

    print("\n# remove_at_index - example 1")
    da = DynamicArray([10, 20, 30, 40, 50, 60, 70, 80])
    print(da)
    da.remove_at_index(0)
    print(da)
    da.remove_at_index(6)
    print(da)
    da.remove_at_index(2)
    print(da)

    print("\n# remove_at_index - example 2")
    da = DynamicArray([1024])
    print(da)
    for i in range(17):
        da.insert_at_index(i, i)
    print(da.length(), da.get_capacity())
    for i in range(16, -1, -1):
        da.remove_at_index(0)
    print(da)

    print("\n# remove_at_index - example 3")
    da = DynamicArray()
    print(da.length(), da.get_capacity())
    [da.append(1) for i in range(100)]  # step 1 - add 100 elements
    print(da.length(), da.get_capacity())
    [da.remove_at_index(0) for i in range(68)]  # step 2 - remove 68 elements
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 3 - remove 1 element
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 4 - remove 1 element
    print(da.length(), da.get_capacity())
    [da.remove_at_index(0) for i in range(14)]  # step 5 - remove 14 elements
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 6 - remove 1 element
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 7 - remove 1 element
    print(da.length(), da.get_capacity())

    for i in range(14):
        print("Before remove_at_index(): ", da.length(), da.get_capacity(), end="")
        da.remove_at_index(0)
        print(" After remove_at_index(): ", da.length(), da.get_capacity())

    print("\n# remove at index - example 4")
    da = DynamicArray([1, 2, 3, 4, 5])
    print(da)
    for _ in range(5):
        da.remove_at_index(0)
        print(da)

    print("\n# slice example 1")
    da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8, 9])
    da_slice = da.slice(1, 3)
    print(da, da_slice, sep="\n")
    da_slice.remove_at_index(0)
    print(da, da_slice, sep="\n")

    print("\n# slice example 2")
    da = DynamicArray([10, 11, 12, 13, 14, 15, 16])
    print("SOURCE:", da)
    slices = [(0, 7), (-1, 7), (0, 8), (2, 3), (5, 0), (5, 3), (6, 1), (6, -1)]
    for i, cnt in slices:
        print("Slice", i, "/", cnt, end="")
        try:
            print(" --- OK: ", da.slice(i, cnt))
        except:
            print(" --- exception occurred.")

    print("\n# map example 1")
    da = DynamicArray([1, 5, 10, 15, 20, 25])
    print(da)
    print(da.map(lambda x: x ** 2))

    print("\n# map example 2")


    def double(value):
        return value * 2


    def square(value):
        return value ** 2


    def cube(value):
        return value ** 3


    def plus_one(value):
        return value + 1


    da = DynamicArray([plus_one, double, square, cube])
    for value in [1, 10, 20]:
        print(da.map(lambda x: x(value)))

    print("\n# filter example 1")


    def filter_a(e):
        return e > 10


    da = DynamicArray([1, 5, 10, 15, 20, 25])
    print(da)
    result = da.filter(filter_a)
    print(result)
    print(da.filter(lambda x: (10 <= x <= 20)))

    print("\n# filter example 2")


    def is_long_word(word, length):
        return len(word) > length


    da = DynamicArray("This is a sentence with some long words".split())
    print(da)
    for length in [3, 4, 7]:
        print(da.filter(lambda word: is_long_word(word, length)))

    print("\n# reduce example 1")
    values = [100, 5, 10, 15, 20, 25]
    da = DynamicArray(values)
    print(da)
    print(da.reduce(lambda x, y: (x // 5 + y ** 2)))
    print(da.reduce(lambda x, y: (x + y ** 2), -1))

    print("\n# reduce example 2")
    da = DynamicArray([100])
    print(da.reduce(lambda x, y: x + y ** 2))
    print(da.reduce(lambda x, y: x + y ** 2, -1))
    da.remove_at_index(0)
    print(da.reduce(lambda x, y: x + y ** 2))
    print(da.reduce(lambda x, y: x + y ** 2, -1))

    def print_chunked_da(arr: DynamicArray):
        if len(str(arr)) <= 100:
            print(arr)
        else:
            print(f"DYN_ARR Size/Cap: {arr.length()}/{arr.get_capacity()}")
            print('[\n' + ',\n'.join(f'\t{chunk}' for chunk in arr) + '\n]')

    print("\n# chunk example 1")
    test_cases = [
        [10, 20, 30, 30, 5, 10, 1, 2, 3, 4],
        ['App', 'Async', 'Cloud', 'Data', 'Deploy',
         'C', 'Java', 'Python', 'Git', 'GitHub',
         'Class', 'Method', 'Heap']
    ]

    for case in test_cases:
        da = DynamicArray(case)
        chunked_da = chunk(da)
        print(da)
        print_chunked_da(chunked_da)

    print("\n# chunk example 2")
    test_cases = [[], [261], [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]]

    for case in test_cases:
        da = DynamicArray(case)
        chunked_da = chunk(da)
        print(da)
        print_chunked_da(chunked_da)

    print("\n# find_mode - example 1")
    test_cases = (
        [1, 1, 2, 3, 3, 4],
        [1, 2, 3, 4, 5],
        ["Apple", "Banana", "Banana", "Carrot", "Carrot",
         "Date", "Date", "Date", "Eggplant", "Eggplant", "Eggplant",
         "Fig", "Fig", "Grape"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"{da}\nMode: {mode}, Frequency: {frequency}\n")

    case = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    da = DynamicArray()
    for x in range(len(case)):
        da.append(case[x])
        mode, frequency = find_mode(da)
        print(f"{da}\nMode: {mode}, Frequency: {frequency}")
