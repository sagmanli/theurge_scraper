from time import time

from scrapy.exceptions import NotConfigured
from scrapy import signals


class Latencies(object):
    """
    An extension that measures request and response latencies
    """
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def __init__(self, crawler):
        self.crawler = crawler
        self.interval = crawler.settings.getfloat('LATENCIES_INTERVAL')

        if not self.interval:
            raise NotConfigured

        cs = crawler.signals
        cs.connect(self._request_scheduled, signal=signals.request_scheduled)
        cs.connect(self._response_received, signal=signals.response_received)
        cs.connect(self._item_scraped, signal=signals.item_scraped)

        self.req_latency,self.res_latency = 0,0


    def _request_scheduled(self, request, spider):
        request.meta['schedule_time'] = time()

    def _response_received(self, response, request, spider):
        request.meta['received_time'] = time()

    def _item_scraped(self, item, response, spider):
        self.req_latency += time() - response.meta['schedule_time']
        self.res_latency += time() - response.meta['received_time']
        spider.logger.info("Request latency: %.2f, Response latency: %.2f"
                           %(self.req_latency, self.res_latency))
        self.req_latency, self.res_latency = 0,0

