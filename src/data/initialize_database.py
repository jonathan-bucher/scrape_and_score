# initializing NFL passing yards database

import src.data.database_functions as df
import os

database = r"C:\Users\jonat\OneDrive\projects\scrape_and_score\data\quarterback.db"
directory = r"C:\Users\jonat\OneDrive\projects\scrape_and_score\data\raw\gamelogs"

os.remove(database)
year = 2024

# create a table for defensive data
for year in range(2005, year + 1):

    df.add_defense(database, "defense_stats", year)


# add a 'weights' column for adjusted yards metrics
df.calculate_weights(database, "defense_stats")

# quarterback game logs table
df.create_gamelogs(directory, database, table = "gamelogs", rank_table = "defense_stats")

# quarterback aggregated passing stats
df.agg_passing(database, "agg_passing_stats", year)