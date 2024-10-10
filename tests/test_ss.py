import pytest

import pandas as pd
import numpy as np

import random

from src.data.column_transforms import format
from src.features import assign_rankings as ar
from src.statistics import statistical_functions as sf


defense_2020 = pd.read_csv(r"C:\Users\jonat\OneDrive\projects\scrape_and_score\data\raw\defense\2020_nfl_defense_data.txt")
burrow_career = pd.read_csv(r"C:\Users\jonat\OneDrive\projects\scrape_and_score\data\raw\quarterbacks\joe_burrow_career.txt")

# format defense to apply tests
ftd_defense_2020 = format(defense_2020, position = 'DEF')

def test_defense_column_transformer():

    # columns have been properly formatted
    assert list(ftd_defense_2020.columns) == ['Tm', 'PassYds', 'RushYds', 'Year', 'def_rk']

    # right number of rows
    assert len(ftd_defense_2020) == 32

    # no null values
    null_values_exist = ftd_defense_2020.isnull().values.any()
    assert not null_values_exist

# format burrow data to apply tests
burrow_formatted = format(burrow_career.copy(), position = 'QB')

def test_qb_column_transform():

    # columns have been properly formatted
    assert list(burrow_formatted.columns) == ['Time', 'Year', 'Date', 'Week', 'Tm', 'Opp', 'Result', 'Home', 'Started',
                                    'Att', 'PassYds', 'PassTD', 
                                    'RushYds', 'RushTD']
    
    # no null values
    null_values_exist = burrow_formatted.isnull().values.any()
    assert not null_values_exist


# rank formatted defense data to apply tests
rkd_defense_2020 = ar.assign_rankings(ftd_defense_2020, 'PassYds')

def test_assign_rankings():

    # rankings are well formatted
    for ranking in range(1, 33):
        assert ranking in list(rkd_defense_2020['def_rk'])

    # teams are correctly ranked
    index_1, index_2 = (random.randint(1, 32), random.randint(1, 32))
    if rkd_defense_2020.loc[index_1, 'PassYds'] <= rkd_defense_2020.loc[index_2, 'PassYds']:
        assert rkd_defense_2020.loc[index_1, 'def_rk'] <= rkd_defense_2020.loc[index_2, 'def_rk']
    else:
        assert rkd_defense_2020.loc[index_1, 'def_rk'] >= rkd_defense_2020.loc[index_2, 'def_rk'] 

    # no null values
    null_values_exist = rkd_defense_2020.isnull().values.any()
    assert not null_values_exist


all_defense = pd.read_csv(r"C:\Users\jonat\OneDrive\projects\scrape_and_score\data\processed\05_24_defense.txt")
burrow_ranked = ar.qb_def_rankings(all_defense, burrow_formatted.copy())

def test_qb_def_rankings():

    # no null values in the def_rk column aside from 2024
    null_values_exist = burrow_ranked.loc[burrow_ranked['Year'] < 2024].isnull().values.any()
    assert not null_values_exist

    # proper values
    proper_values = burrow_ranked.loc[burrow_ranked['Year'] < 2024]['def_rk'].map(lambda x: 0 < x < 33)
    assert False not in proper_values


# testing statistical functions

test_data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'Age': [24, 27, 0, 22, 30]
}

test_df = pd.DataFrame(test_data)

test_data_2 = {
    'City': ['Seattle', 'Las Vegas', 'New York'],
    'Rain': [0.5, 0.1, 0.3]
}

test_df_2 = pd.DataFrame(test_data_2)

# fake runningback stats
test_data_3 = {
    'yards': [100, 180, 75, 200],
    'd_rank': [2, 3, 1, 4],
}

test_df_3 = pd.DataFrame(test_data_3)

def test_probability():
    assert sf.probability(test_df, ('Name', 'eq', 'David')) == 0.20
    assert sf.probability(test_df, ('Name', 'eq', 'David')) != 0.10
    assert sf.probability(test_df, ('Age', 'geq', 22)) == 0.8

def test_condition_indices():
    assert len(sf.condition_indices(test_df, ('Name', 'eq', 'David'))) == 1
    assert len(sf.condition_indices(test_df, ('Age', 'geq', 22))) == 4

def test_joint_probability():
    assert sf.joint_probability(test_df, [('Name', 'eq', 'David'), ('Age', 'leq', 25)]) == 0.2
    assert sf.joint_probability(test_df, [('Name', 'eq', 'Bob'), ('Age', 'l', 25)]) == 0

def test_conditional_probability():
    # given that your age is less than or equal to 25, what is the chance your name is David?
    assert sf.conditional_probability(test_df, [('Name', 'eq', 'David'), ('Age', 'leq', 25)]) == (1 / 3)

def test_bayes():
    # a runningback plays the first game of the season, and rushes for 170 yards
    # what are the odds, based on historical data, that this team is the worst in a four team league
    assert sf.bayes(test_df_3, [('d_rank', 'eq', 4), ('yards', 'geq', 170)]) == 0.5 

