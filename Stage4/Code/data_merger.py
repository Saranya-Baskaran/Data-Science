import numpy as np
import pandas as pd
import pdb

data_columns = ['movie_name', 'movie_rating', 'movie_year']
#                 'movie_genre', , 'movie_directors',
#                 'movie_actors']

candidate_dataframe = pd.read_csv('../data/Candidate_Matches.csv')
predicted_dataframe = pd.read_csv('../data/Predicted.csv')

# Getting index range
possible_matches = len(predicted_dataframe[
                        (predicted_dataframe['predicted'] == 1)])

possible_ranges = range(possible_matches)
# Get new dataframe
id_count = 0

# Map to maintain list of already added movies
added_movies = []

# Create new dataframe
movies = pd.DataFrame(index = possible_ranges,columns=data_columns)

# Iterate through all the predictions_dataframe
for i, row in predicted_dataframe.iterrows():

    # Check if both ltable and rtable id not already added
    l_id = int(row['ltable_id'])
    r_id = int(row['rtable_id'])

    if int(row['predicted']) == 1:
        # Check if one of the ids is already in added_movies
        if l_id not in added_movies and r_id not in added_movies:

            # adding movie title - Always take imdb movie title
            movie_name_series = candidate_dataframe.loc[candidate_dataframe['rtable_id'] == r_id]['rtable_Title']
            movie_name_str = str(movie_name_series[0])

            # Get average rating - (Filmcrave * 2.5 + imdb)/2
            filmcrave_rating_series = candidate_dataframe.loc[candidate_dataframe['ltable_id'] == l_id]['ltable_Overall Rating']
            imdb_rating_series = candidate_dataframe.loc[candidate_dataframe['rtable_id'] == r_id]['rtable_Overall Rating']

            # Some cleaning stuff
            filmcrave_rating_list = str(filmcrave_rating_series[0]).split('/')
            filmcrave_rating = float(filmcrave_rating_list[0])
            imdb_rating = float(imdb_rating_series[0])
            average_rating = (filmcrave_rating * 2.5 + imdb_rating) / 2

            # Get movie year. Always take IMDB year.
            movie_year_series = candidate_dataframe.loc[candidate_dataframe['rtable_id'] == r_id]['rtable_Year']
            movie_year = int(movie_year_series[0])

            # Get Movie Genres - Take union of both genres
            filmcrave_genre_series = candidate_dataframe.loc[candidate_dataframe['ltable_id'] == l_id]['ltable_Genre']
            imdb_genre_series = candidate_dataframe.loc[candidate_dataframe['rtable_id'] == r_id]['rtable_Genre']

            # Getting individual genre fields
            filmcrave_genres = str(filmcrave_genre_series[0]).split('/')
            imdb_genres = str(imdb_genre_series[0]).split(',')
            genre_set = set()

            # cleaning genre and getting union
            for val in imdb_genres:
                val = str(val).strip()
                genre_set.add(val)

            for val in filmcrave_genres:
                val = str(val).strip()
                genre_set.add(val)

            movie_genre_list = list(genre_set)
            movie_genres = ','.join(movie_genre_list)


            added_movies.append(l_id)
            added_movies.append(r_id)
            break
            id_count += 1
