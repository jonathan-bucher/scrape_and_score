# tests database initialization functions

import pandas as pd
import sqlite3
import os

import src.data.webscraping_functions as wf
import src.data.database_functions as db

testing_database = r"C:\Users\jonat\OneDrive\projects\scrape_and_score\tests\testing_db.db"
table = 'defense_stats'
os.remove(testing_database)

# testing add_defense function
db.add_defense(testing_database, table, 2022)

def test_add_defense_columns():

    # access the data
    conn = sqlite3.connect(testing_database)
    df = pd.read_sql_query("SELECT * FROM defense_stats", conn)

    num_cols = df.shape[1]

    assert num_cols == 6

    conn.close()


def test_add_defense_rows():

    # access the data
    conn = sqlite3.connect(testing_database)
    df = pd.read_sql_query("SELECT * FROM defense_stats", conn)

    num_rows = len(df)

    assert num_rows == 32

    conn.close()


def test_not_null():

    conn = sqlite3.connect(testing_database)
    df = pd.read_sql_query("SELECT * FROM defense_stats", conn)

    null_values = df.isnull().values.any()

    assert not null_values

    conn.close()


def test_unique_id():

    conn = sqlite3.connect(testing_database)
    df = pd.read_sql_query("SELECT * FROM defense_stats", conn)

    is_unique = df['defense_id'].is_unique 

    assert is_unique

    conn.close()

def test_rankings():

    conn = sqlite3.connect(testing_database)
    df = pd.read_sql_query("SELECT * FROM defense_stats", conn)

    ranks = []

    for i in range(32):

        ranks.append(df['rank'][i] == i + 1)

    assert ranks 
    
    conn.close()


def test_add_defense_replace():
    # rerun add_defense(2004)
    db.add_defense(testing_database, table, 2022)

    # access the data
    conn = sqlite3.connect(testing_database)
    df = pd.read_sql_query("SELECT * FROM defense_stats", conn)

    num_rows = len(df)

    assert num_rows == 32

    conn.close()

def test_add_defense_append():
    # add 2005 data
    db.add_defense(testing_database, table, 2023)

    # access the data
    conn = sqlite3.connect(testing_database)
    df = pd.read_sql_query("SELECT * FROM defense_stats", conn)

    num_rows = len(df)

    assert num_rows == 64

    conn.close()

weight_df = db.calculate_weights(testing_database, table)


def test_weights_len():

    db.calculate_weights(testing_database, table)

    conn = sqlite3.connect(testing_database)
    df = pd.read_sql_query('SELECT * FROM defense_stats', conn)

    assert len(df) == 64

    conn.close()


def test_weights_values():

    conn = sqlite3.connect(testing_database)
    df = pd.read_sql_query('SELECT * FROM defense_stats', conn)

    # Calculate the overall mean of 'pyds_allowed'
    overall_mean = df['pyds_allowed'].mean()
    
    # Filter for rank 1 defenses    
    r1df = df[df['rank'] == 1]
    r1_mean = r1df['pyds_allowed'].mean()

    # Calculate the expected weight
    expected_weight = overall_mean / r1_mean

    # Ensure all rank 1 weights match the expected weight
    assert (r1df['weight'] == expected_weight).all(), (
        f"Some weights for rank 1 defenses do not match the expected value: {expected_weight}"
    )

    conn.close()

def test_weights_values_all():

    conn = sqlite3.connect(testing_database)
    df = pd.read_sql_query('SELECT * FROM defense_stats', conn)

    ranked_avg = df.groupby('rank')['pyds_allowed'].mean()
    global_avg = df['pyds_allowed'].mean()
    weights = global_avg / ranked_avg
    df['test_weight'] = df['rank'].map(weights)

    assert (df['test_weight'] == df['weight']).all()

    conn.close()
    

folder = r"C:\Users\jonat\OneDrive\projects\scrape_and_score\data\raw\quarterbacks"
# 24 qb's in folder
gl_table = 'game_logs'
# testing the add_game_logs function
test_df = db.create_gamelogs(folder, testing_database, gl_table, table)

def test_gl_col():
    # proper number of columns
    num_cols = test_df.shape[1]
    assert num_cols == 11
    

def test_gl_na():
    null_values = test_df.isnull().values.any()
    assert not null_values


def test_gl_qb_id():
    unique_values = test_df['qb_id'].nunique()
    assert unique_values == 24


def test_qb_id():
    unique_values = test_df['defense_id'].nunique()
    assert unique_values == 31


def test_abbreviation():
    assert len(test_df['opponent'][0]) != 3
    assert len(test_df['team'][0]) != 3


def test_gl_names():
    unique_values = test_df['name'].nunique()
    assert unique_values == 24

def test_glrank():

    assert (0 < test_df['opp_rank']).all()
    assert (test_df['opp_rank'] < 33).all()

def test_glweight():

    assert (test_df['weight'] != 0).all()

# testing ranking and weighted yards metrics
print(test_df[:5])