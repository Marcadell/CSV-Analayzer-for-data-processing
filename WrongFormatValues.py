# This file groups the regex a field value must match to be valid.
# See <re> library documentation to learn more.
# Note: this project is small with two or three fields to check. 
# A possible upgrade in terms of scalability can be made introducing more regex grammar constants...
import pandas as pd
import re

# Fields that need to be checked for misspelling
FIELDS_UNDER_TEST = ["name", "age", "province", "cie", "money"]

# Regex grammar constants for readability
WORD_2_14 = "[A-Z][a-z]{2,14}"
WORD_0_14 = "[A-Z][a-z]{0,14}" #For compound surnames

VALID_NAME = WORD_2_14+r"(?:\s"+WORD_0_14+r"['\-]"+WORD_2_14+r"|\s"+WORD_2_14+r"){1,2}"
VALID_NAME_DESCRIPTION = "#The first letter of a name is uppercase, the others are lowercase.\
 #A name must be at least 3 and at most 15 characters long.\
 #It can be followed by at least one and at most two surnames.\
 #Each surname must be at least 2 and at most 15 characters long.\
 #Compound surnames may contain an apostrophe or hyphen.\
 #Surnames like Giolitti-Pizzigoni, 'Ohara, O'Hara and Oo'Hara are all valid compound surnames.\
 #A compound surname is treated as a single surname.\
 #Each surname is preceded by exactly one whitespace."

VALID_CIE = r"[A-Z]{2,2}[\d]{5,5}[A-Z]{2,2}"
VALID_CIE_DESCRIPTION = "#A valid CIE (Carta d'Identità Elettronica) starts with 2 uppercase letters, /" \
"is followed by 5 numbers and ends 2 uppercase letters"

VALID_MONEY = r"\d+(?:\.\d+)?"
VALID_MONEY_DESCRIPTION = "#A valid money value has only numbers and optionally a dot to separate decimal digits. Negative money values are not allowed"

VALID_PROVINCE_CODES = [
        "AG",
        "AL",
        "AN",
        "AO",
        "AR",
        "AP",
        "AT",
        "AV",
        "BA",
        "BT",
        "BL",
        "BN",
        "BG",
        "BI",
        "BO",
        "BZ",
        "BS",
        "BR",
        "CA",
        "CL",
        "CB",
        "CE",
        "CT",
        "CZ",
        "CH",
        "CO",
        "CS",
        "CR",
        "KR",
        "CN",
        "EN",
        "FM",
        "FE",
        "FI",
        "FG",
        "FC",
        "FR",
        "OT",
        "GE",
        "GO",
        "GR",
        "IM",
        "IS",
        "SP",
        "AQ",
        "LT",
        "LE",
        "LC",
        "LI",
        "LO",
        "LU",
        "MC",
        "MN",
        "MS",
        "MT",
        "ME",
        "MI",
        "MO",
        "MB",
        "NA",
        "NO",
        "NU",
        "OG",
        "OR",
        "PD",
        "PA",
        "PR",
        "PV",
        "PG",
        "PU",
        "PE",
        "PC",
        "PI",
        "PT",
        "PN",
        "PZ",
        "PO",
        "RG",
        "RA",
        "RC",
        "RE",
        "RI",
        "RN",
        "RM",
        "RO",
        "SA",
        "VS",
        "SS",
        "SV",
        "SI",
        "SR",
        "SO",
        "TA",
        "TE",
        "TR",
        "TO",
        "TP",
        "TN",
        "TV",
        "TS",
        "UD",
        "VA",
        "VE",
        "VB",
        "VC",
        "VR",
        "VV",
        "VI",
        "VT",
]

def valid_age(age) -> bool:
       if not (age % 1 == 0):
              return False 
       elif age < 0:
              return False
       elif age > 122: #Oldest person in history
              return False
       else:
              return True

def check_wrongFormat_fields(row : pd.Series) -> dict:
        """
        Checks for any wrong format values in the following fields: name, province, cie.
        Returns a dict whose keys are the same as fields and whose values 
        indicate whether or not the value in that field has wrong format.
        Missing values (pandas NaN) are considered to be spelled correctly. This is not the case
        for empty strings like "".
        """
        
        wrongFormatFields = dict.fromkeys(FIELDS_UNDER_TEST, False)
        wrongFormatFields["iswrongFormat"] = False
        
        if (not pd.isna(row["name"])) and (not re.fullmatch(VALID_NAME, row["name"])):
                wrongFormatFields["name"] = True
               
        if (not pd.isna(row["age"])) and not valid_age(row["age"]):
               wrongFormatFields["age"] = True
        
        if (not pd.isna(row["province"])) and (row["province"] not in VALID_PROVINCE_CODES):
                wrongFormatFields["province"] = True

        if (not pd.isna(row["cie"])) and (not re.fullmatch(VALID_CIE, row["cie"])):
                wrongFormatFields["cie"] = True

        if (not pd.isna(row["money"])) and (not re.fullmatch(VALID_MONEY, row["money"])):
               wrongFormatFields["money"] = True

        wrongFormatFields["iswrongFormat"] = any(wrongFormatFields.values())

        return wrongFormatFields

def list_wrongFormat_rows(df : pd.DataFrame) -> list[dict]:
        """
        Check for any wrong format values in the followind fields: name, province, cie.
        Returns a list of dicts. Each dict
        """
        row_list = []

        for i, row in df.iterrows():
                temp = check_wrongFormat_fields(row)
                if temp["iswrongFormat"]:
                    row_list.append(temp)

        return row_list

def drop_wrongFormat_rows(df : pd.DataFrame, fields : list):
        """
        Returns a copy of the input dataFrame without the rows with wrong format values, 
        which can be specified in <fields>.
        """
        for field in fields:
              if(field not in FIELDS_UNDER_TEST):
                     raise ValueError(f"{field} is not a valid field")

        df2 = df.copy()
       
        for i, row in df.iterrows():
              if "name" in fields and not re.fullmatch(VALID_NAME, row["name"]):
                     df2.drop(index = i, inplace = True)
              elif "money" in fields and not re.fullmatch(VALID_MONEY, str(row["money"])):
                     df2.drop(index = i, inplace = True)
              elif "province" in fields and row["province"] not in VALID_PROVINCE_CODES:
                     df2.drop(index = i, inplace = True)
              elif "age" in fields and not valid_age(row["age"]): # Since a valid "age" would be a positive integer
                                                                  # these are not fields with an incorrect format but rather wrong data.
                     df2.drop(index = i, inplace = True) 
              elif "cie" in fields and not re.fullmatch(VALID_CIE, row["cie"]):
                     df2.drop(index = i, inplace=True)

        return df2