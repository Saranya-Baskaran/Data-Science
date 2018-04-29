import numpy as np
import pandas as pd

data_columns = ['movie_name']
# 'movie_title', 'movie_rating',
#                 'movie_genre', 'movie_year', 'movie_directors',
#                 'movie_actors']

candidate_dataframe = pd.read_csv('../data/Candidate_Matches.csv')
predicted_dataframe = pd.read_csv('../data/Predicted.csv')

# Getting index range
possible_matches = len(predicted_dataframe[
                        (predicted_dataframe['predicted'] == 1)])

possible_range = range(possible_matches)

# Get new dataframe
id_count = 0

# Map to maintain list of already added movies
added_movies = []

# Create new dataframe
movies = pd.DataFrame(index = possible_range, columns=data_columns)

# Iterate through all the predictions_dataframe
for i, row in predicted_dataframe.iterrows():

    # Check if both ltable and rtable id not already added
    l_id = int(row['ltable_id'])
    r_id = int(row['rtable_id'])

    if int(row['predicted']) == 1:
        # Check if one of the ids is already in added_movies
        if l_id not in added_movies and r_id not in added_movies:
            # adding movie title
            # equal movie names
            # if candidate_dataframe[_id]['ltable_Title'] == candidate_dataframe[_id]['rtable_Title']:
            movies.iloc[id_count]['movie_name'] = candidate_dataframe.loc[candidate_dataframe['ltable_id'] == l_id]['ltable_Title']
            added_movies.append(l_id)
            added_movies.append(r_id)
            id_count += 1

print(movies)
