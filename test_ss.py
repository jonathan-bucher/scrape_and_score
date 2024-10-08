import pytest
import pandas as pd
import numpy as np
import random
import column_transforms as ct
import assign_rankings as ar

defense_2020 = pd.read_csv(r"C:\Users\jonat\Python\football_data\defense\2020_nfl_defense_data.txt")
burrow_career = pd.read_csv(r"C:\Users\jonat\Python\football_data\quarterbacks\joe_burrow_career.txt")


def test_defense_column_transformer():

    # columns have been properly formatted
    assert list(defense_2020.columns) == ['Tm', 'PassYds', 'RushYds', 'Year', 'def_rk']

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
    
    # no null values
    null_values_exist = burrow_formatted.isnull().values.any()
    assert not null_values_exist

def test_assign_rankings():

    # rankings are well formatted
    for ranking in range(1, 33):
        assert ranking in list(defense_2020['def_rk'])

    # teams are correctly ranked
    index_1, index_2 = (random.randint(1, 32), random.randint(1, 32))
    if defense_2020.loc[index_1, 'PassYds'] <= defense_2020.loc[index_2, 'PassYds']:
        assert defense_2020.loc[index_1, 'def_rk'] <= defense_2020.loc[index_2, 'def_rk']
    else:
        assert defense_2020.loc[index_1, 'def_rk'] >= defense_2020.loc[index_2, 'def_rk'] 

    # no null values
    null_values_exist = defense_2020.isnull().values.any()
    assert not null_values_exist


all_defense = pd.read_csv(r"C:\Users\jonat\Python\football_data\05_24_defense.txt")
burrow_ranked = ar.qb_def_rankings(all_defense, burrow_formatted.copy())

def test_qb_def_rankings():

    # no null values in the def_rk column aside from 2024
    null_values_exist = burrow_ranked.loc[burrow_ranked['Year'] < 2024].isnull().values.any()
    assert not null_values_exist

    # proper values
    proper_values = burrow_ranked.loc[burrow_ranked['Year'] < 2024]['def_rk'].map(lambda x: 0 < x < 33)
    assert False not in proper_values