# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
"""
the items that we to get for each game are:
- title
- game_id
- price (if not on sale)
- orig_price (if on sale)
- description
- percent_pos (percentage of positive reviews)
- total_reviews
- release_date
- developer
- publisher
- early_access (boolean)
- vr_only (boolean)
- vr_supported (boolean)
- vr_pcinput (list that contains the VR input types supported ex : ['Keyboard/Mouse', 'Gamepad', 'Oculus Rift', 'HTC Vive'])
"""


class SteamscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass  # -*- coding: utf-8 -*-


class SteamGameItem(scrapy.Item):
    ''' Class for holding the data scraped from each individual game. '''

    tag_list = scrapy.Field()
    title = scrapy.Field()
    game_id = scrapy.Field()
    price = scrapy.Field()
    orig_price = scrapy.Field()
    description = scrapy.Field()
    percent_pos = scrapy.Field()
    total_reviews = scrapy.Field()
    release_date = scrapy.Field()
    developer = scrapy.Field()
    publisher = scrapy.Field()
    early_access = scrapy.Field()
    vr_only = scrapy.Field()
    vr_supported = scrapy.Field()
    vr_pcinput = scrapy.Field()

    def __str__(self):
        ''' Function to generate a string for printing contents of game item.
        '''

        ret_val = '''Title = {} : game_id = {} : tags = {}
        % positive = {} Num of Reviews = {}
        '''.format(self['title'], self['game_id'], str(self['tag_list']),
                   self['percent_pos'], self['total_reviews'])
        if ('orig_price' in self.keys()):
            ret_val += 'Original Price = {} Sale price = {}'\
                .format(self['orig_price'], self['price'])
        else:
            ret_val += 'Price = {}'.format(self['price'])
        ret_val += '''
        Release Date = {}, Developer = {}, Publisher = {}
        Early Access = {}
        Description = {}
        '''.format(self['release_date'], self['developer'], self['publisher'],
                   str(self['early_access']), self['description'])
        if ('vr_only' in self.keys()):
            ret_val += 'VR Only = {}, VR Supported = {}, VR PC Input = {}'\
                .format(str(self['vr_only']), str(self['vr_supported']),
                        str(self['vr_pcinput']))
        return ret_val


class SteamReviewItem(scrapy.Item):
    ''' Class for storing the data scraped from game reviews.
        Currently not used by scraper
    '''

    title = scrapy.Field()
    recommend = scrapy.Field()
    hours_played = scrapy.Field()
    date_posted = scrapy.Field()
    review_text = scrapy.Field()
    username = scrapy.Field()
    products_owned = scrapy.Field()
    num_helpful = scrapy.Field()
    num_funny = scrapy.Field()

    def __str__(self):
        ''' Function to generate a string for printing contents of review item.
        '''
        review_sum = ' '.join(self['review_text'].split()[0:10])
        ret_val = '''
        Title = {}
        Recommend = {}, Hours played = {}, Date posted = {}
        Review = {}
        Username = {}, Products owned = {}
        Number found helpful = {}, Number found funny = {}'''\
        .format(self['title'], str(self['recommennd']),
                self['hours_played'], self['date_posted'], review_sum,
                self['username'], self['products_owned'], self['num_helpful'],
                self['num_funny'])

        return ret_val
