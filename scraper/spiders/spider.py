from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.selector import Selector
try:
    from basic_splash.scraper.items import ScraperItem
except ImportError:
    from scraper.items import ScraperItem
from subprocess import Popen,PIPE
from scrapy.cmdline import execute
from pathlib import Path
from scrapy.shell import inspect_response
from scrapy.utils.response import open_in_browser


SPIDERNAME = Path(__file__).stem
BASE_URL = 'http://quotes.toscrape.com/'

class SimpleSpider(Spider):
    name = SPIDERNAME
    start_urls = [
        BASE_URL
    ]
    referer = BASE_URL

    custom_settings = {
        "ITEM_PIPELINES":{
        'scraper.pipelines.ScraperPipeline': 300,
        }
    }

    def start_requests(self):
        for item in self.start_urls:
            yield Request(url=item, headers={'Referer': self.referer})

    def parse(self, response):
        quotes = response.xpath('//*[@class="quote"]')
        for quote in quotes:
            text = quote.xpath(".//*[@class='text']/text()").get()
            author = quote.xpath(".//*[@class='author']/text()").get()
            tags = quote.xpath(".//*[@class='tag']/text()").get()
            yield {"text": text, "author": author, "tags": tags}

        next_page_url = response.xpath('//*[@class="next"]/a/@href').get()
        # inspect_response(response, self)
        if next_page_url:
            yield response.follow(next_page_url, callback=self.parse)

def rewrite_file(filename):
    if filename.exists():
        f = open(str(filename), 'w')
        f.close()

if __name__ == '__main__':

    LOG_LEVEL = 'DEBUG'
    outcome_data_filename = Path(__file__).parents[1] / 'data' / '{}.csv'.format(SPIDERNAME)
    rewrite_file(outcome_data_filename)

    # execute("scrapy crawl {0} -o {1} -L {2}"
    #        .format(SPIDERNAME, str(outcome_data_filename), LOG_LEVEL).split())

    print("scrapy crawl {0} -o {1} -L {2}"
          .format(SPIDERNAME, str(outcome_data_filename), LOG_LEVEL))


