def populate_director_table(directors, id_count, director_id, movie_directors,
                            added_directors):

    movie_directors_list = movie_directors.split(',')

    for director in movie_directors_list:

        if director in added_directors:
            idx = added_directors.index(director)
        else:
            idx = director_id
            director_id += 1
            added_directors.append(director)

        directors = directors.append({
        'movie_id':id_count,
        'director_id':idx,
        'director_name':director
        }, ignore_index=True)

    return directors, director_id

def populate_actor_table(actors, id_count, actor_id, movie_actors,
                            added_actors):

    movie_actors_list = movie_actors.split(',')

    for actor in movie_actors_list:

        if actor in added_actors:
            idx = added_actors.index(actor)
        else:
            idx = actor_id
            actor_id += 1
            added_actors.append(actor)

        actors = actors.append({
        'movie_id':id_count,
        'actor_id':idx,
        'actor_name':actor
        }, ignore_index=True)

    return actors, actor_id

def populate_genre_table(genres, id_count, genre_id, movie_genres,
                            added_genres):

    movie_genres_list = movie_genres.split(',')

    for genre in movie_genres_list:

        if genre in added_genres:
            idx = added_genres.index(genre)
        else:
            idx = genre_id
            genre_id += 1
            added_genres.append(genre)

        genres = genres.append({
        'movie_id':id_count,
        'genre_id':idx,
        'genre_name':genre
        }, ignore_index=True)

    return genres, genre_id
