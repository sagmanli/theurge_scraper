# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from itemloaders.processors import MapCompose, TakeFirst
import scrapy

class TheurgeScraperItem(scrapy.Item):
    title = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=MapCompose(str.strip))
    currency = scrapy.Field()
    brand = scrapy.Field()
    category = scrapy.Field(output_processor=MapCompose(str.lower))
    gender = scrapy.Field()

    url = scrapy.Field(output_processor=TakeFirst())
    project = scrapy.Field(output_processor=TakeFirst())
    spider = scrapy.Field(output_processor=TakeFirst())


class TheurgeApiItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    brand = scrapy.Field()
    category = scrapy.Field()

    url = scrapy.Field()
    project = scrapy.Field()
    spider = scrapy.Field()

