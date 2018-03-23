# -*- coding: utf-8 -*-
import scrapy
from datascience_proj2.items import imdb_movie_item


class imdbSpider(scrapy.Spider):
    name = 'imdb_spider'
    allowed_domains = ['imdb.com']
    # start_urls = ['http://www.imdb.com/search/title?year=2017,2017&title_type=feature&sort=moviemeter,asc']
    start_urls = []
    start_year = 2017
    for j in range(0, 15):
        curr_year = start_year - j
        for i in range(1, 6):
            start_urls.append("http://www.imdb.com/search/title?year=" + str(curr_year) + "," + str(curr_year) + "&title_type=feature&sort=moviemeter,asc&page=" + str(i))

    count = 0

    def parse(self, response):
        items = []
        for movie in response.xpath('//div[contains(@class, "lister-item-content")]'):
            item = imdb_movie_item()
            
            item['movie_title'] = ""
            item['movie_overall_rating'] = ""
            item['movie_year'] = ""
            item['movie_genre'] = ""
            item['movie_mpa_rating'] = ""
            item['movie_director'] = ""
            item['movie_actor'] = ""
            item['movie_plot'] = ""
            item['movie_duration'] = ""
            
            item['movie_title'] = movie.xpath('.//h3[contains(@class, "lister-item-header")]/a/text()').extract()[
                0].encode('utf8')

            overAllRating = movie.xpath('.//div[contains(@class, "ratings-imdb-rating")]/strong/text()').extract()
            if overAllRating:
                item['movie_overall_rating'] = overAllRating[0].encode('utf8')

            year = movie.xpath('.//span[contains(@class, "lister-item-year")]/text()').extract()
            if year:
                item['movie_year'] = year[0].encode('utf8')

            genre = movie.xpath('.//span[contains(@class, "genre")]/text()').extract()
            if genre:
                item['movie_genre'] = genre[0].encode('utf8')
                item['movie_genre'] = str(item['movie_genre']).strip()

            mpaRating = movie.xpath('.//span[contains(@class, "certificate")]/text()').extract()
            if mpaRating:
                item['movie_mpa_rating'] = mpaRating[0].encode('utf8')

            p_content = movie.xpath('.//p[3]')
            names = p_content.xpath('.//a/text()').extract()
            start_names = 0

            p_content = p_content.extract()
            p_string = ''
            if p_content:
                p_string = p_content[0].encode('utf8')
            p_string_split = p_string.split("\n")

            item['movie_director'] = []
            item['movie_actor'] = []

            for div in p_string_split:
                div = div.strip()
                if div.startswith("<a"):
                    item['movie_director'].append(names[start_names].encode('utf8'))
                    start_names += 1
                elif div.startswith("<span"):
                    break

            for i in range(start_names, len(names)):
                item['movie_actor'].append(names[i].encode('utf8'))

            plot = movie.xpath('p[2]/text()').extract()
            if plot:
                item['movie_plot'] = (plot[0].encode('utf8')).strip()

            duration = movie.xpath('.//span[contains(@class, "runtime")]/text()').extract()
            if duration:
                item['movie_duration'] = duration[0].encode('utf8')

            items.append(item)
            self.count += 1

        return items




