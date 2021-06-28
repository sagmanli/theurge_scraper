# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import re
import locale

class TheurgeScraperPipeline:
    def process_item(self, item, spider):
        item['currency'] = item['price'][0]
        item['price'] = re.sub(r'[^0-9'+locale.localeconv()['decimal_point']+r']+', '', str(item['price'][-1]))
        item['gender'] = item['category'][0]
        item['brand'] = item['category'][1]
        item['category'] = '-'.join(item['category'][2:]).replace(' ', '_')


        return item

