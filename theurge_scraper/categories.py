from scrapy.exceptions import NotConfigured
from twisted.internet import task
from scrapy import signals
from collections import defaultdict


class Categories(object):
    """
    An extension that counts the number of scraped categories
    """
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def __init__(self, crawler):
        self.crawler = crawler
        self.interval = crawler.settings.getfloat('LOGSTATS_INTERVAL')

        if not self.interval:
            raise NotConfigured

        cs = crawler.signals
        cs.connect(self._spider_opened, signal=signals.spider_opened)
        cs.connect(self._spider_closed, signal=signals.spider_closed)
        cs.connect(self._item_scraped, signal=signals.item_scraped)

        self.categories = defaultdict(int)

    def _spider_opened(self, spider):
        self.task = task.LoopingCall(self._log, spider)
        self.task.start(self.interval)

    def _spider_closed(self):
        if self.task.running:
            self.task.stop()

    def _item_scraped(self, item):
        self.categories[item['category']] += 1


    def _log(self, spider):
        spider.logger.info('Total number of distinct categories scraped: %d, Category counts: %s'
                           % (len(self.categories.keys()), ", ".join("{}: {}".format(k, v) for k, v in self.categories.items())))