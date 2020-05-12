import ctypes


class DynamicArray:
    """
    A dynamic array class akin to a simplified Python list.
    """
    def __init__(self):
        """
        Create an empty array.
        """
        self._n = 0                                      # count actual elements
        self._capacity = 1                               # default array capacity
        self._array = self._make_array(self._capacity)   # low-level array

    def __str__(self):
        """
        Return a string representation of an array

        :return: str
        """
        st = '['
        for i in range(self._capacity - 1):
            st += str(self._array[i]) + ', '
        st += str(self._array[-1]) + ']'
        return st

    def __len__(self):
        """
        Return number of elements stored in the array.

        :return: int
        """
        return self._n

    def __getitem__(self, index):
        """
        Return element at index.

        :param index: int
        :return: any
        """
        assert 0 <= index < self._n, 'Invalid Index'
        return self._array[index]

    def append(self, obj):
        """
        Add object to end of the array.
        If not enough room, double the capacity.

        :param obj: any
        """
        if self._n == self._capacity:
            self._resize(2 * self._capacity)
        self._array[self._n] = obj
        self._n += 1

    def _resize(self, capacity):
        """
        Resize internal array to capacity c.

        :param capacity: int
        """
        array_b = self._make_array(capacity)
        # Fetch all elements from A to B
        for index in range(self._n):
            array_b[index] = self._array[index]
        # Set a new reference for our A array
        self._array = array_b
        self._capacity = capacity

    @staticmethod
    def _make_array(capacity):
        """
        Return new array with capacity c.

        :param capacity: int
        :return: Ctypes Array Object
        """
        return (capacity * ctypes.py_object)()

    def remove(self, value):
        """
        Remove first occurrence of value( or  raise ValueError).
        Note: we do not consider shrinking the dynamic array in this version

        :param value: any
        """
        for index in range(self._n):
            if self._array[index] == value:
                # shift others to fill gap
                for j in range(index, self._n - 1):
                    self._array[j] = self._array[j + 1]
                # help garbage collection
                self._array[self._n - 1] = None
                self._n -= 1

        raise ValueError("Value not found!")


class SimpleDictionary:
    """
    A very simple Python version of dictionary
    with base get and set item functions.
    """
    def __init__(self):
        """
        Create a Dictionary with Python default size equal to 256
        """
        self.size = 256
        self.hash_map = [[] for _ in range(0, self.size)]

    def hash_func(self, key):
        """
        Return a hashed key

        :param key: any
        :return: hashed value
        """
        hashed_key = hash(key) % self.size
        return hashed_key

    def set(self, key, value):
        """
        Set a (key, value) tuple into our HashMap

        :param key: any
        :param value: any
        """
        hash_key = self.hash_func(key)
        key_exists = False
        slot = self.hash_map[hash_key]
        i = 0

        for key_value in slot:
            key_, value_ = key_value
            if key == key_:
                key_exists = True
                break

        if key_exists:
            slot[i] = (key, value)
        else:
            slot.append((key, value))

    def get(self, key):
        """
        Get a value by a hashed key

        :param key: any
        :return: value
        """
        hash_key = self.hash_func(key)
        slot = self.hash_map[hash_key]

        for key_value in slot:
            key_, value_ = key_value
            if key == key_:
                return value_
            else:
                raise KeyError('Key does not exist.')

    def __setitem__(self, key, value):
        """
        Set item into a dictionary

        :param key: any
        :param value: any
        :return: method
        """
        self.set(key, value)

    def __getitem__(self, key):
        """
        Return a value by a key

        :param key: any
        :return: any
        """
        return self.get(key)
