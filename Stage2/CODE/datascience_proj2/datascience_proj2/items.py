# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class imdb_movie_item(Item):
	movie_title = Field()
	movie_overall_rating = Field()
	movie_year = Field()
	movie_genre = Field()
	movie_mpa_rating = Field()
	movie_director = Field()
	movie_actor = Field()
	movie_plot = Field()
	movie_duration = Field()

class filmcrave_movie_item(Item):
    movie_title = Field()
    movie_overall_rating = Field()
    movie_year = Field()
    movie_genre = Field()
    movie_mpa_rating = Field()
    movie_director = Field()
    movie_actor = Field()
    movie_plot = Field()
