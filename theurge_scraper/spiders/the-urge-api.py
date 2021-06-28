from scrapy.loader import ItemLoader
from theurge_scraper.items import TheurgeApiItem
from itemloaders.processors import TakeFirst
import scrapy

base = 'https://api.theurge.com/search-results?page={}'

class TheUrgeSpider(scrapy.Spider):
    name = 'the-urge-api'
    page_counter = 1
    start_urls = [base.format(page_counter)]

    def parse(self, response):
        """
        @url https://api.theurge.com/search-results?page=1

        @returns items 20
        @scrapes title price description brand category
        @scrapes url project spider
        """
        self.page_counter += 1
        data = response.json()
        total = data['meta']['meta']['total']
        pageSize = data['meta']['meta']['pageSize']

        for product in data['data']:

            l = ItemLoader(item = TheurgeApiItem(), response=response)
            l.default_output_processor = TakeFirst()

            l.add_value('title', product['attributes']['e_product_name'])
            l.add_value('price', product['attributes']['retailer_price'])
            l.add_value('description', product['attributes']['long_description'])
            l.add_value('brand', product['attributes']['e_brand_formatted'])
            l.add_value('category', product['attributes']['e_categories'])

            l.add_value('url', product['attributes']['friendly_canonical'])
            l.add_value('project', self.settings.get('BOT_NAME'))
            l.add_value('spider', self.name)

            yield l.load_item()

        if self.page_counter <= total/pageSize:
            yield scrapy.Request(base.format(self.page_counter))
