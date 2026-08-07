import pandas as pd
import numpy as np

# Per questa funzione va scritto il test
class CSVDataAnalyzer:
    def __init__(self, df : pd.DataFrame = None):
        self._df = df

    def read_data(self, filename):
        if "csv" in str(filename):
            self._df = pd.read_csv(filename)
        else:
            print("Unsupported file format")

    def list_duplicates(self, sort_descending : bool = False) -> list[DuplicatedRow]:
        """
        Returns a list of duplicated rows and their occurrence number.
        Parameters:

        sort_descending : bool, default False
            The output list[DuplicatedRow] is sorted in descending order.
        """
        duplicated_rows = []
        for i, row in enumerate(self._df.duplicated()):
            if row == True:
                temp = DuplicatedRow(self._df.iloc[i]).row_isin_index(duplicated_rows)
                if temp == -1:
                    duplicated_rows.append(DuplicatedRow(self._df.iloc[i], 2))
                else:
                    duplicated_rows[temp].add_occurrence()

        duplicated_rows.sort(reverse=sort_descending)
        return duplicated_rows



    def list_and_drop_duplicates(self, _sort_descending : bool = False, printLog : bool = False, 
                                 _inplace : bool = False, _keep : 
                                 {'first', 'last', False} = 'first') -> list[DuplicatedRow]:
        """
        Returns a list of duplicated rows and their occurrence number, removing the duplicates from the DataFrame.
        Parameters:

        sort_descending : bool, default False
            The output list[DuplicatedRow] is sorted in descending order.
        printLog : bool, default False
            Print a comparison between the clean DataFrame and the original one.
        
        df.drop parameters (source: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.drop_duplicates.html):
        
        keep : {‘first’, ‘last’, False}, default ‘first’
            Determines which duplicates (if any) to keep.
                ‘first’ : Drop duplicates except for the first occurrence.
                ‘last’ : Drop duplicates except for the last occurrence.
                False : Drop all duplicates.

        inplace : bool, default False
            Whether to modify the DataFrame rather than creating a new one.
        """

        temp = self.list_duplicates(sort_descending = _sort_descending)
        temp2 = self._df
        self._df = self._df.drop_duplicates(inplace = _inplace, keep = _keep)
        if(printLog):
            print(f"List of duplicates, in {"descending" if _sort_descending else "ascending"} order.")
            for x in temp:
                print(x)
            print(f"Original DataFrame size:{temp2.size}\tNew DataFrame size:{self._df.size}")
        return self._df

class DuplicatedRow:
    def __init__(self, row : pd.Series , number_of_occurrences : int = 1):
        self._row = row
        self._number_of_occurrences = number_of_occurrences

    def add_occurrence(self):
        self._number_of_occurrences += 1

    def __str__(self):
         return f"Row:{self._row}\t \n\nOccurred {self._number_of_occurrences} times."

    def __eq__(self, obj : DuplicatedRow):

        if not isinstance(obj, DuplicatedRow):
            print(f"{obj} type is not DuplicatedRow.")
            return False

        return self._row.equals(obj._row) and self._number_of_occurrences == obj._number_of_occurrences

    def __gt__(self, obj : DuplicatedRow):
        return self._number_of_occurrences > obj._number_of_occurrences 

    def __lt__(self, obj : DuplicatedRow):
        return self._number_of_occurrences < obj._number_of_occurrences
    
    def isin(self, obj_list : list[DuplicatedRow]):
        return self in obj_list
    

    # Returns the index of the first obj with the same row value in obj_list. 
    # If self is not in obj_list, returns -1
    def row_isin_index(self, obj_list : list[DuplicatedRow]):
            for i, obj in enumerate(obj_list):
                if obj._row.equals(self._row):
                    return i
            return -1
    
