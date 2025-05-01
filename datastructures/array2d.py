from __future__ import annotations
import os
from typing import Iterator, Sequence

from datastructures.iarray import IArray
from datastructures.array import Array
from datastructures.iarray2d import IArray2D, T

class Array2D(IArray2D[T]):

    class Row(IArray2D.IRow[T]):
        def __init__(self, row_index: int, array: IArray, num_columns: int, data_type: type) -> None:
            self.row_index = row_index
            self.array = array
            self.num_columns = num_columns
            self.data_type = data_type

        def __getitem__(self, column_index: int) -> T:
            if not (0 <= column_index < self.num_columns):
                raise IndexError(f"The column index {column_index} is out of bounds.")
            
            index = self.row_index * self.num_columns + column_index

            return self.array[index]
        
        def __setitem__(self, column_index: int, value: T) -> None:
            if not (0 <= column_index < self.num_columns):
                raise IndexError(f"The column index {column_index} is out of bounds.")
            
            if not isinstance(value, self.data_type):
                raise TypeError(f"Value must be of type {self.data_type}.")
            
            index = self.row_index * self.num_columns + column_index

            self.array[index] = value
        
        def __iter__(self) -> Iterator[T]:
            for column_index in range(self.num_columns):
                yield self[column_index]
        
        def __reversed__(self) -> Iterator[T]:
            for column_index in range(self.num_columns - 1, -1, -1):
                yield self[column_index]

        def __len__(self) -> int:
            return self.num_columns
        
        def __str__(self) -> str:
            return f"[{', '.join([str(self[column_index]) for column_index in range(self.num_columns)])}]"
        
        def __repr__(self) -> str:
            return f'Row {self.row_index}: [{", ".join([str(self[column_index]) for column_index in range(self.num_columns - 1)])}, {str(self[self.num_columns - 1])}]'


    def __init__(self, starting_sequence: Sequence[Sequence[T]]=[[]], data_type=object) -> None:
        if not isinstance(starting_sequence, Sequence) or any(not isinstance(row, Sequence) for row in starting_sequence):
            raise ValueError("must be a sequence of sequences")
        
        if isinstance(starting_sequence, str):
            raise ValueError("must be a sequence of sequences")
        
        if any(not isinstance(item, data_type) for row in starting_sequence for item in row):
            raise ValueError("All items must be of the same type")
        
        num_columns = len(starting_sequence[0]) if starting_sequence else 0
        if any(len(row) != num_columns for row in starting_sequence):
            raise ValueError("must be a sequence of sequences with the same length")
        
        self.__num_rows = len(starting_sequence)
        self.__num_columns = num_columns
        self.__data_type = data_type

        flattened_data = [item for row in starting_sequence for item in row]

        self.__array = Array(flattened_data, data_type)

        self.__rows = [Array2D.Row(i, self.__array, self.__num_columns, self.__data_type) for i in range(self.__num_rows)]

        for row in range(self.__num_rows):
            for col in range(self.__num_columns):
                index = row * self.__num_columns + col
                self.__array[index] = starting_sequence[row][col]

    @staticmethod
    def empty(rows: int=0, cols: int=0, data_type: type=object) -> Array2D:
        grid = [[data_type() for _ in range(cols)] for _ in range(rows)]
        return Array2D(grid, data_type)

    def __getitem__(self, row_index: int) -> Array2D.IRow[T]:
        if not (0 <= row_index < self.__num_rows):
            raise IndexError(f"Row index {row_index} out of bounds.")
        return self.__rows[row_index]
    
    def __iter__(self) -> Iterator[Sequence[T]]:
        for row_index in range(self.__num_rows):
            yield self[row_index]
    
    def __reversed__(self):
        for row_index in range(self.__num_rows - 1, -1, -1):
            yield self[row_index]

    def __len__(self):
        return self.__num_rows
                                  
    def __str__(self) -> str: 
        return f'[{", ".join(f"{str(row)}" for row in self)}]'
    
    def __repr__(self) -> str: 
        return f'Array2D {self.__num_rows} Rows x {self.__num_columns} Columns, items: {str(self)}'

if __name__ == '__main__':
    filename = os.path.basename(__file__)
    print(f'This is the {filename} file.\nDid you mean to run your tests or program.py file?\nFor tests, run them from the Test Explorer on the left.')