from pathlib import Path
from data_analysis import CSVDataAnalyzer 
from data_analysis import MispelledRow
import dirty_data_generator as ddg
import pandas as pd


WORKDIR = Path.cwd()
DATAPATH = WORKDIR/"data/"
filename = DATAPATH/"dati_vari.csv"
#ddg.generate_dirty_csv(200, filename, "it_IT", include_duplicates=True, max_number_of_duplicates=30)


#pd.set_option({"display.max_columns": 200, "display.max_rows": 200})

myAnalyzer = CSVDataAnalyzer()
myAnalyzer.read_data(filename)
#duplicated_data = myAnalyzer.list_duplicates(sort_descending=False)

duplicated_data = myAnalyzer.list_and_drop_duplicates(_sort_descending = False, printLog=True,
                                                      _inplace = False, _keep = 'first')
for row in duplicated_data:
    print(row)

print(myAnalyzer._df)

test = MispelledRow(myAnalyzer._df.iloc[3])
print(test)
