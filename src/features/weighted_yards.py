# create an 'adjusted yards' metric for comparing quarterbacks

# average yards per ranking in central df (create a dictionary)

# create adjusted yards column

import pandas as pd

all_defense = pd.read_csv(r"C:\Users\jonat\OneDrive\projects\scrape_and_score\data\processed\all_defense.txt")

# find the average value for each defense rank

# define a dictionary mapping ranking to average yards allowed
rank_weights = {}
rank_weights['overall_average'] = all_defense['PassYds'].mean()

for rank in range(1, 33):

    # locate all defenses of this rank
    weighted_all_defense = all_defense.loc[all_defense['def_rk'] == rank]

    # add the average yards to the defense rank
    rank_weights[rank] = weighted_all_defense.loc[:, 'PassYds'].mean()

print(rank_weights)
# import all_quarterbacks, and created a weighted average for each yardage total 