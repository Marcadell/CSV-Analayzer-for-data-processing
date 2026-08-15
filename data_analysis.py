from __future__ import annotations
import pandas as pd
import DuplicatedValues as DV
import WrongFormatValues as WF
import matplotlib.pyplot as plt
import numpy as np



class CSVDataAnalyzer:

    def __init__(self, df : pd.DataFrame = None):
        self._df = df
        self._header = None
        self._duplicates = []
        self._wrongFormat = []
        self._missing = []
        self._missingName = 0
        self._missingProvince = 0
        self._missingCIE = 0
        self._missingAge = 0
        self._missingMoney = 0
        self._wrongName = 0
        self._wrongAge = 0
        self._wrongProvince = 0
        self._wrongCIE = 0
        self._wrongMoney = 0


    def read_data(self, filename):
        if "csv" in str(filename):
            self._df = pd.read_csv(filename)
            self._header = self._df.columns.tolist()
        else:
            print("Unsupported file format")

    
    def update_duplicates(self):
        self._duplicates = DV.list_duplicates(self._df)


    def update_wrongFormat(self):
        self._wrongFormat = WF.list_wrongFormat_rows(self._df)


    def update_missing(self):
        self._missing = self._df[self._df.isna().any(axis = 1)]
                    
            
    def update_missing_values(self):

        self._missingName = 0
        self._missingProvince = 0
        self._missingCIE = 0
        self._missingAge = 0
        self._missingMoney = 0

        for i, row in self._df.iterrows():

            if pd.isna(row["name"]):
                self._missingName +=1

            if pd.isna(row["province"]):
                self._missingProvince += 1

            if pd.isna(row["cie"]):
                self._missingCIE += 1

            if pd.isna(row["age"]):
                self._missingAge += 1

            if pd.isna(row["money"]):
                self._missingMoney += 1


    def update_wrongFormat_values(self):
        self._wrongName = 0
        self._wrongProvince = 0
        self._wrongCIE = 0

        for row in self._wrongFormat:
            if row["name"]:
                self._wrongName += 1
            if row["age"]:
                self._wrongAge += 1
            if row["province"]:
                self._wrongProvince += 1
            if row["cie"]:
                self._wrongCIE += 1
            if row["money"]:
                self._wrongMoney += 1
            


    def print_dirty_data_statistics(self, update : bool = True):

        if(update):
            self.update_duplicates()
            self.update_missing()
            self.update_missing_values()
            self.update_wrongFormat()
            self.update_wrongFormat_values()

        print("The number of missing and wrong occurences include duplicates.")
        print(f"Rows:\t{self._df.shape[0]}")
        print(f"Duplicates:\t{len(self._duplicates)}")

        print(f"Wrong format:\t{len(self._wrongFormat)}")
        print(f"|\n|\n---- wrong name:\t{self._wrongName}")
        print(f"|\n|\n---- wrong age:\t{self._wrongAge}")
        print(f"|\n|\n---- wrong province:\t{self._wrongProvince}")
        print(f"|\n|\n---- wrong CIE:\t{self._wrongCIE}")
        print(f"|\n|\n---- wrong money:\t{self._wrongMoney}")
        
        print(f"\nMissing:\t{len(self._missing)}")
        print(f"|\n|\n---- missing name:\t{self._missingName}")
        print(f"|\n|\n---- missing age:\t{self._missingAge}")
        print(f"|\n|\n---- missing province:\t{self._missingProvince}")
        print(f"|\n|\n---- missing CIE:\t{self._missingCIE}")
        print(f"|\n|\n---- missing money:\t{self._missingMoney}")

    def show_dirty_data_statistics(self, update : bool = True):

        if(update):
            self.update_duplicates()
            self.update_missing()
            self.update_missing_values()
            self.update_wrongFormat()
            self.update_wrongFormat_values()


        fields = ("Name", "Age", "Province", "CIE", "Money")
        fields_values = {
                         "Missing values" : (self._missingName, self._missingAge,
                                               self._missingProvince, self._missingCIE,
                                               self._missingMoney),
                         "Wrong Format values" : (self._wrongName, self._wrongAge,
                                               self._wrongProvince, self._wrongCIE,
                                               self._wrongMoney)}
        

        fig, ax = plt.subplots(layout = "constrained")
        res = ax.grouped_bar(fields_values, tick_labels=fields, group_spacing=1)
        for container in res.bar_containers:
            ax.bar_label(container, padding = 3)

        ax.set_ylabel("Number of occurences")
        ax.set_title("Dirty data statistics")
        ax.legend(loc='upper center', ncols = 3)
        plt.show()

        

    def wealth_by_province(self):
        df2 = self._df.copy()

        df2 = WF.drop_wrongFormat_rows(df2, ["money", "province"]) # Remove dirty data
        df2["money"] = pd.to_numeric(df2["money"]) #Since some rows have the "$" character, "money" column is treated as a str type

        group = df2.groupby(by ="province", dropna = True)["money"]
        group_mean = group.mean().sort_values(ascending = False)
        print("The five wealthiest provinces:\n",group_mean.iloc[0:5])
        print("The five poorest provinces:\n", group_mean.iloc[len(group_mean)-5 : len(group_mean)])
        print(group_mean)
                
                        
    


   
       

    



