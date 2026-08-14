import pandas as pd



def list_duplicates(df : pd.DataFrame, sort_descending : bool = False) -> list[RowOccurrence]:
            """
            Returns a list of duplicated rows and their occurrence number.
            Parameters:
    
            sort_descending : bool, default False
                The output list[RowOccurrence] is sorted in descending order.
            """
            duplicated_rows = []
            for i, row in enumerate(df.duplicated()):
                if row == True:
                    temp = RowOccurrence(df.iloc[i]).row_isin_index(duplicated_rows)
                    if temp == -1:
                        duplicated_rows.append(RowOccurrence(df.iloc[i], 2))
                    else:
                        duplicated_rows[temp].add_occurrence()
    
            duplicated_rows.sort(reverse=sort_descending)
            return duplicated_rows

class RowOccurrence:
    def __init__(self, row : pd.Series , number_of_occurrences : int = 1):
        self._row = row
        self._number_of_occurrences = number_of_occurrences

    def add_occurrence(self):
        self._number_of_occurrences += 1

    def __str__(self):
         return f"Row:{self._row}\t \n\nOccurred {self._number_of_occurrences} times."

    def __eq__(self, obj : RowOccurrence):

        if not isinstance(obj, RowOccurrence):
            print(f"{obj} type is not RowOccurrence.")
            return False

        return self._row.equals(obj._row) and self._number_of_occurrences == obj._number_of_occurrences

    def __gt__(self, obj : RowOccurrence):
        return self._number_of_occurrences > obj._number_of_occurrences 

    def __lt__(self, obj : RowOccurrence):
        return self._number_of_occurrences < obj._number_of_occurrences
    
    def isin(self, obj_list : list[RowOccurrence]):
        return self in obj_list
    

    # Returns the index of the first obj with the same row value in obj_list. 
    # If self is not in obj_list, returns -1
    def row_isin_index(self, obj_list : list[RowOccurrence]):
            for i, obj in enumerate(obj_list):
                if obj._row.equals(self._row):
                    return i
            return -1

