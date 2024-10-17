# testing the assign_rankings script

import pytest

import pandas as pd
import numpy as np

import random

from src.data.column_transforms import format
from src.features import assign_rankings as ar

# data 
defense_2020 = pd.read_csv(r"C:\Users\jonat\OneDrive\projects\scrape_and_score\data\raw\defense\2020_nfl_defense_data.txt")
burrow_career = pd.read_csv(r"C:\Users\jonat\OneDrive\projects\scrape_and_score\data\raw\quarterbacks\joe_burrow_career.txt")

# format defense to apply tests
ftd_defense_2020 = format(defense_2020, position = 'DEF')

# rank formatted defense data to apply tests
rkd_defense_2020 = ar.assign_rankings(ftd_defense_2020, 'PassYds')

def test_full_rankings():

    # rankings are well formatted
    for ranking in range(1, 33):
        assert ranking in list(rkd_defense_2020['def_rk'])

def test_correct_rankings():

    # teams are correctly ranked
    index_1, index_2 = (random.randint(1, 32), random.randint(1, 32))
    if rkd_defense_2020.loc[index_1, 'PassYds'] <= rkd_defense_2020.loc[index_2, 'PassYds']:
        assert rkd_defense_2020.loc[index_1, 'def_rk'] <= rkd_defense_2020.loc[index_2, 'def_rk']
    else:
        assert rkd_defense_2020.loc[index_1, 'def_rk'] >= rkd_defense_2020.loc[index_2, 'def_rk'] 

def test_assign_rankings_null():

    # no null values
    null_values_exist = rkd_defense_2020.isnull().values.any()
    assert not null_values_exist

# format burrow data to apply tests
burrow_formatted = format(burrow_career.copy(), position = 'QB')

all_defense = pd.read_csv(r"C:\Users\jonat\OneDrive\projects\scrape_and_score\data\processed\05_24_defense.txt")
burrow_ranked = ar.qb_def_rankings(all_defense, burrow_formatted.copy())

def test_qb_def_rankings_null():

    # no null values in the def_rk column aside from 2024
    null_values_exist = burrow_ranked.loc[burrow_ranked['Year'] < 2024].isnull().values.any()
    assert not null_values_exist

def test_qb_def_rankings_values():

    # proper values
    proper_values = burrow_ranked.loc[burrow_ranked['Year'] < 2024]['def_rk'].map(lambda x: 0 < x < 33)
    assert False not in proper_values