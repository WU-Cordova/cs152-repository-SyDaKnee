from typing import Iterable, Optional
from datastructures.ibag import IBag, T

class Bag(IBag[T]):
    def __init__(self, *items: Optional[Iterable[T]]) -> None:
        self.__bag = [] # This is initializing the bag as an empty list.
        
    def add(self, item: T) -> None:
        if item is None: # If the item is an unaccpeted data type,
            raise TypeError("You cannot add nothing to the bag.") # Raise a TypeError.
        self.__bag.append(item) # Else, add the items to the bag. 
        
    def remove(self, item: T) -> None:
        if item not in self.__bag: # If the item isn't in the bag to being with,
            raise ValueError("You can't remove this item, it isn't in your bag.") # Raise a ValueError.
        else:
            self.__bag.remove(item)
        
    def count(self, item: T) -> int:
        return self.__bag.count(item) # Return the number of occurences of a specific item. 

    def __len__(self) -> int:
        return len(self.__bag) # Return the amount of items in the bag. 

    def distinct_items(self) -> int:
        distinct_items = set(self.__bag) # Since sets can't contain duplicate items, convert the bag into a set. 
        return distinct_items # Return the set values. 

    def __contains__(self, item) -> bool:
        if item in self.__bag: # If an item is in the bag,
            return True # Return True.
        else:
            return False

    def clear(self) -> None:
        return self.__bag.clear() # Clear all of the items out of the bag. 