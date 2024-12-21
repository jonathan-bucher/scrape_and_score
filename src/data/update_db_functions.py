# script to update quarterback gamelogs and defensive stats on a weekly basis during the nfl season

# download the season schedule updated at start of the season
# create a qb database with each quarterbacks info that will be updated at the start of the season

# subtract the yards weekly to find how many points was put up by opponent that week
    # match yards to quarterback using qb table

    # create game log for that week with week, year 
        # qb name, team, id FROM qb
        # opponent FROM schedule
        # opp_rank, defense_id, weight, adjusted_yards FROM defense_stats
        # append it all onto gamelogs every week if not BYE

# database = r"C:\Users\jonat\OneDrive\projects\scrape_and_score\data\nfl_database.db"

# scrape current defense data
# subtract from last week
# store as a dataframe with team, opponent, and yards allowed
# map onto the 'active_qb' table, which has quarterback, team, team_id,
# store this as a single week of data
# map this onto rankings, weights, and adjusted yards
# append on to the 

# scrape qb season rankings;
# subtract them from last week
# use schedule to map this onto the opponent
    # this may actually be somewhat tricky
# then it's easy
import sqlite3
import hashlib
import os
import numpy as np
import pandas as pd
import src.data.webscraping_functions as wf

#mschedule = r"C:\Users\jonat\OneDrive\projects\scrape_and_score\data\processed\2024_schedule.txt"

def update_defense(year: int):
    """
    updates the defense_stats table every week
    """
    pass


def update_gamelogs(database: str, table: str, agg_table: str, schedule: str, year: int, week: int):
    """
    Updates quarterback gamelogs

    Args:
        - database (str): a sqlite database
        - table (str): a sqlite table where gamelogs will be appended
        - agg_table (str): a sqlite table with quarterback aggregated passing stats for a given year
        - schedule (str): a csv file containing an nfl schedule 
    """

    df = wf.scrape_pass(year)

    schedule = pd.read_csv(schedule)
    # find games for current week
    schedule = schedule.loc[schedule['week'] == week]       # week is str?
    schedule_dict = dict(zip(schedule['team'], schedule['opp']))
    df['opponent'] = df['team'].map(schedule_dict)
    
    # subtract pass_yards from season data
    conn = sqlite3.connect(database)
    agg_df = pd.read_sql_query(f"SELECT * FROM {agg_table}", conn)
    
    
    # overwrite old aggregate data


    # df['pass_yards'] = df['pass_yards] - season_df['pass_yards]

    # operations to append on and multiply, either new function or existing function

    # Append on to gamelogs

    pass
