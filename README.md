# CSV-Analyzer-for-data-processing
A CSV Analyzer in Python with a built-in generator of dirty data. This little project aims to point out common problems when
dealing with dirty datasets, like invalid, wrongly formatted, duplicated or missing data.
An overview of what the program can do is showed and commented in the jupyter notebook. An example on how the program can be used is shown in the main, which will:

1) Generate a sample dataset with dirty data (all data like name, age, CIE and money are fake values generated with Faker, hence no real person data is used).

2) Read the dataset (a .csv file) counting:
    - the number of rows containing missing, wrong or wrongly formatted data.
    - the number of occurrences of missing, wrong or wrongly formatted data for each field.

3) Cleans the dataset dropping rows with duplicate, invalid or missing data, calculating the average salary by province and age group.
   
4) All the results are showed as bar plots.

## Possible improvements
    - For a bigger project, the WrongFormatValues module should be rewritten, since both wrong and wrongly format data
      have been grouped under the same definition of "wrongly format data". For example, a negative age is well formatted as integer but has no significate.
    - The average salary for the kid age group has no sense, since kids don't have one. The possible solutions could be:
        a. To drop any row within the "kid" range with a "money" value greater than zero
        b. To set the aforementioned "money" value to zero 

## Skills practiced
    - Python
    - Pandas
    - Matplotlib
    - Regular expressions
    - Handling invalid data
    - Find relationships between data
