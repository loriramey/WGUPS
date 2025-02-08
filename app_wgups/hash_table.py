# implement hash table to hold Package objects
# handles collisions using chaining
# sources for code:  Zybooks section 6, Hash Tables (all sub-sections) at https://learn.zybooks.com/zybook/WGUC950Template2023/chapter/6/section/1
# also W3Schools - Python - DSA Hash Tables found at https://www.w3schools.com/dsa/dsa_theory_hashtables.php

class HashTable:
    def __init__(self, capacity=23):
        """
        Initializes a hash table with a specified capacity.
        This constructor sets up the hash table with an initial number of buckets,
        initializes size tracking, and prepares for handling collisions using chaining.

        Args:
            capacity (int, optional): The initial number of buckets in the hash table.
                                      Defaults to 23 (a prime number to reduce collisions).
        Attributes:
            capacity (int): The number of buckets in the hash table.
            size (int): The current number of key-value pairs stored in the table.
            table (list): A list of empty lists, where each sublist represents a bucket.
            longest_bucket (int): Tracks the maximum bucket size for auto-resizing logic.
        Returns:
            None
        """
        self.capacity = capacity
        self.size = 0  #track objects in table
        self.table = [ []for _ in range(capacity) ]  #make the buckets
        self.longest_bucket = 0  # Tracks the max length of any bucket for auto-resizing


    #function to hash keys
    def hash(self, key):
        """
        Computes the hash value for a given key.
        This function applies the modulo operation to determine the appropriate
        index in the hash table's bucket list.

        Args:
            key (int): The key to be hashed. It must be an integer.
        Returns:
            int: The computed index in the hash table (0 to capacity - 1).
        """
        return key % self.capacity


    #function to insert new data into hash table
    def insert(self, key, value):
        """
        Inserts a new key-value pair into the hash table.
        If the key already exists, its value is updated.
        If a bucket exceeds a length of 3 (due to collisions), the hash table resizes automatically.

        Args:
            key (int): The key for the data entry. Must be an integer.
            value (any): The value associated with the key. Can be any data type.
        Returns:
            None: The function does not return anything. It modifies the hash table in place.
        """
        index = self.hash(key)
        bucket = self.table[index]

        #update if key already exists
        for i, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                bucket[i] = (key, value)
                return

        #otherwise insert new key-value pair
        bucket.append((key, value))
        self.size += 1

        #update the largest bucket size to keep chaining in check
        self.longest_bucket = max(self.longest_bucket, len(bucket))

        #RESIZE table if any bucket exceeds chain length of 3
        if len(bucket) > 3:
            self._resize()


    # function to look up data or retrieve from hash table via package ID key
    def lookup(self, key):
        """
        Retrieves a value from the hash table using the given key.
        This function searches for the key within the appropriate bucket.
        If the key is found, it returns the associated value; otherwise, it returns None.

        Args:
            key (int): The key for the data entry. Must be an integer.
        Returns:
            any: The value associated with the key if found,
            or None if the key does not exist in the hash table.
        """
        index = self.hash(key)
        bucket = self.table[index]

        for existing_key, value in bucket:
            if existing_key == key:
                return value   #when key is found, return value (package object)

        return None #only if key not found


    # function to update an object stored in the hash table
    def update(self, key, new_value):
        """
        Updates the value associated with a given key in the hash table.
        This function searches for the key in the appropriate bucket.
        If the key exists, it updates the value and returns True.
        If the key is not found, it returns False.

        Args:
            key (int): The key identifying the entry to update.
            new_value (any): The new value to associate with the key.
        Returns:
            bool: True if the update was successful, False if the key was not found.
        """
        index = self.hash(key)
        bucket = self.table[index]

        for i, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                bucket[i] = (key, new_value)
                return True  #operation successful - key found, object updated

        return False #if key not found


    # function to delete from hash table - remove key/value pair
    def delete(self, key):
        """
        Removes a key-value pair from the hash table.
        This function searches for the specified key in the hash table.
        If found, it deletes the key-value pair and reduces the size count.
        If the key is not found, it returns False.

        Args:
            key (int): The key of the entry to remove.
        Returns:
            bool: True if the key was successfully deleted, False if the key was not found.
        """
        index = self.hash(key)
        bucket = self.table[index]

        for i, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                del bucket[i]   #remove this key value pair
                self.size -= 1   #reduce load count of hash table
                return True  #successful find and delete

        return False #if key not found


    #function to RESIZE table - resizes to the next prime number for modulo
    def _resize(self):
        """
        Dynamically resizes the hash table to maintain efficiency.
        This function increases the table size to the next prime number
        greater than twice the current capacity to maintain optimal hashing performance.
        It then rehashes all existing key-value pairs into the new table.

        Args:
            None
        Returns:
            None: The function modifies the hash table in place.
        """
        new_capacity = self._next_prime(self.capacity*2)
        new_table = [ [] for _ in range(new_capacity) ]

        self.longest_bucket = 0  # Reset max bucket length tracker

        for bucket in self.table:
            for key, value in bucket:
                new_index = key % new_capacity
                new_table[new_index].append((key, value))

        self.capacity = new_capacity
        self.table = new_table
        self.longest_bucket = max(self.longest_bucket, len(new_table))


    #function needed for resize to determine next prime to use as new table size
    def _next_prime(self, n):
        """
        Finds the next prime number greater than or equal to `n`.
        This function is used to determine the next prime number when resizing
        the hash table to optimize hashing efficiency. It ensures that the new
        table size is a prime number to reduce collisions.

        Args:
            n (int): The starting number to check for the next prime.
        Returns:
            int: The next prime number greater than or equal to `n`.
        """
        def is_prime(num):
            """
            Checks whether a given number is prime.
            A prime number is only divisible by 1 and itself. This function
            determines primality by checking divisibility up to the square root of the number.

            Args:
                num (int): The number to check for primality.
            Returns:
                bool: True if the number is prime, False otherwise.
            """
            if num < 2:
                return False
            for i in range(2, int(num ** 0.5) + 1):
                if num % i == 0:
                    return False
            return True

        while not is_prime(n):
            n += 1

        return n


    #print a text copy of hash table contents
    def __str__(self):
        """
        Returns a string representation of the hash table.
        This function converts the hash table's internal structure into a formatted
        string where each bucket is displayed with its index.

        Args:
            None
        Returns:
            str: A multi-line string representing the hash table, where each line
                 corresponds to a bucket index and its contents.
        """
        return "\n".join(f"{i}: {bucket}" for i, bucket in enumerate(self.table))
