# pro football reference allows webscraping for team defensive data by season. We scrape defense data back to 2005,
# and cache this data to csv files, before and after proper formatting. 
# understandably, pro football reference does not condone scraping of player game logs, 
# but still generously offers manual export options for these tables

import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import src.data.hash as hs
from src.data.database_functions import *


def scrape_def(year: int, cache = False):

    """
    scrapes and caches pro football reference defensive season rankings dataframes 
    """

    # opening webpage
    
    url = f"https://www.pro-football-reference.com/years/{year}/opp.htm"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # locate the data

    table = soup.find('table', {'id': 'team_stats'})

    # extract subheaders. In this case, we are uninterested in the headers, so we start at the second row.

    subheaders = []
    header_row = table.find_all('tr')[1]    # taking the second row
    repeat_counter = 1                      # needed to identify repeat column labels

    for th in header_row.find_all('th')[1:]:    # 'rank' column is encoded as a header, so we skip this
        subheader = th.text.strip()
        if subheader in subheaders:
            subheader = f"{subheader}.{repeat_counter}"
            repeat_counter += 1
        subheaders.append(subheader)

    # extract the data rows
    
    rows = []
    for row in table.find_all('tr')[2:-3]:    # skip the first two header rows and last three compiled stat rows
        cells = row.find_all('td')     # last three rows are average team stats
        cells = [cell.text.strip() for cell in cells]
        if len(cells) == len(subheaders):  # Ensure the number of columns match. In this case, the table is so large there are multiple headers embedded in the data
            rows.append(cells)
        else:
            print(f"Skipping row with {len(cells)} columns, expected {len(subheaders)}")

    # create dataframe
    df = pd.DataFrame(rows, columns = subheaders)
    df.replace("", np.nan, inplace = True)

    if cache == True:
        # cache raw data
        df.to_csv(rf"C:\Users\jonat\OneDrive\projects\scrape_and_score\data\raw\defense\{year}_nfl_defense_data.txt", index = False)

    return df

    # import the schedule file
    # create a dictionary mapping teams to oponents for that specific week
    # map the value over


def scrape_pass(year: int):

    """
    scrapes and caches pro football reference qb season rankings dataframes 
    """

    url = f"https://www.pro-football-reference.com/years/{year}/passing.htm"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'id': 'passing'})

    # extract headers
    headers = []
    header_row = table.find_all('tr')[0]    # taking the headers

    for th in header_row.find_all('th')[1:]:    # 'rank' column is encoded as a header, so we skip this
        subheader = th.text.strip()
        headers.append(subheader)

    # extract the data rows
    rows = []
    for row in table.find_all('tr')[1:]:    # skip the first header row
        cells = row.find_all('td')     # last three rows are average team stats
        cells = [cell.text.strip() for cell in cells]
        if len(cells) == len(headers):  # Ensure the number of columns match. In this case, the table is so large there are multiple headers embedded in the data
            rows.append(cells)
        else:
            print(f"Skipping row with {len(cells)} columns, expected {len(headers)}")

    # create dataframe
    df = pd.DataFrame(rows, columns = headers)                                                                  # create dataframe
    df = df.loc[:, ~df.columns.duplicated()]                                                                    # dropping duplicate column names
    df = df[["Player", "Team", "Yds"]]                                                                          # keeping only relevant columns
    df = df.rename(columns = {'Player': 'name', 'Team': 'team', 'Yds': 'pass_yards'})                           # rename columns
    df['name'] = df['name'].str.lower()                                                                         # change names to lowercase
    df['qb_id'] = df.apply(lambda row: hs.generate_key(position = 'quarterback', name = row['name']), axis = 1)    # creat qb_id key
    df['team'] = df['team'].map(abbreviation_team_dict)
    # df['opponent'] = df['team'].map()

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
