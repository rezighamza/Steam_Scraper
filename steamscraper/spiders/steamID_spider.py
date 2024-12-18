from scrapy import Spider, Request
from steamscraper.items import SteamGameItem
from scrapy.http import FormRequest
import pandas as pd
import re
import logging


class SteamSpider(Spider):
    name = "steamID_spider"
    allowed_domains = ["store.steampowered.com"]
    start_urls = ["https://store.steampowered.com/search/?category1=998"]

    def parse(self, response):
        # Start by parsing the initial search page.
        # Find the number for the last page of the games
        last_page = int(response.xpath('//div[@class="search_pagination_' +
                                       'right"]/a/text()')[-2].extract())
        # Use a list comprehension to generate all of the pages that will
        # for our case , we will scrape the first 2000 pages , so we will get 50000 games
        last_page = 2000
        # need to be scraped.
        browse_url_list = [('https://store.steampowered.com/search/?' +
                            'sort_by=Released_DESC&category1=998&page={}&' +
                            'supportedlang=english').format(x)
                           for x in range(1, last_page + 1)]
        # Yield a request for each page that contains a list of games
        for url in browse_url_list:
            yield Request(url=url, callback=self.parse_browse_page)
    def parse_browse_page(self, response):
        # Extract games on the current page
        games = response.xpath('//div[@id="search_resultsRows"]/a')

        for game in games:
            yield {
                "name": game.xpath('.//span[@class="title"]/text()').get(),
                "steam_appid": game.xpath('./@href').re_first(r'app/(\d+)/')
            }

        # Follow the next page link
        next_page = response.xpath('//a[@class="pagebtn" and contains(text(), "›")]/@href').get()
        if next_page:
            yield Request(url=next_page, callback=self.parse)
