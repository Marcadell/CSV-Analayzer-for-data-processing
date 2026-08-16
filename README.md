# CSV-Analyzer-for-data-processing
A CSV Analyzer in Python with a built-in generator of dirty data. This little project aims to highlight common problems that arise when
dealing with dirty datasets, like invalid, wrongly formatted, duplicated or missing data.
An overview of what the program can do is showed and commented in the jupyter notebook. An example on how the program can be used is shown in the main, which will:

1) Generate a sample dataset with dirty data (all data like name, age, CIE and money are fake values generated with Faker, hence no real person data is used).

2) Read the dataset (a .csv file) counting:
    - the number of rows containing missing, wrong or wrongly formatted data.
    - the number of occurrences of missing, wrong or wrongly formatted data for each field.

3) Cleans the dataset dropping rows with duplicate, invalid or missing data, calculating the average salary by province and age group.
   
4) All the results are showed as bar plots.

## Possible improvements
1) For a bigger project, the WrongFormatValues module should be rewritten, since both wrong and wrongly formatted data
   have been grouped under the same definition of "wrongly formatted data".
   For example, a negative age is well formatted as integer but has no significance.
3) The average salary for the kid age group doesn't make sense, since kids don't have one. The possible solutions could be:
        a. To drop any row within the "kid" range with a "money" value greater than zero
        b. To set the aforementioned "money" value to zero 

## Skills practiced
    - Python
    - Pandas
    - Matplotlib
    - Regular expressions
    - Handling invalid data
    - Find relationships between data
