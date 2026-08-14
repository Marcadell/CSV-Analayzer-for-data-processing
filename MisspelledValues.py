# This file groups the regex a field value must match to be valid.
# See <re> library documentation to learn more.
# Note: this project is small with two or three fields to check. 
# A possible upgrade in terms of scalability can be made introducing more regex grammar constants...
import pandas as pd
import re

# Fields that need to be checked for misspelling
FIELDS_UNDER_TEST = ["name", "provincia", "cie", "age"]

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


valid_province_codes = [
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
        "OG",
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


def check_misspelled_fields(row : pd.Series) -> dict:
        """
        Checks for any misspelled values in the following fields: name, provincia, cie.
        Returns a dict whose keys are the same as fields and whose values 
        indicate whether or not the value in that field is misspelled.
        Missing values (pandas NaN) are considered to be spelled correctly. This is not the case
        for empty strings like "".
        """
        
        misspelledFields = dict.fromkeys(FIELDS_UNDER_TEST, False)
        misspelledFields["isMisspelled"] = False
        
        if (not pd.isna(row["name"])) and (not re.fullmatch(VALID_NAME, row["name"])):
                misspelledFields["name"] = True
                print(re.match(VALID_NAME, row["name"]))

        if (not pd.isna(row["provincia"])) and (row["provincia"] not in valid_province_codes):
                misspelledFields["provincia"] = True

        if (not pd.isna(row["cie"])) and (not re.fullmatch(VALID_CIE, row["cie"])):
                misspelledFields["cie"] = True

        misspelledFields["isMisspelled"] = any(misspelledFields.values())

        return misspelledFields
def list_misspelled_rows(df : pd.DataFrame) -> list[dict]:
        """
        Check fo any misspelled values in the followind fields: name, provincia, cie.
        Returns a list of dicts. Each dict
        """
        row_list = []

        for i, row in df.iterrows():
                temp = check_misspelled_fields(row)
                print(f"Row:{row}\t fieldStatus:{temp}")
                if temp["isMisspelled"]:
                    row_list.append(temp)

        return row_list