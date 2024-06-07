# Name: Mark Bastion-Cavnar
# OSU Email: bastionm@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment 6:HashMap
# Due Date:6/6/2024
# Description: My submission for a Separate Chaining HashMap


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Add a key-value pair to the hash map. If the key already exists,
        update its value. Resize the table if the load factor is greater than or equal to 1.0.
        """
        index = self._hash_function(key) % self._capacity
        bucket = self._buckets[index]

        # Check if the key is already present and remove it if necessary
        if bucket.contains(key):
            bucket.remove(key)
        else:
            self._size += 1

        # Insert the new key-value pair
        bucket.insert(key, value)

        # Debug print to verify the put operation
        print(f"Put: ({key}, {value}) into bucket index {index}")

        # Resize the table if the load factor is greater than or equal to 1.0
        if self.table_load() >= 1.0:
            print(f"Load factor >= 1.0, resizing table. Current load factor: {self.table_load()}")
            self.resize_table(self._capacity * 2)

    def table_load(self) -> float:
        """
        Return the current load factor of the table.
        """
        if self._capacity == 0:  # Prevent division by zero
            return 0
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Return the number of empty buckets in the hash map.
        """
        empty_count = 0
        for i in range(self._capacity):
            if self._buckets[i].length() == 0:
                empty_count += 1
        return empty_count

    def resize_table(self, new_capacity: int) -> None:
        """
        Resize the hash table to a new capacity, rehashing all key-value pairs.
        """
        # Ensure the new capacity is not less than 1
        if new_capacity < 1:
            return

        # Ensure the new capacity is a prime number
        new_capacity = self._next_prime(new_capacity)
        new_buckets = DynamicArray()

        # Initialize new buckets
        for _ in range(new_capacity):
            new_buckets.append(LinkedList())

        # Rehash all key-value pairs into the new buckets
        for i in range(self._capacity):
            current = self._buckets[i]._head
            while current:
                # Calculate the new bucket index using the new capacity
                index = self._hash_function(current.key) % new_capacity
                # Insert the key-value pair into the new bucket
                new_buckets[index].insert(current.key, current.value)
                current = current.next

        # Update the hash map with the new buckets and capacity
        self._buckets = new_buckets
        self._capacity = new_capacity

        # Debug print to verify resizing
        print(f"Resized table to new capacity: {self._capacity}, number of items: {self._size}")

    def table_load(self) -> float:
        """
        Return the current load factor of the table.
        """
        if self._capacity == 0:  # Prevent division by zero
            return 0
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Return the number of empty buckets in the hash map.
        """
        empty_count = 0
        for i in range(self._capacity):
            if self._buckets[i].length() == 0:
                empty_count += 1
        return empty_count

    def get(self, key: str) -> object:
        """
        Retrieve the value associated with the given key. Return None if the key does not exist.
        """
        index = self._hash_function(key) % self._capacity
        bucket = self._buckets[index]

        node = bucket.contains(key)
        if node:
            return node.value
        return None

    def contains_key(self, key: str) -> bool:
        """
        Check if the given key exists in the hash map.
        """
        index = self._hash_function(key) % self._capacity
        bucket = self._buckets[index]

        if bucket.contains(key):
            return True
        return False

    def remove(self, key: str) -> None:
        """
        Remove the key-value pair associated with the given key from the hash map.
        """
        index = self._hash_function(key) % self._capacity
        bucket = self._buckets[index]

        if bucket.contains(key):
            bucket.remove(key)
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Return a DynamicArray containing all key-value pairs in the hash map.
        """
        result = DynamicArray()
        for i in range(self._capacity):
            current = self._buckets[i]._head  # Use '_head' instead of 'head'
            while current:
                result.append((current.key, current.value))
                current = current.next
        return result

    def clear(self) -> None:
        """
        Remove all key-value pairs from the hash map.
        """
        for i in range(self._capacity):
            self._buckets[i] = LinkedList()
        self._size = 0


def find_mode(arr: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Find the mode(s) in the given DynamicArray. Return a tuple containing a
    DynamicArray of the mode(s) and their frequency.
    """
    hash_map = HashMap()
    max_frequency = 0
    mode_array = DynamicArray()

    # Count the frequency of each element in the array
    for i in range(arr.length()):
        value = arr[i]
        frequency = hash_map.get(value)
        if frequency is None:
            hash_map.put(value, 1)
            frequency = 1
        else:
            hash_map.put(value, frequency + 1)
            frequency += 1

        if frequency > max_frequency:
            max_frequency = frequency

    # Find all elements with the highest frequency
    for i in range(arr.length()):
        value = arr[i]
        if hash_map.get(value) == max_frequency:
            # Check if the value is already in the mode_array
            already_in_array = False
            for j in range(mode_array.length()):
                if mode_array[j] == value:
                    already_in_array = True
                    break
            if not already_in_array:
                mode_array.append(value)

    return mode_array, max_frequency




# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
