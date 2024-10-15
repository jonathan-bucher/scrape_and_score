# pro football reference allows webscraping for team defensive data by season. We scrape defense data back to 2005,
# and cache this data to csv files, before and after proper formatting. 
# understandably, pro football reference does not condone scraping of player game logs, 
# but still generously offers manual export options for these tables

import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import os
import time

import src.features.assign_rankings as ar
import src.data.column_transforms as ct

def scrape_pfr_data(year: int):

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

    # cache raw data
    df.to_csv(rf"C:\Users\jonat\OneDrive\projects\scrape_and_score\data\raw\defense\{year}_nfl_defense_data.txt", index = False)

    # clean the data, and rank it
    df = ct.defense_column_transform(df.copy(), year)
    df = ar.assign_rankings(df.copy(), 'PassYds')

    # cache processed data
    df.to_csv(rf"C:\Users\jonat\OneDrive\projects\scrape_and_score\data\processed\defense\{year}_nfl_defense_data.txt", index = False)

    return df

# retrieve all data going back to 2005. Compile into seperate folders and also a central dataframe
years = range(2005,2024)
for year in years:
    scrape_pfr_data(year)
    print(f"{year} defense data cached")
    time.sleep(5)

# compile data into a central dataframe

folder_path = r"C:\Users\jonat\OneDrive\projects\scrape_and_score\data\processed\defense"

dfs = []

# loop through each file in the folder
for file_name in os.listdir(folder_path):

    file_path = os.path.join(folder_path, file_name)
    df = pd.read_csv(file_path)
        
    dfs.append(df)

# concatenate all the dataframes into one central dataframe
central_df = pd.concat(dfs, ignore_index=True)

# save the central dataframe to a new csv
central_df.to_csv(r"C:\Users\jonat\OneDrive\projects\scrape_and_score\data\processed\all_defense.txt", index=False)

