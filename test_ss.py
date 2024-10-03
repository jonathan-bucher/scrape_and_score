import pytest
import pandas as pd
import numpy as np
import random
import column_transforms as ct
import assign_rankings as ar

# data

defense_2020 = pd.read_csv(r"C:\Users\jonat\Python\football_data\defense\2020_nfl_defense_data.txt")

# test for no null values in the individual player data

# we are writing a script that will go through our central defensive dataframe, and assign a ranking by year based on passing yards
# we will then assign a rank to the defense played by quarterbacks each week. 
    # this can either be done individually, before they are compiled, or in a central dataframe
# and then we're done

# ensure that each defense is represented 

defense_2020 = ct.defense_column_transform(defense_2020.copy(), 2020)

def test_defense_column_transformer():
    assert list(defense_2020.columns) == ['Tm', 'PassYds', 'RushYds', 'Year']
    # check there is the right number of rows
    assert len(defense_2020) == 32

# def test_assign_rankings():
    # assert 