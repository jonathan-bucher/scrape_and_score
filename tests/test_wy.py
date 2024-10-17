# testing the feature engineering script weighted_yards.py

import pytest
import pandas as pd

from src.features.weighted_yards import *

# data
all_defense = pd.read_csv(r"C:\Users\jonat\OneDrive\projects\scrape_and_score\data\processed\all_defense.txt")

def test_rank():
    # ensure all defenses have been ranked

    for rank in range(1, 33):
        assert rank in rank_weights.keys()

def test_values():
    # values make sense

    for rank, yards in rank_weights.items():
        if type(rank) != str and rank != 32:
            assert yards < rank_weights[rank + 1]

def test_overall_avg():
    # overall average is the true average

    assert rank_weights['overall_average'] == all_defense['PassYds'].mean()


    
