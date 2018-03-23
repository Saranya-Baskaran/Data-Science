# -*- coding: utf-8 -*-
import scrapy
from datascience_proj2.items import filmcrave_movie_item

class FilmcraveSpider(scrapy.Spider):


    name = 'filmcrave'
    #start_urls = ['http://www.filmcrave.com/list_top_movie.php?yr=2017']
    start_urls = []
    for i in range(1,24):
        start_urls.append("http://www.filmcrave.com/list_top_movie.php?yr=2017&page=" + str(i))
    for i in range(1,24):
        start_urls.append("http://www.filmcrave.com/list_top_movie.php?yr=2016&page=" + str(i))
    for i in range(1,24):
        start_urls.append("http://www.filmcrave.com/list_top_movie.php?yr=2015&page=" + str(i))
    for i in range(1,24):
        start_urls.append("http://www.filmcrave.com/list_top_movie.php?yr=2014&page=" + str(i))
    for i in range(1,24):
        start_urls.append("http://www.filmcrave.com/list_top_movie.php?yr=2013&page=" + str(i))
    for i in range(1,24):
        start_urls.append("http://www.filmcrave.com/list_top_movie.php?yr=2012&page=" + str(i))
    for i in range(1,24):
        start_urls.append("http://www.filmcrave.com/list_top_movie.php?yr=2011&page=" + str(i))
    for i in range(1,24):
        start_urls.append("http://www.filmcrave.com/list_top_movie.php?yr=2010&page=" + str(i))
    for i in range(1,24):
        start_urls.append("http://www.filmcrave.com/list_top_movie.php?yr=2009&page=" + str(i))
    for i in range(1,24):
        start_urls.append("http://www.filmcrave.com/list_top_movie.php?yr=2008&page=" + str(i))
    for i in range(1,24):
        start_urls.append("http://www.filmcrave.com/list_top_movie.php?yr=2007&page=" + str(i))
    for i in range(1,24):
        start_urls.append("http://www.filmcrave.com/list_top_movie.php?yr=2006&page=" + str(i))
    for i in range(1,24):
        start_urls.append("http://www.filmcrave.com/list_top_movie.php?yr=2005&page=" + str(i))
    for i in range(1,24):
        start_urls.append("http://www.filmcrave.com/list_top_movie.php?yr=2004&page=" + str(i))

    def parse(self, response):
        items = []
        movies = []
        for r in response.xpath(".//tr"):
            movie = []
            name = r.xpath("td[3]/a/text()").extract()
            rating = r.xpath("td[5]/span/text()").extract()
            if not name or not rating:
                continue
            else:
                #print name[0].encode('utf8'), rating[0].encode('utf8')
                movie.append(name[0].encode('utf8'))
                movie.append(rating[0].encode('utf8'))
            movie.append('2017')
            movies.append(movie)
        i = 0
        f = open("output.txt", "a+")
        rows = response.xpath("//tr/td/p")

        for row in rows:
            values = row.xpath(".//text()[preceding-sibling::br]").extract()
            if len(values) > 0:

                for val in values:
                    temp = str(val.encode('utf8')).strip()
                    if temp == "":
                       continue
                    else:
                        movies[i].append(temp)
                        # f.write(temp)
                        # f.write("\n")
                i = i + 1
                # f.write("********************************************************")
                # f.write("\n")

        for movie in movies:
            for m in movie:
                f.write(m)
                f.write("\n")
            f.write("-"*50)
            f.write("\n")

        for movie in movies:
            item = filmcrave_movie_item()
            item['movie_title'] = ""

            item['movie_overall_rating'] = ""

            item['movie_year'] = ""

            item['movie_genre'] = ""

            item['movie_mpa_rating'] = ""

            item['movie_director'] = ""
            item['movie_actor'] = ""

            item['movie_plot'] = ""
            for i in range(len(movie)):
                if i == 0:
                    item['movie_title'] = movie[0].strip()
                if i == 1:
                    item['movie_overall_rating'] = movie[1].strip()
                if i == 2:
                    item['movie_year'] = movie[2].strip()
                if i == 3:
                    item['movie_genre'] = movie[3].strip()
                if i == 4:
                    item['movie_mpa_rating'] = movie[4].strip()
                if i == 5:
                    item['movie_director'] = movie[5].strip()
                if i == 6:
                    item['movie_actor'] = movie[6].strip()
                if i == 7:
                    item['movie_plot'] = movie[7].strip()
            items.append(item)
        f.write("item length" + str(len(items)))
        return items