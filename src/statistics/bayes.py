# function that takes as arguments a quarterback, a line, n games, average weighted yards over that span
# delivers if QB is category 1 or category 2, 
# probability that are category 2 given they are category 1 and vice versa
# eventually, probability of hitting the line (run regression on the numbers given above)
# data visualization

import pandas as pd
import numpy as np
from collections import deque
import src.statistics.statistical_functions as sf

import logging

# Configure the logging settings
logging.basicConfig(
    filename = "C:\Users\jonat\OneDrive\projects\scrape_and_score\logging\bayes_model.log", 
    level = logging.info,  
    format = '%(asctime)s - %(levelname)s - %(message)s',  
    datefmt = '%Y-%m-%d %H:%M:%S'  
)

# active 2024 quarterbacks with strength of defense adjusted passing yards metrics

all_qb_weighted = pd.read_csv(r"C:\Users\jonat\OneDrive\projects\scrape_and_score\data\processed\all_quarterbacks_weighted.txt")


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



def over_under(df, qb: str, line: float, games: int, avg_yards: float) -> list:
    """
    Determines whether a quarterbacks passing yards projection is overfit to recent data
    
    Args: 
        qb (str): name of the quarterback
        line (float): passing yards projection
        games (int): number of games played in most recent season
        avg_yards (float) average yards over that interval of games

    Returns:

    """

    # create new dataframe with the n_game_averages column
    df = last_n_avg(df, games, 'weighted_yards', f'{games}_game_avg', 'name')

    # we may need another function to go in and calculate the odds of each player hitting the specific n_game_avg
        # this can be done quickly with conditional probabilities? 
    # split these quarterbacks into category 1 and category 2 (append a column with 0's and 1's)


    # create a dictionary for holding the odds that a player will hit the weighted yards value over the course of their career
    categories = {}

    for player in df['name'].unique():

        # if the probability of the qb hitting the line is over fifty, they are category one
        if sf.probability(df, ('weighted_yards', 'geq', line)) > 50:
            categories[player] = 1

            cat_1 += 1
        
        else:
            categories[player] = 0

        # store pobability player hits the line for logging purposes
        if player == qb:
            qb_hits_line = sf.probability(df, ('weighted_yards', 'geq', line))

    # map players to their category in a category column
    df['category'] = df['name'].map(categories)

    # drop null values (where the quarterbacks are at the start of their career) and calculate conditional prob of category 1 hitting avg
    hit_avg_gvn_1 = sf.conditional_probability(df, [(f'{games}_game_avg', 'geq', avg_yards), ('category', 'eq', 1)], null = True)

    # calculate odds a qb is category 1
    ones = sum(1 for value in categories.values() if value == 1)
    cat_1 = ones / len(categories.values)

    # odds of any player hitting n game avg 
    hit_avg = sf.probability(df, (f'{games}_game_avg', 'geq', avg_yards))

    # Bayesian analysis (odds of that line given category 1 (log this), times odds of category 1 (log this), 
        # over total odds of hitting that avg over that game span (log this) = odds of category 1 given that run) 

    qb_is_cat_1 = (hit_avg_gvn_1 * cat_1) / (hit_avg)

    # create a dataframe to return with all relevant values
    logging_df = pd.Series({'model': 'bayes', 'games': {games}, 'avg': {avg_yards},
                            'qb_hits_line': qb_hits_line, 'hit_avg_gvn_1': hit_avg_gvn_1, 'prob_cat_1': 
                            cat_1, 'qb_is_cat_1': qb_is_cat_1})
    
    logging.info(logging_df)

    return logging_df



# logging information: percent chance our qb of interest hit the line (this will be important)