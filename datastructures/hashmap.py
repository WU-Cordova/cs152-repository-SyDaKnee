import copy
from typing import Callable, Iterator, Optional, Tuple
from datastructures.ihashmap import KT, VT, IHashMap
from datastructures.array import Array
import pickle
import hashlib

from datastructures.linkedlist import LinkedList

class HashMap(IHashMap[KT, VT]):

    def __init__(self, number_of_buckets=7, load_factor=0.75, custom_hash_function: Optional[Callable[[KT], int]]=None) -> None:
        self._capacity = number_of_buckets
        self._size = 0
        self._load_factor = load_factor
        self._hash_function = custom_hash_function or self._default_hash_function
        self._buckets = Array(
            [LinkedList(tuple) for _ in range(self._capacity)],
        )

    def _hash(self, key: KT) -> int:
        return self._hash_function(key) % self._capacity
    
    def _resize(self):
        old_items = list(self.items())
        self._capacity *= 2
        self._buckets = Array(
            [LinkedList(tuple) for _ in range(self._capacity)],
            data_type = LinkedList
        )
        self._size = 0
        for key, value in old_items:
            self[key] = value

    def __getitem__(self, key: KT) -> VT:
        bucket = self._buckets[self._hash(key)]
        for k, v in bucket:
            if k == key:
                return v
        raise KeyError(f"The key {key} is not found.")

    def __setitem__(self, key: KT, value: VT) -> None:        
        bucket = self._buckets[self._hash(key)]
        for item in bucket:
            if item[0] == key:
                bucket.remove(item)
                bucket.append((key, value))
                return
        bucket.append((key, value))
        self._size += 1
        if self._size / self._capacity > self._load_factor:
            self._resize()

    def keys(self) -> Iterator[KT]:
        return iter(self)
    
    def values(self) -> Iterator[VT]:
        for bucket in self._buckets:
            for _, v in bucket:
                yield v

    def items(self) -> Iterator[Tuple[KT, VT]]:
        for bucket in self._buckets:
            for pair in bucket:
                yield pair
            
    def __delitem__(self, key: KT) -> None:
        bucket = self._buckets[self._hash(key)]
        for item in bucket:
            if item[0] == key:
                bucket.remove(item)
                self._size -= 1
                return
        raise KeyError(f"The key {key} is not found.")
    
    def __contains__(self, key: KT) -> bool:
        bucket = self._buckets[self._hash(key)]
        return any(k == key for k, _ in bucket)
    
    def __len__(self) -> int:
        return self._size
    
    def __iter__(self) -> Iterator[KT]:
        for bucket in self._buckets:
            for k, _ in bucket:
                yield k
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, HashMap) or len(self) != len(other):
            return False
        for k, v in self.items():
            if k not in other or other[k] != v:
                return False
        return True

    def __str__(self) -> str:
        return "{" + ", ".join(f"{key}: {value}" for key, value in self) + "}"
    
    def __repr__(self) -> str:
        return f"HashMap({str(self)})"

    @staticmethod
    def _default_hash_function(key: KT) -> int:
        """
        Default hash function for the HashMap.
        Uses Pickle to serialize the key and then hashes it using SHA-256. 
        Uses pickle for serialization (to capture full object structure).
        Falls back to repr() if the object is not pickleable (e.g., open file handles, certain C extensions).
        Returns a consistent integer hash.
        Warning: This method is not suitable
        for keys that are not hashable or have mutable state.

        Args:
            key (KT): The key to hash.
        Returns:
            int: The hash value of the key.
        """
        try:
            key_bytes = pickle.dumps(key)
        except Exception:
            key_bytes = repr(key).encode()
        return int(hashlib.md5(key_bytes).hexdigest(), 16)