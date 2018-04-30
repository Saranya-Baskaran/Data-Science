import pandas as pd
from merger_methods import merger, nomerge
from directors import populate_director_table

movie_data_columns = ['movie_name', 'movie_rating', 'movie_year', 'movie_genres',
                'movie_directors', 'movie_actors']

actor_data_columns = ['movie_id', 'actor_id', 'actor_name']
director_data_columns = ['movie_id', 'director_id', 'director_name']
genre_data_columns = ['movie_id','genre_id', 'genre_name']

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

# Map to maintain list of already added movies
added_movies = []
added_directors = []
added_genres = []
added_actors = []

# Create new dataframes
movies = pd.DataFrame(columns=movie_data_columns)
directors = pd.DataFrame(columns=director_data_columns)
actors = pd.DataFrame(columns=actor_data_columns)
genres = pd.DataFrame(columns=genre_data_columns)
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

        # directors, director_id = populate_director_table(directors, id_count,
                                # director_id, merged_movie[4], added_directors)

        movie_directors_list = merged_movie[4].split(',')

        for director in movie_directors_list:

            if director in added_directors:
                idx = added_directors.index(director) + 1
            else:
                director_id += 1
                idx = director_id
                added_directors.append(director)

            directors = directors.append({
            'movie_id':id_count,
            'director_id':idx,
            'director_name':director
            }, ignore_index=True)

        id_count += 1

movies = movies[pd.notnull(movies['movie_name'])]
directors = directors[pd.notnull(directors['director_name'])]

print('Total number of movies ', len(movies))
print('Total number of directors ', director_id)

movies.to_csv('../Data/final_movie_data.csv')
directors.to_csv('../Data/final_director_data.csv')
