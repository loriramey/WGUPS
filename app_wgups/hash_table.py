# implement hash table to hold Package objects
# handles collisions using chaining
# sources for code:  Zybooks section 6, Hash Tables (all sub-sections) at https://learn.zybooks.com/zybook/WGUC950Template2023/chapter/6/section/1
# also W3Schools - Python - DSA Hash Tables found at https://www.w3schools.com/dsa/dsa_theory_hashtables.php

class HashTable:
    def __init__(self, capacity=23):
        self.capacity = capacity
        self.size = 0  #track objects in table
        self.table = [ []for _ in range(capacity) ]  #make the buckets
        self.longest_bucket = 0  # Tracks the max length of any bucket for auto-resizing

    #method to hash keys
    def hash(self, key):
        return key % self.capacity

    #function to insert new data into hash table
    def insert(self, key, value):
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

        #update largest bucket size to keep chaining in check
        self.longest_bucket = max(self.longest_bucket, len(bucket))

        #RESIZE table if any bucket exceeds chain length of 3
        if len(bucket) > 3:
            self._resize()

    # function to look up data or retrieve from hash table via package ID key
    def search(self, key):
        index = self.hash(key)
        bucket = self.table[index]

        for existing_key, value in bucket:
            if existing_key == key:
                return value   #when key is found, return value (package object)

        return None #only if key not found

    # funtion to update an object stored in the hash table
    def update(self, key, new_value):
        index = self.hash(key)
        bucket = self.table[index]

        for i, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                bucket[i] = (key, new_value)
                return True  #operation successful - key found, object updated

        return False #if key not found

    # function to delete from hash table - remove key/value pair
    def delete(self, key):
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

        def is_prime(num):
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
        return "\n".join(f"{i}: {bucket}" for i, bucket in enumerate(self.table))


