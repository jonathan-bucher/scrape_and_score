# clean and format raw qb data
# cache to processed data
# compile into single dataframe

import os
import pandas as pd
import src.data.column_transforms as ct
import src.features.assign_rankings as ar

folder_path = r"C:\Users\jonat\OneDrive\projects\scrape_and_score\data\raw\quarterbacks"
all_defenses = pd.read_csv(r"C:\Users\jonat\OneDrive\projects\scrape_and_score\data\processed\all_defense.txt")

dfs = []

# loop through each file in the directory

for file_name in os.listdir(folder_path):

    file_path = os.path.join(folder_path, file_name)
    df = pd.read_csv(file_path)
    
    # format the data
    df = ct.format(df, position = 'QB')

    # drop values where they didn't start
    df = df.loc[df['Started'] == True]

    # drop 2024
    df = df.loc[df['Year'] != 2024]

    # drop rows with null values
    df = df.dropna()

    # rank the defenses faced by passing yardage
    df = ar.qb_def_rankings(all_defenses, df)

    # the following steps are for caching the csv to formatted data
    # create a column with the quarterbacks name
    first_last = file_name.split("_")

    # ensure proper formatting
    assert len(first_last) == 3
    assert first_last[2] == 'career.txt'

    name = f"{first_last[0]} {first_last[1]}"

    df['name'] = name

    # cache to processed data
    df.to_csv(fr"C:\Users\jonat\OneDrive\projects\scrape_and_score\data\processed\quarterbacks\ftd_{first_last[0]}_{first_last[1]}_career.txt")

    dfs.append(df)

# compile all quarterback data into single dataframe

# concatenate all the dataframes into one central dataframe
central_df = pd.concat(dfs, ignore_index=True)

# save the central dataframe to a new csv
central_df.to_csv(r"C:\Users\jonat\OneDrive\projects\scrape_and_score\data\processed\all_quarterbacks.txt", index=False)
