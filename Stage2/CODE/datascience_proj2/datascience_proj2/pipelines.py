# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv

class datainsertion(object):
    count = 0
    def process_item(self, item, spider):
        filmcrave_item = []
        imdb_movie_item = []
        #count += 1
        if spider.name == 'filmcrave':
            #filmcrave_item.append(str(count))
            filmcrave_item.append(item['movie_title'])
            filmcrave_item.append(item['movie_overall_rating'])
            filmcrave_item.append(item['movie_year'])
            filmcrave_item.append(item['movie_genre'])
            filmcrave_item.append(item['movie_mpa_rating'])
            filmcrave_item.append(item['movie_director'])
            filmcrave_item.append(item['movie_actor'])
            filmcrave_item.append(item['movie_plot'])

            with open("filmcrave.csv","a+") as f:
                wr = csv.writer(f, dialect = 'excel')
                wr.writerow(filmcrave_item)
        else:
            #imdb_movie_item.append(str(count))
            imdb_movie_item.append(item['movie_title'])
            imdb_movie_item.append(item['movie_overall_rating'])
            imdb_movie_item.append(item['movie_year'])
            imdb_movie_item.append(item['movie_genre'])
            imdb_movie_item.append(item['movie_mpa_rating'])
            imdb_movie_item.append(item['movie_director'])
            imdb_movie_item.append(item['movie_actor'])
            imdb_movie_item.append(item['movie_plot'])

            with open("imdb.csv","a+") as f:
                wr = csv.writer(f, dialect = 'excel')
                wr.writerow(imdb_movie_item)
