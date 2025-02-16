# datastructures.array.Array

""" This module defines an Array class that represents a one-dimensional array. 
    See the stipulations in iarray.py for more information on the methods and their expected behavior.
    Methods that are not implemented raise a NotImplementedError until they are implemented.
"""

from __future__ import annotations
from collections.abc import Sequence
import os
from typing import Any, Iterator, overload
import numpy as np
from numpy.typing import NDArray
import copy


from datastructures.iarray import IArray, T


class Array(IArray[T]):  

    def __init__(self, starting_sequence: Sequence[T] = [], data_type: type = object) -> None:

        if not isinstance(starting_sequence, Sequence):
            raise ValueError("This sequence type is not a valid sequence type.")
        
        if not isinstance(data_type, type):
            raise TypeError("This data type is not a valid data type.")
        
        if not all(isinstance(item, data_type) for item in starting_sequence):
            raise TypeError("All items in the starting sequence must be of the same data type.")
        
        self.__item_count = len(starting_sequence)
        self.__items = np.empty(self.__item_count, dtype = object)
        self.__data_type = data_type

        for i, item in enumerate(starting_sequence):
            self.__items[i] = copy.deepcopy(item) 

    @overload
    def __getitem__(self, index: int) -> T: ...
    @overload
    def __getitem__(self, index: slice) -> Sequence[T]: ...
    def __getitem__(self, index: int | slice) -> T | Sequence[T]:
        if isinstance(index, slice):
            return Array(list(self.__items[index]), self.__data_type)
        elif isinstance(index, int):
            if index < 0 or index >= self.__item_count:
                raise IndexError("The index is out of range.")
            return self.__items[index]
        else:
            raise TypeError("This index type is invalid.")

    def __setitem__(self, index:int, value: T) -> None:
        if not isinstance(index, int):
            raise TypeError("The index must be an integer.")
        if index < 0 or index >= self.__item_count:
            raise IndexError("The index is out of range.")
        if not isinstance(value, self.__data_type):
            raise TypeError("The data type of the value does not match the array.")
        
    def append(self, data: T) -> None:
        if not isinstance(data, self.__data_type):
            raise TypeError("This item is not the same type as the array.")
        
        new_items = np.empty(self.__item_count + 1, dtype = object)
        
        for i in range(self.__item_count):
            new_items[i] = self.__items[i]

        new_items[self.__item_count] = copy.deepcopy(data)

        self.__items = new_items
        self.__item_count += 1

    def append_front(self, data: T) -> None:
        if not isinstance(data, self.__data_type):
            raise TypeError("This item is not the same type as the array.")
        
        new_items = np.empty(self.__item_count + 1, dtype = object)
        new_items[0] = copy.deepcopy(data)

        for i in range(self.__item_count):
            new_items[i + 1] = self.__items[i]

        self.__items = new_items
        self.__item_count += 1

    def pop(self) -> None:
        if self.__item_count == 0:
            raise IndexError("The array is empty, you cannot remove anything.")
        
        item = self.__items[self.__item_count - 1]
        removed_item = np.empty(self.__item_count - 1, dtype = object)

        for i in range(self.__item_count - 1):
            removed_item[i] = self.__items[i]

        self.__items = removed_item
        self.__item_count -= 1

        return item
    
    def pop_front(self) -> None:
        if self.__item_count == 0:
            raise IndexError("The array is empty, you cannot remove anything.")
        
        item = self.__items[0]
        removed_item = np.empty(self.__item_count - 1, dtype = object)

        for i in range(1, self.__item_count):
            removed_item[i - 1] = self.__items[i]

        self.__items = removed_item
        self.__item_count -= 1

        return item

    def __len__(self) -> int: 
        return self.__item_count

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Array):
            return False
        
        if self.__item_count != other.__item_count:
            return False
        
        return all(self[i] == other[i] for i in range(self.__item_count))
    
    def __iter__(self) -> Iterator[T]:
        return iter(self.__items[:self.__item_count])

    def __reversed__(self) -> Iterator[T]:
        return (self[i] for i in range(self.__item_count -1, -1, -1))

    def __delitem__(self, index: int) -> None:
        if not (0 <= index < self.__item_count):
            raise IndexError("The index is out of range.")
        
        for i in range(index, self.__item_count - 1):
            self.__items[i] = self.__items[i + 1]

        self.__item_count -= 1

    def __contains__(self, item: Any) -> bool:
       if item in self.__items:
           return True
       else:
           return False

    def clear(self) -> None:
        self.__item_count = 0
        self.__items = np.empty(0, dtype = object)

    def __str__(self) -> str:
        return '[' + ', '.join(str(item) for item in self) + ']'
    
    def __repr__(self) -> str:
        return f'Array {self.__str__()}, Logical: {self.__item_count}, Physical: {len(self.__items)}, type: {self.__data_type}'
    

if __name__ == '__main__':
    filename = os.path.basename(__file__)
    print(f'This is the {filename} file.\nDid you mean to run your tests or program.py file?\nFor tests, run them from the Test Explorer on the left.')