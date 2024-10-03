# the probability of a quarterback hitting their projected passing yards in a given week is found by comparing 
# the defense they are facing with similar defenses they have played in the past. This critical step necessitates
# appending a def_rank column to dataframes with quarterback weekly gamelogs

import numpy as np
import pandas as pd
import random

team_abbreviation_dict = {
    'Arizona Cardinals': 'ARI',
    'Atlanta Falcons': 'ATL',
    'Baltimore Ravens': 'BAL',
    'Buffalo Bills': 'BUF',
    'Carolina Panthers': 'CAR',
    'Chicago Bears': 'CHI',
    'Cincinnati Bengals': 'CIN',
    'Cleveland Browns': 'CLE',
    'Dallas Cowboys': 'DAL',
    'Denver Broncos': 'DEN',
    'Detroit Lions': 'DET',
    'Green Bay Packers': 'GNB',  
    'Houston Texans': 'HOU',
    'Indianapolis Colts': 'IND',
    'Jacksonville Jaguars': 'JAX',
    'Kansas City Chiefs': 'KAN',  
    'Las Vegas Raiders': 'LVR',
    'Los Angeles Chargers': 'LAC',
    'Los Angeles Rams': 'LAR',
    'Miami Dolphins': 'MIA',
    'Minnesota Vikings': 'MIN',
    'New England Patriots': 'NWE',
    'New Orleans Saints': 'NOR',
    'New York Giants': 'NYG',
    'New York Jets': 'NYJ',
    'Philadelphia Eagles': 'PHI',
    'Pittsburgh Steelers': 'PIT',
    'San Francisco 49ers': 'SFO',
    'Seattle Seahawks': 'SEA',
    'Tampa Bay Buccaneers': 'TAM',
    'Tennessee Titans': 'TEN',
    'Washington Commanders': 'WAS',
    'Washington Redskins': 'WAS'
}


def quick_sort(nums: list) -> list:
    """
    sorts a list of numeric values into ascending order
    """
    if len(nums) <= 1:
        return nums
    pivot_index = random.randint(0, len(nums) - 1)
    pivot = nums[pivot_index]
    left = [x for x in nums if x < pivot]
    middle = [x for x in nums if x == pivot]
    right = [x for x in nums if x > pivot]   
    return quick_sort(left) + middle + quick_sort(right)


def assign_rankings(df, col: str) -> list:
    """
    takes a dataframe, and appends a row with rankings for a specific column
    """
    ordered = quick_sort(list(df[col]))

    for index, row in df.iterrows():
        df.loc[index, 'def_rk'] = ordered.index(row[col]) + 1
    
    return df

def qb_def_pass_rankings(defense_df, player_df):
    """
    takes a pfr dataframe of quarterback weekly stats, and will append a value for the quality of the passing defense played that week
    """
    
    # Map the team abbreviations to the full team names in defense_2023 DataFrame
    defense_df['Opp'] = defense_df['Tm'].map(team_abbreviation_dict)

    # Merge player_df with defense_df on both Year and Opponent columns
    player_df = player_df.merge(
    defense_df[['Year', 'Opp', 'def_rk']],  # Select only the relevant columns
    how='left',  # Keep all rows from player_df, fill missing ranks with NaN
    left_on=['Year', 'Opp'],  # Columns to merge on from player_df
    right_on=['Year', 'Opp']  # Columns to merge on from defense_df
    )

    return player_df

