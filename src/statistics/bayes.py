# model to predict whether or not a quarterbacks line is overfit to recent data

import pandas as pd
import numpy as np
from collections import deque
import src.statistics.statistical_functions as sf

import logging

# active 2024 quarterbacks with strength of defense adjusted passing yards metrics

all_qb_weighted = pd.read_csv(r"C:\Users\jonat\OneDrive\projects\scrape_and_score\data\processed\all_quarterbacks_weighted.txt")



def over_under(df, qb: str, line: float, games: int, avg_yards: float) -> list:
    """
    Determines whether a quarterbacks passing yards projection is overfit to recent data
    
    Args: 
        df (Pandas DataFrame): dataframe with game logs of quarterbacks concatenated together
        qb (str): name of the quarterback
        line (float): passing yards projection
        games (int): number of games played in most recent season
        avg_yards (float) average yards over that interval of games

    Returns:
    """

    # create new dataframe with the n_game_averages column
    df = last_n_avg(df, games, 'weighted_yards', f'{games}_game_avg', 'name')

    # create a dictionary for holding the odds that a player will hit the weighted yards value over the course of their career
    categories = {}

    for player in df['name'].unique():

        # if the probability of the qb hitting the line is over fifty, they are categorized as 'over
        prob = sf.conditional_probability(df, [('weighted_yards', 'geq', line), ('name', 'eq', player)])                                
        if prob > 0.5:
            categories[player] = 'over'

        else:
            categories[player] = 'under'

        # store pobability qb of interest hits line
        if player == qb:
            qb_hits_line = prob

    # map players to their category in a category column
    df['category'] = df['name'].map(categories)

    if prob < 50:

        return proj_under(df, categories, qb, line, games, avg_yards, qb_hits_line)

    else:

        return proj_over(df, categories, qb, line, games, avg_yards, qb_hits_line)
    




def last_n_avg(df, n: int, column_1: str, column_2: str, on_column: str):
    """
    creates a new column in a dataframe with the average value of the last n rows, where the value of a second column in the dataframe is unchanged

    Args:
        df (Pandas Dataframe): dataframe with quarterback game logs
        n (int): number of games for which the average will be calculated
        column_1 (str): column for which averages will be calculated
        column_2 (str): column where averages will be stored
        on_column (str): column where change in value results in new average calculation

    Returns:
        New Pandas dataframe with 'last_n_avg' column
    """

    # initialize a queue to calculate averages
    queue = deque()

    # store first on_column value
    on_column_val = df.loc[0, on_column]

    # create a new column to store the average of the last n values
    df[column_2] = np.nan

    for index, row in df.iterrows():

        # check if on_column value has changed
        if on_column_val != row[on_column]:

            # remove all values from queue
            queue = deque()

        # append value from column where averages are calculated
        queue.append(row[column_1])

        # ensure there is the proper number of elements
        if len(queue) == n:
            
            # calculate the average
            average = sum(queue) / n

            df.loc[index, column_2] = average

            # remove the first element
            queue.popleft()

        # update 'on_column'
        on_column_val = row[on_column] 

    return df 



def proj_under(df, categories: dict, qb: str, line: float, games: int, avg_yards: float, qb_hits_line: float):
    """
    Calculates the probability a quarterback will hit the over on their line given 
    that they are projected to hit the under based on historical data

    Args: 
        df (Pandas DataFrame): a dataframe with a category over or under column

    Returns:
        a list with two elements
            - first element is Pandas DataFrame with category column
            - second element is the probability that the quarterback hits their line  
    """

    # calculate probability quarterback projected to hit the over hits the given string of games
    hit_avg_gvn_ovr = sf.conditional_probability(df, [(f'{games}_game_avg', 'geq', avg_yards), ('category', 'eq', 'over')], null = True)

    # calculate odds a quarterback is category over
    overs = sum(1 for value in categories.values() if value == 'over')
    cat_over = overs / len(categories)

    # odds a quarterback hits the over given they are category over
    hit_ovr_gvn_ovr = sf.conditional_probability(df, [('weighted_yards', 'geq', line), ('category', 'eq', 'over')], null = True)

    # odds of any player hitting n game avg 
    hit_avg = sf.probability(df, (f'{games}_game_avg', 'geq', avg_yards), null = True)

    # Bayesian analysis (odds of that line given category 1 (log this), times odds of category 1 (log this), 
        # over total odds of hitting that avg over that game span (log this) = odds of category 1 given that run) 
    if hit_avg == 0:
        qb_is_cat_over = float("inf")

    else:
        qb_is_cat_over = (hit_avg_gvn_ovr * cat_over) / (hit_avg)

    # return the expected probability
    expected_probability = qb_is_cat_over * (hit_ovr_gvn_ovr) + (1 - qb_is_cat_over) * (qb_hits_line)

    # log results

    logging_probabilities(df, categories, qb, games, avg_yards, qb_hits_line, cat_over,
                        qb_is_cat_over, expected_probability)

    return [df, expected_probability]



def proj_over(df, categories: dict, qb: str, line: float, games: int, avg_yards: float, qb_hits_line: float):
    """
    Calculates probability a quarterback will hit the over on their line given 
    that they are projected to hit the over based on historical data
    """

    # calculate probability quarterback projected to hit under misses the given string of games
    miss_avg_gvn_under = sf.conditional_probability(df, [(f'{games}_game_avg', 'leq', avg_yards), ('category', 'eq', 'over')], null = True)

    # odds of a player being category under
    unders = sum(1 for value in categories.values() if value == 'under')
    cat_under = unders / len(categories)

    # odds of a player being category over
    cat_over = 1 - cat_under

    # odds a player misses line given they are category under
    miss_ovr_gvn_undr = sf.conditional_probability(df, [('weighted_yards', 'leq', line), ('category', 'eq', 'under')], null = True)

    # odds of any player missing the n-game average 
    miss_avg = sf.probability(df, (f'{games}_game_avg', 'geq', avg_yards), null = True)

    # Bayesian analysis (odds of missing that average given category under, times odds of category under, 
        # over total odds of missing that average = probability qb misses line given that string of games

    if miss_avg == 0:
        qb_is_cat_under = float("inf")

    else:
        qb_is_cat_under = (miss_avg_gvn_under * cat_under) / (miss_avg)

    # return the complement of the expected probability qb misses line
    expected_probability = (qb_is_cat_under) * (miss_ovr_gvn_undr) + (1 - qb_is_cat_under) * (1 - qb_hits_line)

    logging_probabilities(df, categories, qb, games, avg_yards, qb_hits_line, (1 - cat_over), (1 - qb_is_cat_under), expected_probability)

    return [df, 1 - expected_probability]




def logging_probabilities(df, categories: dict, qb: str, games: int, avg_yards,
                            qb_hits_line: float, cat_over: float, 
                            qb_is_cat_over: float, expected_probability: float):
    """
    calculates and returns all the probabilities needed for over_under functions
    """

    # create a dataframe to return with all relevant values
    logging_df = pd.DataFrame({'model': ['bayes'], 
                            'name': [f'{qb}'], 
                            'games': [games], 
                            'avg': [avg_yards],
                            f'hist over (qb)': [qb_hits_line], 
                            'hist over (all)' : [cat_over], 
                            f'bayes over': [qb_is_cat_over],
                            f'odds hits over': [expected_probability]})
    
    # log the model results
    logging_df.to_csv(r"C:\Users\jonat\OneDrive\projects\scrape_and_score\logging\models\bayes.log")
    df.to_csv(r"C:\Users\jonat\OneDrive\projects\scrape_and_score\logging\models\df.log")
    pd.Series(categories).to_csv(r"C:\Users\jonat\OneDrive\projects\scrape_and_score\logging\models\categories.log")
