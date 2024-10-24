
# pfr dataframes include many columns that are unnecessary for this project, which vary by position. 
# we these columns, rename relevant columns for clarity, and convert data to numeric datatypes in 
# preparation for statistical analysis

import numpy as np
import pandas as pd

def defense_column_transform(df, year: int):
    """
    keeps only the relevant columns, and renames for clarity
    """

    df = df[['Tm', 'Yds.1', 'Yds.4']].copy()
    df.rename(columns = {'Yds.1': 'PassYds', 'Yds.4': 'RushYds'}, inplace = True)
    df['Year'] = year
        
    return df


def qb_column_transform(df):
    """
    Formats and cleans a pro football reference dataframe with quarterback data

    Args:
        df: a pandas dataframe containing the data

    Returns:
        df: relevant columns of the dataframe, renamed for clarity 
    """

    # keep only relevant columns
    df = df[['Rk', 'Year', 'Date', 'Week', 'Tm', 'Opp', 'Result', 'Unnamed: 7', 'GS',
                                    'Att', 'Yds', 'TD', 
                                    'Yds.2', 'TD.1']].copy()

    
    # rename columns for clarity
    df.rename(columns = {'Yds': 'PassYds'}, inplace = True)
    df.rename(columns = {'TD': 'PassTD'}, inplace = True)
    df.rename(columns = {'Yds.2': 'RushYds'}, inplace = True)
    df.rename(columns = {'TD.1': 'RushTD'}, inplace = True)
    df.rename(columns = {'Unnamed: 7': 'Home'}, inplace = True)
    df.rename(columns = {'Rk': 'Time'}, inplace = True)
    df.rename(columns = {'GS': 'Started'}, inplace = True)

    # convert columns to numeric datatype
    df['PassYds'] = pd.to_numeric(df['PassYds'], errors='coerce')
    df['PassTD'] = pd.to_numeric(df['PassTD'], errors='coerce')
    df['RushYds'] = pd.to_numeric(df['RushYds'], errors='coerce')
    df['RushTD'] = pd.to_numeric(df['RushTD'], errors='coerce')
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')

    return df


def rb_column_transform(df):
    """
    Formats and cleans a pro football reference dataframe with runningback data

    Args:
        df: a pandas dataframe containing the data

    Returns:
        df: relevant columns of the dataframe, renamed for clarity 
    """

    # keep only relevant columns
    df = df[['Rk', 'Year', 'Date', 'Week', 'Tm', 'Opp', 'Result', 'Unnamed: 7', 'GS',
                                    'Att', 'Yds', 'TD', 
                                    'Rec', 'Yds.1', 'TD.1']].copy()
    
    # rename columns for clarity
    df.rename(columns = {'Yds': 'RushYds'}, inplace = True)
    df.rename(columns = {'TD': 'RushTD'}, inplace = True)
    df.rename(columns = {'Yds.1': 'RecYds'}, inplace = True)
    df.rename(columns = {'TD.1': 'RecTD'}, inplace = True)
    df.rename(columns = {'Unnamed: 7': 'Home'}, inplace = True)
    df.rename(columns = {'Rk': 'Time'}, inplace = True)
    df.rename(columns = {'GS': 'Started'}, inplace = True)

    # convert columns to numeric datatype
    df['RecYds'] = pd.to_numeric(df['RecYds'], errors='coerce')
    df['RecTD'] = pd.to_numeric(df['RecTD'], errors='coerce')
    df['RushYds'] = pd.to_numeric(df['RushYds'], errors='coerce')
    df['RushTD'] = pd.to_numeric(df['RushTD'], errors='coerce')
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')

    return df


def format(df, position: str, year = False):
    """
    Formats and cleans a pro football reference dataframe

    Args:
        df: a pandas dataframe containing the data
        position: a string indicating the position of the player
        year: required argument for def_column_transforms

    Returns:
        df: a formatted and cleaned pandas dataframe 
    """

    # add in a started parameter for QB and RB. 
    # add in a name parameter

    # keep only relevant data for each position
    if position == 'RB':
        df = rb_column_transform(df)

    elif position == 'QB':
        df = qb_column_transform(df)

    elif position == 'DEF':

        df = defense_column_transform(df, year)
        return df

    # turn home into a boolean value
    df['Home'] = df['Home'].map(lambda x: x != '@')

    # turn ttarted into a boolean value
    df['Started'] = df['Started'].map(lambda x: x == '*')
        
    return df
