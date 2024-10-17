# testing column_transfroms (format)

import pytest
from src.data.column_transforms import format
import pandas as pd
import numpy as np

defense_2020 = pd.read_csv(r"C:\Users\jonat\OneDrive\projects\scrape_and_score\data\raw\defense\2020_nfl_defense_data.txt")
burrow_career = pd.read_csv(r"C:\Users\jonat\OneDrive\projects\scrape_and_score\data\raw\quarterbacks\joe_burrow_career.txt")

# format defense to apply tests
ftd_defense_2020 = format(defense_2020, position = 'DEF')

def test_ftd_defense_columns():

    # columns have been properly formatted
    assert list(ftd_defense_2020.columns) == ['Tm', 'PassYds', 'RushYds', 'Year']

def test_ftd_defense_row_count():

    # right number of rows
    assert len(ftd_defense_2020) == 32

def test_ftd_defense_null():

    # no null values
    null_values_exist = ftd_defense_2020.isnull().values.any()
    assert not null_values_exist

# format burrow data to apply tests
burrow_formatted = format(burrow_career.copy(), position = 'QB')

def test_ftd_qb_columns():

    # columns have been properly formatted
    assert list(burrow_formatted.columns) == ['Time', 'Year', 'Date', 'Week', 'Tm', 'Opp', 'Result', 'Home', 'Started',
                                    'Att', 'PassYds', 'PassTD', 
                                    'RushYds', 'RushTD']

def test_ftd_qb_null():

    # no null values
    null_values_exist = burrow_formatted.isnull().values.any()
    assert not null_values_exist