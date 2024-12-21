# functions for initializing a quarterback passing yards database
# defensive data included to weight passing yards based on strength of opposition

import sqlite3
import os
import numpy as np
import pandas as pd
import src.data.webscraping_functions as wf
import src.data.hash as hs



def add_defense(database: str, table: str, year: int):

    """
    Scrapes pro football reference defensive data to create or add to a table in a specified database
    
    Args:
        - database (str): a sqlite database
        - table (str): a sqlite table
        - year (int): the year of defensive data to be scraped and added to the database table

    Returns: 
        - the sqlite table as a Pandas Dataframe
    """

    df = wf.scrape_def(year)

    # keep only the team, and the yards columns
    df = df[['Tm', 'Yds.1']].copy()
    df.rename(columns = {'Tm': 'team', 'Yds.1': 'pyds_allowed'}, inplace = True)
    df['year'] = year

    # create a unique defense_id
    df['defense_id'] = df.apply(lambda row: hs.generate_key(position = 'defense', team = row['team'], year = row['year']), axis = 1)

    # ranking the defenses for that year
    df.sort_values(by = 'pyds_allowed', ascending = True, inplace = True)
    df['rank'] = df['pyds_allowed'].rank(method = 'dense', ascending = True).astype(int)

    # add in a weights column for adjusting qb yards based on strength of defense played
    df['weight'] = 1
    
    conn = sqlite3.connect(database)

    # create a table with a primary key for the defense
    conn.execute(
                f'CREATE TABLE IF NOT EXISTS {table} (\
                 defense_id TEXT PRIMARY KEY,\
                 team TEXT NOT NULL,\
                 year INTEGER NOT NULL,\
                 pyds_allowed REAL,\
                 rank INTEGER,\
                 weight REAL\
                 )') 

    # delete existng rows for the specified year
    conn.execute(f'DELETE FROM {table} WHERE year = ?', (year,))

    # write the dataframe to the sqlite table
    df.to_sql(table, conn, if_exists = 'append', index = False)
    conn.commit()
    conn.close()

    return df.reset_index(inplace = True)


def calculate_weights(database: str, table: str):

    """
    Calculates weights for stat adjustment in any table with defenseive stats and rankings by that stat

    Args:
        - database (str): a sqlite database
        - table (str): a sqlite table with defensive stats, and rankings by that stat

    Returns:
        - the sqlite table as a pandas dataframe
    """

    conn = sqlite3.connect(database)

    query = f'''
    SELECT 
        ds.defense_id, 
        ds.team, ds.year, 
        ds.pyds_allowed, 
        ds.rank, 
        (SELECT AVG(pyds_allowed) FROM {table}) / ra.ranked_average AS weight 
    FROM 
        {table} ds 
    JOIN 
        (SELECT rank, AVG(pyds_allowed) AS ranked_average FROM {table} GROUP BY rank) ra 
    ON 
        ds.rank = ra.rank
    ''' 

    df = pd.read_sql_query(query, conn)
    
    df.to_sql(table, conn, if_exists = 'replace', index = False)
    
    conn.commit()
    conn.close()

    return df


def create_gamelogs(directory: str, database: str, table: str, rank_table: str):

    """
    Compiles qb game logs in csv format into a sqlite database table

    Args:
        - directory (str): folder where csv gamelogs are stored (pfr prohibits scraping of data of this type)
        - database (str): a sqlite database
        - table (str): a sqlite table to be created
        - rank_table (str): a sqlite table with defensive rankings and weights
    """

    conn = sqlite3.connect(database)
    # create table
    conn.execute(
                f'''CREATE TABLE IF NOT EXISTS {table} ( 
                qb_id TEXT PRIMARY KEY,  
                year INT, 
                week INT, 
                name TEXT, 
                team TEXT NOT NULL,  
                pass_yards REAL,
                opponent TEXT,  
                defense_id TEXT, 
                opp_rank INTEGER, 
                weight REAL, 
                adjusted_yards REAL 
                 )''') 

    # create dataframe to concatenate individual player data onto
    game_logs = pd.read_sql_query(f"SELECT * FROM {table}", conn)
    
    # loop through the proper directory
    # add each player to the database table
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)

            df = pd.read_csv(file_path)

            # keep only relevant columns
            df = df[['Year', 'Week', 'Tm', 'Opp', 'Yds']]
            df.rename(columns = {'Year': 'year', 'Week': 'week', 'Tm': 'team',
                                 'Opp': 'opponent', 'Yds': 'pass_yards'}, inplace = True)

            # find the player name from the filename
            # filenames are format 'first_last_career.csv
            name_list = filename.split("_")
            name = " ".join(name_list[:2])
            df['name'] = name 

            # format columns
            df['year'] = df['year'].astype(int)
            df['week'] = df['week'].astype(int)

            # the data is imported as a team abbreviation, which needs to be mapped to the full team name
            df['team'] = df['team'].map(abbreviation_team_dict)
            df['opponent'] = df['opponent'].map(abbreviation_team_dict)

            # 'rank', 'weight', and 'adjusted_yards' will be assigned to the defenses with a join on defense_id
            df['opp_rank'] = 0
            df['weight'] = 0
            df['adjusted_yards'] = 0

            # add in keys
            df['qb_id'] = df.apply(lambda row: hs.generate_key(position = 'quarterback', name = row['name']), axis = 1)
            df['defense_id'] = df.apply(lambda row: hs.generate_key(position = 'defense', team = row['opponent'], year = row['year']), axis = 1)

            # concatenate the dataframe
            game_logs = pd.concat([game_logs, df])

    # handle null values

    game_logs.to_sql(table, conn, if_exists = "replace", index = False)

    query = f"""
    SELECT 
        gl.qb_id, 
        gl.year, 
        gl.week, 
        gl.name, 
        gl.team, 
        gl.pass_yards, 
        gl.opponent, 
        gl.defense_id, 
        ds.rank AS opp_rank, 
        ds.weight AS weight, 
        gl.pass_yards * ds.weight AS adjusted_yards 
    FROM 
        {table} gl 
    JOIN 
        {rank_table} ds 
     ON gl.defense_id = ds.defense_id 
    """

    game_logs = pd.read_sql_query(query, conn)
    conn.commit()
    conn.close()

    return game_logs


# scrape season data
def agg_passing(database, table, year):

    """
    Creates a sqlite table of aggregated quarterback passing yards.

    Args:
        - database (str): a sqlite database
        - table (str): a sqlite table
        - year (int): the year in which the game logs will be collected 

    Returns:
        - a pandas dataframe with aggregated passing yards data
    """

    # webscraping function adds keys and cleans data
    df = wf.scrape_pass(year)

    conn = sqlite3.connect(database)

    df.to_sql(table, conn, if_exists="replace", index=False)

    conn.close()

    return df



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
    'Oakland Raiders': 'OAK',
    'San Diego Chargers': 'SDG',
    'Los Angeles Chargers': 'LAC',
    'St. Louis Rams': 'STL',
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
    'Washington Redskins': 'WAS',
    'Washington Football Team': 'WAS'
}

# Reverse the dictionary
abbreviation_team_dict = {value: key for key, value in team_abbreviation_dict.items()}


