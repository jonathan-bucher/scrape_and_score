import pytest
import pandas as pd
import numpy as np
import random
import column_transforms as ct
import assign_rankings as ar

# data

defense_2020 = pd.read_csv(r"C:\Users\jonat\Python\football_data\defense\2020_nfl_defense_data.txt")
burrow_career = pd.read_csv(r"C:\Users\jonat\Python\football_data\quarterbacks\joe_burrow_career.txt")

# test for no null values in the individual player data

# we are writing a script that will go through our central defensive dataframe, and assign a ranking by year based on passing yards
# we will then assign a rank to the defense played by quarterbacks each week. 
    # this can either be done individually, before they are compiled, or in a central dataframe
# and then we're done

defense_2020 = ct.defense_column_transform(defense_2020.copy(), 2020)

def test_defense_column_transformer():

    # columns have been properly formatted
    assert list(defense_2020.columns) == ['Tm', 'PassYds', 'RushYds', 'Year']

    # right number of rows
    assert len(defense_2020) == 32

    # no null values
    null_values_exist = defense_2020.isnull().values.any()
    assert not null_values_exist

burrow_formatted = ct.qb_column_transform(burrow_career.copy())

def test_qb_column_transform():

    # columns have been properly formatted
    assert list(burrow_formatted.columns) == ['Time', 'Year', 'Date', 'Week', 'Tm', 'Opp', 'Result', 'Home', 'Started',
                                    'Att', 'PassYds', 'PassTD', 
                                    'RushYds', 'RushTD']

ranked_defense_2020 = ar.assign_rankings(defense_2020.copy(), 'PassYds')

def test_assign_rankings():

    # rankings are well formatted
    for ranking in range(1, 33):
        assert ranking in list(ranked_defense_2020['def_rk'])

    # teams are correctly ranked
    index_1, index_2 = (random.randint(1, 32), random.randint(1, 32))
    if ranked_defense_2020.loc[index_1, 'PassYds'] <= ranked_defense_2020.loc[index_2, 'PassYds']:
        assert ranked_defense_2020.loc[index_1, 'def_rk'] <= ranked_defense_2020.loc[index_2, 'def_rk']
    else:
        assert ranked_defense_2020.loc[index_1, 'def_rk'] >= ranked_defense_2020.loc[index_2, 'def_rk'] 

    # no null values
    null_values_exist = ranked_defense_2020.isnull().values.any()
    assert not null_values_exist

# def test prf_webscraper()

# burrow_ranked = ar.qb_def_rankings(defense_2020, burrow_formatted.copy())

# def test_qb_def_rankings():

    # no null values in the def_rk column if the year is 2020

    # null_values_exist = ranked_defense_2020.isnull().values.any()
    # assert not null_values_exist