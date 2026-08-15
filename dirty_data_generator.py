from numpy import random
from faker import Faker
import csv
from decimal import *

"""
Config vectors for dirty csv generation.
"""
MISSING_DATA_CONFIG = {"no_name" : 0.02, "no_province" : 0.05,
                        "no_age": 0.03, "no_money": 0.05,
                        "no_cie": 0.01}

MISSPELLED_DATA_CONFIG = {"misp_name"  : 0.01, "misp_province" : 0.015,
                            "misp_cie" : 0.02}

WRONG_DATA_CONFIG = {"wrong_name" : 0.01, "wrong_age" : 0.015, "wrong_money" : 0.03}

# A function that prints the probability vectors should be written.
# The user should be aware of what are the chances for each value to be dirty.


def roll_a_dice(probability : float) -> bool:
    """
    probability (float) --> Input probability, a float between 0 and 1.0.
    Generate a random float in range [0,1] and returns True
    if less than the input probability.
    """
    if probability > 1 or probability < 0:
        raise ValueError("Input must be a float value between 0 and 1.0")
    return (random.rand()<probability)


def misspell_string(mystring : str) -> str:
    """
    mystring (str) --> input string
    Returns the same string with each character randomly capitalized or lowered.
    """
    new_string = ""
    for x in mystring:
        k = random.rand()
        if k > 0.5:
            new_string+=str(x).upper()
        else:
            new_string+=str(x).lower()
    return new_string

def wrong_format_string(mystring : str, string_type : str) -> str:
    """
    Returns a string whose format is different from Faker library's one.
    """
    new_string = ""
    match string_type:
        case "name":
            temp = mystring.split(" ")
            for word in temp:
                 if random.rand() > 0.5:
                     new_string+=word[0]+". "
                 else:
                     new_string+=word+" "
        case "money":
            if random.rand() > 0.5:
                new_string = "$"+mystring
            else:
                new_string = mystring+"$"
        case _:
            raise ValueError(f"Bad format: {string_type}")
    return new_string
            

def generate_dirty_csv(number_of_rows : int, filename, faker_locale : str = None, include_duplicates:bool = False,
                       max_number_of_duplicates : int = 0):
    """
    Generate a CSV dataset with wrong, missing or misspelled data.
    Args: 
            number of rows (int) --> Number of unique records (no duplicates)
            filename (str) --> The target file path
            faker_locale (str) --> Faker library locale value. Default value: None (English)
            include_duplicates (bool) --> Adds a random number of duplicate rows along with the unique ones Default value: False
            max_number_of_duplicates (int) --> If include_duplicates is true, up to max_number_of_duplicates duplicated rows are added
    """
    if not str(filename).endswith(".csv"):
        raise ValueError("Invalid extension: must be a .csv file")
    
    elif(max_number_of_duplicates == 0 and include_duplicates == True):
        raise ValueError("Duplicates are enabled but number_of_duplicates is set to 0")

    elif(max_number_of_duplicates < 0):
        raise ValueError(f"Illegal value for number_of_duplicates = {max_number_of_duplicates}, must be a positive int")
    
    rows = []
    duplicate_cnt = max_number_of_duplicates

    fake = Faker(locale=faker_locale)
    field_list = ["name","age","province","cie","money"]

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_list)
        writer.writeheader()

        for row in range(number_of_rows):

            # Sample data
            name = fake.name()
            province = fake.state_abbr()
            age = random.randint(1,100)
            cie = fake.cie()
            money = Decimal(random.normal(1500, 700)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

            
            # Name
            if roll_a_dice(MISSING_DATA_CONFIG["no_name"]) :
                name = None
            elif roll_a_dice(MISSPELLED_DATA_CONFIG["misp_name"]) :
                name = misspell_string(name)
            elif roll_a_dice(WRONG_DATA_CONFIG["wrong_name"]) :
                name = wrong_format_string(name, "name")

            
            # province
            if roll_a_dice(MISSING_DATA_CONFIG["no_province"]) :
                province = None
            elif roll_a_dice(MISSPELLED_DATA_CONFIG["misp_province"]) :
                province = misspell_string(province)

        
            # Age
            if roll_a_dice(MISSING_DATA_CONFIG["no_age"]) :
                age = None
            elif roll_a_dice(WRONG_DATA_CONFIG["wrong_age"]):
                age = -age

            # Money
            if roll_a_dice(MISSING_DATA_CONFIG["no_money"]) :
                new_money = None
            elif roll_a_dice(WRONG_DATA_CONFIG["wrong_money"]):
                new_money = wrong_format_string(str(money), "money")
            else:
                new_money = money
            

            # CIE
            if roll_a_dice(MISSING_DATA_CONFIG["no_cie"]) :
                cie = None
            elif roll_a_dice(MISSPELLED_DATA_CONFIG["misp_cie"]) :
                cie = misspell_string(cie)

            temp_dict = {"name": "" if name is None else name,
                        "age" : "" if age is None else str(age),
                        "province" : "" if province is None else province,
                        "cie" : "" if cie is None else cie,
                        "money" : "" if new_money is None else str(new_money)}
            rows.append(temp_dict)

            #Duplicates
            if(include_duplicates):
                if(random.rand() > 0.85 and len(rows) != 0 and duplicate_cnt > 0):
                    duplicate_cnt = duplicate_cnt -1
                    index = random.randint(0, len(rows))
                    writer.writerow(rows[index])
            writer.writerow(temp_dict)
        