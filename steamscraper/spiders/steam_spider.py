from scrapy import Spider, Request
from steamscraper.items import SteamGameItem
from scrapy.http import FormRequest
import pandas as pd
import re
import logging


class SteamSpider(Spider):
    """Class statement for the Steam spider that crawls the Steam website."""

    name = 'steam_spider'
    allowed_urls = ['https://store.steampowered.com']
    start_urls = ['https://store.steampowered.com/app/10/CounterStrike/']
    timeout_urls = 'timeout_urls.list'
    cur_tag_index_pair = 0

    def parse(self, response):
        """Parse the initial response and generate requests for game details."""
        path = "./steam_id.csv"
        game_list = pd.read_csv(path, usecols=['steam_appid']).squeeze("columns")
        game_list = game_list[:2]
        for index, game in game_list.items():
            game_id = game
            detail_url = f"https://store.steampowered.com/app/{game_id}"

            # Skip entries that point to bundles
            if '/sub/' in detail_url:
                continue

            meta = {'game_id': game_id}
            yield Request(
                url=detail_url,
                callback=self.parse_game_detail,
                meta=meta,
                cookies={
                    'wants_mature_content': '1',
                    'birthtime': '189302401',
                    'lastagecheckage': '1-January-1976',
                }
            )

    def parse_game_detail(self, response):
        """Scrape the details for an individual game."""
        game_item = SteamGameItem()

        try:
            game_item['title'] = response.xpath(
                './/div[@class="apphub_AppName"]/text()').get()
        except Exception as e:
            logging.error(f"Error extracting title: {e}")

        try:
            game_item['game_id'] = response.meta['game_id']
        except Exception as e:
            logging.error(f"Error extracting game_id: {e}")

        try:
            game_item['price'] = response.xpath(
                './/div[@class="game_purchase_price price"]/text()').get(default="").strip()
            if not game_item['price']:
                game_item['price'] = response.xpath(
                    './/div[@class="discount_final_price"]/text()').get(default="").strip()
                game_item['orig_price'] = response.xpath(
                    './/div[@class="discount_original_price"]/text()').get(default="").strip()
        except Exception as e:
            logging.error(f"Error extracting price: {e}")

        try:
            release_date = response.xpath('//div[@class="release_date"]/div[@class="date"]/text()').extract_first()
        except Exception as e:
            logging.error(f"Error extracting release_date: {e}")
            release_date = None

        try:
            prerelease_test = response.xpath('//div[@class="game_area_comingsoon game_area_bubble"]') != []
        except Exception as e:
            logging.error(f"Error extracting prerelease_test: {e}")
            prerelease_test = False

        # Skip games without release date or only available for prepurchase.
        if not release_date or prerelease_test:
            return

        try:
            tag_list = list(
                map(lambda x: x.strip(), response.xpath('//div[@class="glance_tags popular_tags"]/a/text()').extract()))
        except Exception as e:
            logging.error(f"Error extracting tag_list: {e}")
            tag_list = []

        try:
            description = response.xpath(
                '//div[@class="game_description_snippet"]/text()').extract_first().lstrip().rstrip()
        except Exception as e:
            logging.error(f"Error extracting description: {e}")
            description = ""

        try:
            test_for_no_reviews = response.xpath('//div[@class="summary column"]/text()').extract_first().strip().find(
                'No user') >= 0
        except Exception as e:
            logging.error(f"Error extracting test_for_no_reviews: {e}")
            test_for_no_reviews = False

        # Handle games with no reviews
        if test_for_no_reviews:
            percent_pos = 'N/A'
            total_reviews = '0'
        else:
            try:
                review_summary = response.xpath(
                    '//span[@class="nonresponsive_hidden responsive_reviewdesc"]/text()').extract_first().strip()
            except Exception as e:
                logging.error(f"Error extracting review_summary: {e}")
                review_summary = ""

            # Handle games with reviews but not enough for percent positive.
            if review_summary.find('Need') >= 0:
                percent_pos = 'N/A'
                try:
                    total_reviews = re.search('(\d+) user', response.xpath(
                        '//span[@class="game_review_summary not_enough_reviews"]/text()').extract_first()).group(1)
                except Exception as e:
                    logging.error(f"Error extracting total_reviews: {e}")
                    total_reviews = '0'
            # Handle games with large number of reviews
            else:
                try:
                    total_reviews = \
                    response.xpath('//div[@class="summary column"]/span[@class="responsive_hidden"]/text()').extract()[
                        -1].strip().strip('()').replace(',', '')
                except Exception as e:
                    logging.error(f"Error extracting total_reviews: {e}")
                    total_reviews = '0'
                try:
                    percent_pos = re.search('(\d+)%', response.xpath(
                        '//span[@class="nonresponsive_hidden responsive_reviewdesc"]/text()').extract_first()).group(1)
                except Exception as e:
                    logging.error(f"Error extracting percent_pos: {e}")
                    percent_pos = 'N/A'

        try:
            developer = response.xpath('//div[@id="developers_list"]/a/text()').extract_first()
        except Exception as e:
            logging.error(f"Error extracting developer: {e}")
            developer = ""

        try:
            publisher = response.xpath('//div[@class="summary column"]/a/text()').extract_first()
        except Exception as e:
            logging.error(f"Error extracting publisher: {e}")
            publisher = ""

        # Set a boolean for games under the early access program.
        try:
            early_access = response.xpath('//div[@class="early_access_header"]') != []
        except Exception as e:
            logging.error(f"Error extracting early_access: {e}")
            early_access = False

        # Set boolean for games with VR support
        try:
            vr_only = response.xpath('.//span[@class="vr_required"' +
                                     ']') != []
            vr_supported = response.xpath('.//span[@class="vr_supported"' +
                                          ']') != []
            vr_pcinput = list(map(lambda x: x.strip(), response.xpath(
                '//div[@class="VR_warning"]/text()').extract()))
        except Exception as e:
            logging.error(f"Error extracting VR support: {e}")
            vr_only = False
            vr_supported = False
            vr_pcinput = []

        game_item['tag_list'] = tag_list
        game_item['description'] = description
        game_item['percent_pos'] = percent_pos
        game_item['total_reviews'] = total_reviews
        game_item['release_date'] = release_date
        game_item['developer'] = developer
        game_item['publisher'] = publisher
        game_item['early_access'] = early_access
        game_item['vr_only'] = vr_only
        game_item['vr_supported'] = vr_supported
        game_item['vr_pcinput'] = vr_pcinput
        return game_item
