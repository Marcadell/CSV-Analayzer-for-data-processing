from __future__ import annotations
import pandas as pd
import DuplicatedValues as DV


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


    def list_and_drop_duplicates(self, sort_descending : bool = False, printLog : bool = False,
                                 keep : {'first', 'last', False} = 'first') -> list[DV.RowOccurrence]:
        """
        Returns a list of duplicated rows and their occurrence number, removing the duplicates from the DataFrame.
        Parameters:

        sort_descending : bool, default False
            The output list[RowOccurrence] is sorted in descending order.
        printLog : bool, default False
            Print a comparison between the clean DataFrame and the original one.
        
        for df.drop parameters see https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.drop_duplicates.html
        
        """

        temp = DV.list_duplicates(df = self._df, sort_descending = sort_descending)
        temp2 = self._df.copy()
        self._df.drop_duplicates(inplace = True, keep = keep)
        if(printLog):
            print(f"List of duplicates, in {"descending" if sort_descending else "ascending"} order.")
            for x in temp:
                print(x)
            print(f"Original DataFrame size:{temp2.size}\tNew DataFrame size:{self._df.size}")
        return self._df


    
                        
    


   
       

    



