# Name: Mark Bastion-Cavnar
# OSU Email: bastionm@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment:1
# Due Date: 4/22/2024
# Description: This python file contains the 10 functions required for assignment 1 CS261


import random
from static_array import *


# ------------------- PROBLEM 1 - MIN_MAX -----------------------------------

def min_max(arr: StaticArray) -> tuple[int, int]:
    """ Returns a tuple containing the minimum and maximum values in the array. """
    if arr.length() == 0:
        raise StaticArrayException('Array is empty')

    min_value = arr[0]  # You can also use arr.get(0) if you prefer
    max_value = arr[0]  # You can also use arr.get(0) if you prefer

    for i in range(1, arr.length()):
        value = arr[i]  # You can also use arr.get(i) if you prefer
        if value < min_value:
            min_value = value
        if value > max_value:
            max_value = value

    return (min_value, max_value)


# ------------------- PROBLEM 2 - FIZZ_BUZZ ---------------------------------
def fizz_buzz(arr: StaticArray) -> StaticArray:
    # Create a new StaticArray for the result
    result = StaticArray(arr.length())

    for i in range(arr.length()):
        value = arr[i]  # Accessing element using index directly due to __getitem__

        # Check if the value is an integer before processing
        if isinstance(value, int):
            if value % 3 == 0 and value % 5 == 0:
                result[i] = 'fizzbuzz'
            elif value % 3 == 0:
                result[i] = 'fizz'
            elif value % 5 == 0:
                result[i] = 'buzz'
            else:
                result[i] = value  # Storing the original number if no conditions are met
        else:
            result[i] = value  # Keep the original value if it's not an integer

    return result


# ------------------- PROBLEM 3 - REVERSE -----------------------------------

def reverse(arr: StaticArray) -> None:
    left_index = 0
    right_index = arr._size - 1

    while left_index < right_index:
        # Swap the elements
        left_value = arr.get(left_index)
        right_value = arr.get(right_index)
        arr.set(left_index, right_value)
        arr.set(right_index, left_value)

        # Move towards the middle
        left_index += 1
        right_index -= 1
    pass


# ------------------- PROBLEM 4 - ROTATE ------------------------------------

def rotate(arr: StaticArray, steps: int) -> StaticArray:
    # Normalize the number of steps to be within the size of the array
    steps = steps % arr.length()
    # Create a new StaticArray to hold the rotated elements
    rotated_arr = StaticArray(arr.length())

    for i in range(arr.length()):
        # Calculate the new position for each element
        new_position = (i + steps) % arr.length()
        # Use the set method to place the element at the new position
        rotated_arr[new_position] = arr[i]  # Using bracket notation for setting due to __setitem__

    return rotated_arr

    pass


# ------------------- PROBLEM 5 - SA_RANGE ----------------------------------

def sa_range(start: int, end: int) -> StaticArray:
    # Calculate the number of elements in the range
    if start <= end:
        # Generate range in increasing order
        size = end - start + 1
        data = range(start, end + 1)
    else:
        # Generate range in decreasing order
        size = start - end + 1
        data = range(start, end - 1, -1)

    # Create a new StaticArray with the calculated size
    result = StaticArray(size)

    # Set each element of the StaticArray to the corresponding value from data
    for i, value in enumerate(data):
        result[i] = value

    return result


# ------------------- PROBLEM 6 - IS_SORTED ---------------------------------

def is_sorted(arr: StaticArray) -> int:
    # Assume both ascending and descending to start with
    ascending = True
    descending = True

    # Iterate over the array to determine if it's ascending or descending
    for i in range(arr.length() - 1):
        if arr[i] < arr[i + 1]:
            descending = False  # Found a case where a later element is greater
        elif arr[i] > arr[i + 1]:
            ascending = False   # Found a case where a later element is smaller

        # Early exit if array is neither ascending nor descending
        if not ascending and not descending:
            return 0

    # Check and return the appropriate code based on the flags
    if ascending:
        return 1
    if descending:
        return -1
    return 0  # If neither, return 0

    pass


# ------------------- PROBLEM 7 - FIND_MODE -----------------------------------

def find_mode(arr: StaticArray) -> tuple[object, int]:
    # Check if the array is empty using the length() method from StaticArray
    if arr.length() == 0:
        return None

    # Initialize variables to keep track of the mode and its frequency
    current_element = arr[0]
    mode = current_element
    current_freq = 1
    max_freq = 1

    # Traverse the static array to find the mode
    for i in range(1, arr.length()):
        if arr[i] == current_element:
            current_freq += 1
        else:
            current_element = arr[i]
            current_freq = 1

        # Update mode and max frequency if the current frequency is greater
        if current_freq > max_freq:
            max_freq = current_freq
            mode = current_element

    return (mode, max_freq)

    pass


# ------------------- PROBLEM 8 - REMOVE_DUPLICATES -------------------------

def remove_duplicates(arr: StaticArray) -> StaticArray:
    # Check if the array is empty using the length() method from StaticArray
    if arr.length() == 0:
        return StaticArray(0)

    # Initialize variables to track the count of unique elements
    unique_count = 1
    for i in range(1, arr.length()):
        if arr[i] != arr[i - 1]:
            unique_count += 1

    # Create a new StaticArray to store unique elements
    result = StaticArray(unique_count)
    result[0] = arr[0]  # Set the first element
    current_index = 1

    # Populate the result array with unique elements
    for i in range(1, arr.length()):
        if arr[i] != arr[i - 1]:
            result[current_index] = arr[i]
            current_index += 1

    return result

    pass


# ------------------- PROBLEM 9 - COUNT_SORT --------------------------------

def count_sort(arr: StaticArray) -> StaticArray:
    if arr.length() == 0:
        return StaticArray(0)

    # Manually find the maximum and minimum values in the array
    max_val = arr[0]
    min_val = arr[0]
    for i in range(1, arr.length()):
        if arr[i] > max_val:
            max_val = arr[i]
        if arr[i] < min_val:
            min_val = arr[i]

    # Initialize the 'count array' (as a tuple) for the range of input array values
    range_of_values = max_val - min_val + 1
    count_array = tuple(0 for _ in range(range_of_values))

    # Populate the count array
    for i in range(arr.length()):
        index = arr[i] - min_val
        count_array = count_array[:index] + (count_array[index] + 1,) + count_array[index + 1:]

    # Create the sorted array in non-ascending order
    sorted_arr = StaticArray(arr.length())
    sorted_index = 0
    for i in range(len(count_array) - 1, -1, -1):
        while count_array[i] > 0:
            sorted_arr[sorted_index] = i + min_val
            sorted_index += 1
            count_array = count_array[:i] + (count_array[i] - 1,) + count_array[i + 1:]

    return sorted_arr
    pass


# ------------------- PROBLEM 10 - SORTED SQUARES ---------------------------
def sorted_squares(arr: StaticArray) -> StaticArray:
    if arr.length() == 0:
        return StaticArray(0)

    result = StaticArray(arr.length())
    left = 0
    right = arr.length() - 1
    result_index = right

    while left <= right:
        left_square = arr[left] ** 2
        right_square = arr[right] ** 2

        if left_square > right_square:
            result[result_index] = left_square
            left += 1
        else:
            result[result_index] = right_square
            right -= 1
        result_index -= 1

    return result
    pass


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print('\n# min_max example 1')
    arr = StaticArray(5)
    for i, value in enumerate([7, 8, 6, -5, 4]):
        arr[i] = value
    print(arr)
    result = min_max(arr)
    if result:
        print(f"Min: {result[0]: 3}, Max: {result[1]}")
    else:
        print("min_max() not yet implemented")

    print('\n# min_max example 2')
    arr = StaticArray(1)
    arr[0] = 100
    print(arr)
    result = min_max(arr)
    if result:
        print(f"Min: {result[0]}, Max: {result[1]}")
    else:
        print("min_max() not yet implemented")

    print('\n# min_max example 3')
    test_cases = (
        [3, 3, 3],
        [-10, -30, -5, 0, -10],
        [25, 50, 0, 10],
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value
        print(arr)
        result = min_max(arr)
        if result:
            print(f"Min: {result[0]: 3}, Max: {result[1]}")
        else:
            print("min_max() not yet implemented")

    print('\n# fizz_buzz example 1')
    source = [_ for _ in range(-5, 20, 4)]
    arr = StaticArray(len(source))
    for i, value in enumerate(source):
        arr[i] = value
    print(fizz_buzz(arr))
    print(arr)

    print('\n# reverse example 1')
    source = [_ for _ in range(-20, 20, 7)]
    arr = StaticArray(len(source))
    for i, value in enumerate(source):
        arr.set(i, value)
    print(arr)
    reverse(arr)
    print(arr)
    reverse(arr)
    print(arr)

    print('\n# rotate example 1')
    source = [_ for _ in range(-20, 20, 7)]
    arr = StaticArray(len(source))
    for i, value in enumerate(source):
        arr.set(i, value)
    print(arr)
    for steps in [1, 2, 0, -1, -2, 28, -100, 2 ** 28, -2 ** 31]:
        space = " " if steps >= 0 else ""
        print(f"{rotate(arr, steps)} {space}{steps}")
    print(arr)

    print('\n# rotate example 2')
    array_size = 1_000_000
    source = [random.randint(-10 ** 9, 10 ** 9) for _ in range(array_size)]
    arr = StaticArray(len(source))
    for i, value in enumerate(source):
        arr[i] = value
    print(f'Started rotating large array of {array_size} elements')
    rotate(arr, 3 ** 14)
    rotate(arr, -3 ** 15)
    print(f'Finished rotating large array of {array_size} elements')

    print('\n# sa_range example 1')
    cases = [
        (1, 3), (-1, 2), (0, 0), (0, -3),
        (-95, -89), (-89, -95)]
    for start, end in cases:
        print(f"Start: {start: 4}, End: {end: 4}, {sa_range(start, end)}")

    print('\n# is_sorted example 1')
    test_cases = (
        [-100, -8, 0, 2, 3, 10, 20, 100],
        ['A', 'B', 'Z', 'a', 'z'],
        ['Z', 'T', 'K', 'A', '5'],
        [1, 3, -10, 20, -30, 0],
        [-10, 0, 0, 10, 20, 30],
        [100, 90, 0, -90, -200],
        ['apple']
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value
        result = is_sorted(arr)
        space = "  " if result and result >= 0 else " "
        print(f"Result:{space}{result}, {arr}")

    print('\n# find_mode example 1')
    test_cases = (
        [1, 20, 30, 40, 500, 500, 500],
        [2, 2, 2, 2, 1, 1, 1, 1],
        ["zebra", "sloth", "otter", "otter", "moose", "koala"],
        ["Albania", "Belgium", "Chile", "Denmark", "Egypt", "Fiji"]
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value

        result = find_mode(arr)
        if result:
            print(f"{arr}\nMode: {result[0]}, Frequency: {result[1]}\n")
        else:
            print("find_mode() not yet implemented\n")

    print('# remove_duplicates example 1')
    test_cases = (
        [1], [1, 2], [1, 1, 2], [1, 20, 30, 40, 500, 500, 500],
        [5, 5, 5, 4, 4, 3, 2, 1, 1], [1, 1, 1, 1, 2, 2, 2, 2]
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value
        print(arr)
        print(remove_duplicates(arr))
    print(arr)

    print('\n# count_sort example 1')
    test_cases = (
        [1, 2, 4, 3, 5], [5, 4, 3, 2, 1], [0, -5, -3, -4, -2, -1, 0],
        [-3, -2, -1, 0, 1, 2, 3], [1, 2, 3, 4, 3, 2, 1, 5, 5, 2, 3, 1],
        [10100, 10721, 10320, 10998], [-100320, -100450, -100999, -100001],
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value
        print(f"Before: {arr}")
        result = count_sort(arr)
        print(f"After : {result}")

    print('\n# count_sort example 2')
    array_size = 5_000_000
    min_val = random.randint(-1_000_000_000, 1_000_000_000 - 998)
    max_val = min_val + 998
    case = [random.randint(min_val, max_val) for _ in range(array_size)]
    arr = StaticArray(len(case))
    for i, value in enumerate(case):
        arr[i] = value
    print(f'Started sorting large array of {array_size} elements')
    result = count_sort(arr)
    print(f'Finished sorting large array of {array_size} elements')

    print('\n# sorted_squares example 1')
    test_cases = (
        [1, 2, 3, 4, 5],
        [-5, -4, -3, -2, -1, 0],
        [-3, -2, -2, 0, 1, 2, 3],
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(sorted(case)):
            arr[i] = value
        print(arr)
        result = sorted_squares(arr)
        print(result)

    print('\n# sorted_squares example 2')
    array_size = 5_000_000
    case = [random.randint(-10 ** 9, 10 ** 9) for _ in range(array_size)]
    arr = StaticArray(len(case))
    for i, value in enumerate(sorted(case)):
        arr[i] = value
    print(f'Started sorting large array of {array_size} elements')
    result = sorted_squares(arr)
    print(f'Finished sorting large array of {array_size} elements')