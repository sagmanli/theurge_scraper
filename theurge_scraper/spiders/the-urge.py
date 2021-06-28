import os
from scrapy.loader import ItemLoader
from theurge_scraper.items import TheurgeScraperItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import yaml


class TheUrgeSpider(CrawlSpider):
    name = 'the-urge'
    allowed_domains = ['www.theurge.com', 'theurge.com']
    start_urls = ['https://theurge.com']

    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'yaml_configs/%s.yml' % name)) as yaml_fileobj:
            config = yaml.safe_load(yaml_fileobj.read())

    rules = []

    for extractor in config['extractors'].keys():
        rules.append(Rule(LinkExtractor(restrict_xpaths=config['extractors'][extractor].get('xpath')),
                          callback=config['extractors'][extractor].get('callback', None)))

    def parse_item(self, response):
        """
        @url https://theurge.com/product/black-martine-rose-logo-print-cotton-jersey-long-sleeved-t-shirt-1384538-mf
        @returns items 1
        @scrapes title price category
        @scrapes url project spider
        """
        l = ItemLoader(item = TheurgeScraperItem(), response=response)

        for field in self.config['fields'].keys():
            l.add_xpath(field, self.config['fields'][field]['xpath'])

        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('spider', self.name)

        return l.load_item()

