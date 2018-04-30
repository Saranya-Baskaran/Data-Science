def nomerge(candidate_dataframe, _id, mode):

    if mode == 0:
        t_id = 'l'
    else:
        t_id = 'r'

    locator = t_id + 'table_id'
    title = t_id + 'table_Title'
    rating = t_id + 'table_Overall Rating'
    year = t_id + 'table_Year'
    genre = t_id + 'table_Genre'
    directors = t_id + 'table_Directors'
    actors = t_id + 'table_Actors'

    idx = candidate_dataframe.index[candidate_dataframe[locator] == _id]

    # adding movie title - Always take imdb movie title
    movie_name_series = candidate_dataframe.loc[idx][title].values[0]
    movie_name = str(movie_name_series)

    movie_rating_series = candidate_dataframe.loc[idx][rating].values[0]
    if mode == 0:
        filmcrave_rating_list = str(movie_rating_series).split('/')
        average_rating = float(filmcrave_rating_list[0])
    else:
        average_rating = float(movie_rating_series)

    movie_year_series = candidate_dataframe.loc[idx][year].values[0]
    movie_year = int(movie_year_series)

    movie_genre_series = candidate_dataframe.loc[idx]['ltable_Genre'].values[0]
    if mode == 0:
        movie_genres_list = str(movie_genre_series).split('/')
    else:
        movie_genres_list = str(movie_genre_series).split(',')

    for val in movie_genres_list:
        val = str(val).strip()

    movie_genres = ','.join(movie_genres_list)

    # Get movie directors - Get from IMDB more reliable
    movie_director_series = candidate_dataframe.loc[idx][directors].values[0]
    movie_directors = str(movie_director_series)

    # Get movie actors - Get from IMDB more reliable
    movie_actor_series = candidate_dataframe.loc[idx][actors].values[0]
    movie_actors = str(movie_actor_series)

    result = [movie_name, average_rating, movie_year, movie_genres,
              movie_directors, movie_actors]

    return result


def merger(candidate_dataframe, l_id, r_id):

    r_index = candidate_dataframe.index[candidate_dataframe['rtable_id'] == r_id]
    l_index = candidate_dataframe.index[candidate_dataframe['ltable_id'] == l_id]

    # adding movie title - Always take imdb movie title
    movie_name = candidate_dataframe.loc[r_index]['rtable_Title'].values[0]

    # Get average rating - (Filmcrave * 2.5 + imdb)/2
    filmcrave_rating_series = candidate_dataframe.loc[l_index]['ltable_Overall Rating'].values[0]
    imdb_rating_series = candidate_dataframe.loc[r_index]['rtable_Overall Rating'].values[0]

    # Some cleaning stuff
    filmcrave_rating_list = str(filmcrave_rating_series).split('/')
    filmcrave_rating = float(filmcrave_rating_list[0])
    imdb_rating = float(imdb_rating_series)
    average_rating = (filmcrave_rating * 2.5 + imdb_rating) / 2

    # Get movie year. Always take IMDB year.
    movie_year_series = candidate_dataframe.loc[r_index]['rtable_Year'].values[0]
    movie_year = int(movie_year_series)

    # Get Movie Genres - Take union of both genres
    filmcrave_genre_series = candidate_dataframe.loc[l_index]['ltable_Genre'].values[0]
    imdb_genre_series = candidate_dataframe.loc[r_index]['rtable_Genre'].values[0]

    # Getting individual genre fields
    filmcrave_genres = str(filmcrave_genre_series).split('/')
    imdb_genres = str(imdb_genre_series).split(',')
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

    # Get movie directors - Get from IMDB more reliable
    imdb_director_series = candidate_dataframe.loc[r_index]['rtable_Directors'].values[0]
    movie_directors = str(imdb_director_series)

    # Get movie actors - Get from IMDB more reliable
    imdb_actor_series = candidate_dataframe.loc[r_index]['rtable_Actors'].values[0]
    movie_actors = str(imdb_actor_series)

    result = [movie_name, average_rating, movie_year, movie_genres,
              movie_directors, movie_actors]

    return result
