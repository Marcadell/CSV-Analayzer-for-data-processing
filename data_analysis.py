from __future__ import annotations
import pandas as pd
import numpy as np

TEXT_FIELDS = ["name", "country", "job"]

# Per questa funzione va scritto il test
class CSVDataAnalyzer:
    def __init__(self, df : pd.DataFrame = None):
        self._df = df
        self._header = None

    def read_data(self, filename):
        if "csv" in str(filename):
            self._df = pd.read_csv(filename)
            self._header = self._df.columns.tolist()
        else:
            print("Unsupported file format")

    def list_duplicates(self, sort_descending : bool = False) -> list[RowOccurrence]:
        """
        Returns a list of duplicated rows and their occurrence number.
        Parameters:

        sort_descending : bool, default False
            The output list[RowOccurrence] is sorted in descending order.
        """
        duplicated_rows = []
        for i, row in enumerate(self._df.duplicated()):
            if row == True:
                temp = RowOccurrence(self._df.iloc[i]).row_isin_index(duplicated_rows)
                if temp == -1:
                    duplicated_rows.append(RowOccurrence(self._df.iloc[i], 2))
                else:
                    duplicated_rows[temp].add_occurrence()

        duplicated_rows.sort(reverse=sort_descending)
        return duplicated_rows



    def list_and_drop_duplicates(self, _sort_descending : bool = False, printLog : bool = False, 
                                 _inplace : bool = False, _keep : 
                                 {'first', 'last', False} = 'first') -> list[RowOccurrence]:
        """
        Returns a list of duplicated rows and their occurrence number, removing the duplicates from the DataFrame.
        Parameters:

        sort_descending : bool, default False
            The output list[RowOccurrence] is sorted in descending order.
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

class MispelledRow:

    def __init__(self, row : pd.Series):
        self._row = row
        self._mispelledFields = dict.fromkeys(TEXT_FIELDS, False)
        self._correctedFields = dict.fromkeys(TEXT_FIELDS)
        self.hasMispelledName(self._row["name"])
        self.hasMispelledJob(self._row["job"])

    def __str__(self):
        s = ""
        for field in TEXT_FIELDS:
           s = s + f"Original:{self._row[field]}\nNew:{self._mispelledFields[field]}\n\n"
        return s



    def correctFields(self):
       for field in TEXT_FIELDS:
           if self._mispelledFields[field]:

               if field == "name" or field == "country":
                    self._correctedFields[field] = self.correctName(self._row[field])

               if field == "job":
                   self._correctedFields[field] = self.correctJob(self._row[field])
           else:
               self._correctedFields[field] = self._row[field]


    def correctJob(self, job : str) -> str:
        if pd.isna(job):
            return ""
        
        elif not isinstance(job, str):
           raise ValueError(f"{job} is not a string!")
        
        
        new = ""

        for i, x in enumerate(self._row["job"].replace(",", " ").split()):
            if i == 0:
                new = new + str(x).upper()
            else:
                new = new+ str(x).lower()
        return new
                   
                   
    def correctName(self, name : str) -> str:
        if pd.isna(name):
                    return ""
        
        elif not isinstance(name, str):
           raise ValueError(f"{name} is not a string!")


        new = ""

        for word in self._row["name"].replace("'", " ").split(" "):
            for i, x in word:
                if i == 0:
                    new = new + str(x).upper()
                else:
                    new = new+ str(x).lower()
        return new


   
    def hasMispelledName(self, name : str) -> bool:
        """
            Names are supposed to be spelled like this:
            Mario Augusto De Chirico.
            Returns True if:
                - The first letter of at least one word is lower
                - The other letters are capitalized
            The same function can be used for country names, for example:
                Stati Uniti D'America
        """
        if not isinstance(name, str):
            raise ValueError(f"Value {name} is not a string!")

        if name is None:
            return False # Empty fields are not flagged as Mispelled
    
        temp = name.replace("'", " ").split(" ") #Some countries have "'" chars
        for word in temp:
            for i, char in enumerate(word):
                if i == 0 and str(char).islower():
                    self._mispelledFields["name"] = True
                    return True
                elif i != 0 and str(char).isupper():
                    self._mispelledFields["name"] = True  
                    return True          

    def hasMispelledJob(self, job : str):
       """
        Names are supposed to be spelled like this:
        Ingegnere meccanico, controllo qualità.
        Returns True if:
            - The first letter of the first word is lower
            - The other letters are capitalized
        """
       if not isinstance(job, str):
           raise ValueError(f"{job} is not a string!")

       if job is None:
           return False # Empty fields are not flagged as mispelled
       
       temp = job.replace(",", " ").split() #Some jobs have both commas and spaces
       for i, word in enumerate(temp):
           if i == 0:
               if str(word[0]).islower():
                    self._mispelledFields["job"] = True
                    return True
               else:
                    for x in word:
                        if str(x).isupper():
                            self._mispelledFields["job"] = True 
                            return True        
           else:
               for x in word:
                   if str(x).isupper():
                       self._mispelledFields["job"] = True
                       return True
           self._mispelledFields["job"] = False
           return False

   
       

    



