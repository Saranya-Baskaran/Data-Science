import pandas as pd
from merger_methods import merger, nomerge
from populate_foreigntables import *

movie_data_columns = ['movie_name', 'movie_rating', 'movie_year', 'movie_genres',
                'movie_directors', 'movie_actors']

genre_data_columns = ['movie_id','genre_id', 'genre_name']
director_data_columns = ['movie_id', 'director_id', 'director_name']
actor_data_columns = ['movie_id', 'actor_id', 'actor_name']

candidate_dataframe = pd.read_csv('../data/Candidate_Matches.csv')
predicted_dataframe = pd.read_csv('../data/Predicted.csv')

# Getting index range
possible_matches = len(predicted_dataframe[
                        (predicted_dataframe['predicted'] == 1)])

print('Total tuple combinations: ',len(predicted_dataframe))

# id's for tables
id_count = 0
director_id = 0
actor_id = 0
genre_id = 0

# Map to maintain list of already added movies
added_movies = []
added_directors = []
added_genres = []
added_actors = []

# Create new dataframes
movies = pd.DataFrame(columns=movie_data_columns)
genres = pd.DataFrame(columns=genre_data_columns)
directors = pd.DataFrame(columns=director_data_columns)
actors = pd.DataFrame(columns=actor_data_columns)


# Iterate through all the predictions_dataframe
for i, row in predicted_dataframe.iterrows():

    # Check if both ltable and rtable id not already added
    l_id = int(row['ltable_id'])
    r_id = int(row['rtable_id'])

    merged_movie = []
    if int(row['predicted']) == 1:
        # Check if one of the ids is already in added_movies
        if l_id not in added_movies and r_id not in added_movies:
            # call merger for l_id and r_id
            merged_movie = merger(candidate_dataframe, l_id, r_id)
            added_movies.append(l_id)
            added_movies.append(r_id)

    # Cannot do this because l_id and r_id need not be same
    # else:
    #     if l_id not in added_movies:
    #         # Call nomerge method to extract only from one table
    #         merged_movie = nomerge(candidate_dataframe, l_id, 0)
    #         added_movies.append(l_id)
    #
    #     if r_id not in added_movies:
    #         # Call nomerge method to extract only from one table
    #         merged_movie = nomerge(candidate_dataframe, r_id, 1)
    #         added_movies.append(r_id)

    if merged_movie:
        # Append to movies dataframe
        movies = movies.append({
        'movie_name':merged_movie[0],
        'movie_rating':merged_movie[1],
        'movie_year':merged_movie[2],
        'movie_genres':merged_movie[3],
        'movie_directors':merged_movie[4],
        'movie_actors':merged_movie[5]
        }, ignore_index=True)

        genres, genre_id = populate_genre_table(genres, id_count, genre_id,
                            merged_movie[3], added_genres)

        directors, director_id = populate_director_table(directors, id_count,
                                 director_id, merged_movie[4], added_directors)

        actors, actor_id = populate_actor_table(actors, id_count, actor_id,
                            merged_movie[5], added_actors)

        id_count += 1

movies = movies[pd.notnull(movies['movie_name'])]
genres = genres[pd.notnull(genres['genre_name'])]
directors = directors[pd.notnull(directors['director_name'])]
actors = actors[pd.notnull(actors['actor_name'])]


print('Total number of movies ', len(movies))
print('Total number of genres ', genre_id)
print('Total number of directors ', director_id)
print('Total number of actors ', actor_id)


movies.to_csv('../Data/movie_table.csv')
genres.to_csv('../Data/genre_table.csv')
directors.to_csv('../Data/director_table.csv')
actors.to_csv('../Data/actor_table.csv')
