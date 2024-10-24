# test bayes

from src.statistics.bayes import *
import pandas as pd
import numpy as np

# data
all_qb_weighted_1 = pd.read_csv(r"C:\Users\jonat\OneDrive\projects\scrape_and_score\data\processed\all_quarterbacks_weighted.txt")
all_qb_weighted = last_n_avg(all_qb_weighted_1, 6, 'weighted_yards', '6_game_avg', 'name')


# testing n_games function

def test_dim():
    # dataframe is proper dimensions
    assert len(all_qb_weighted_1) == len(all_qb_weighted)

def test_col():
    # column has been added
    assert '6_game_avg' in all_qb_weighted.columns

def test_values():
    # test the average value of the weighted yards column at various indices of the dataframe

    test_df_1 = all_qb_weighted_1.iloc[67:73]
    if test_df_1['name'].nunique() == 1:
        assert all_qb_weighted.loc[72, '6_game_avg'] == test_df_1['weighted_yards'].mean()
    else:
        assert all_qb_weighted.loc['6_game_avg'][67:73].isna().sum() >= 1

def test_first_null():
    # ensure that there are only null values in the first n - 1 entries of the dataframe
    assert all_qb_weighted['6_game_avg'][:6].isna().sum() == 5

def test_highest():
    # if n != 1, no value in the averages column will be higher then the highest value
    highest = all_qb_weighted['weighted_yards'].max()
    test_column_1 = all_qb_weighted['6_game_avg'] <= highest
    assert False not in test_column_1

def test_lowest():
    # if n != 1, no value in the averages column will be lower then the lowest value
    lowest = all_qb_weighted['weighted_yards'].min()
    test_column_2 = all_qb_weighted['6_game_avg'] >= lowest
    assert False not in test_column_2

def test_handled_next_qb():
    # function properly handled new quarterbacks
    qb = all_qb_weighted.loc[0, 'name']
    for index, row in all_qb_weighted.iterrows():
        next_qb = all_qb_weighted.loc[index, 'name']
        if next_qb != qb:
            assert np.isnan(all_qb_weighted.loc[index, '6_game_avg'])
        qb = all_qb_weighted.loc[index, 'name']


# testing the bayes model
test_df2 = over_under(all_qb_weighted_1, 'geno smith', 267.5, 6, 301)[0]

def test_category_col_null():
    assert test_df2['category'].notnull().all()

def test_category_col_values():
    assert 1 in test_df2['category'] 
    