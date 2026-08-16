from pathlib import Path
from data_analysis import CSVDataAnalyzer 
import dirty_data_generator as ddg
import pandas as pd

WORKDIR = Path.cwd()
DATAPATH = WORKDIR/"data/"
filename = DATAPATH/"dati_vari.csv"
ddg.generate_dirty_csv(1200, filename, "it_IT", include_duplicates=True, max_number_of_duplicates=30)


pd.set_option({"display.max_columns": 200, "display.max_rows": 200})

myAnalyzer = CSVDataAnalyzer()
myAnalyzer.read_data(filename)
