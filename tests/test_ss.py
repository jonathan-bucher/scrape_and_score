# testing statistical functions

import pytest

import pandas as pd
import numpy as np

from src.statistics import statistical_functions as sf

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

