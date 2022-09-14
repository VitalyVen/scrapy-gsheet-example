from typing import Iterator, Optional

from scrapy.crawler import CrawlerProcess
from scrapy.http import Request, Response
from scrapy.spiders import Spider
from scrapy.utils.project import get_project_settings

BASE_URL = "https://quotes.toscrape.com/"
settings = get_project_settings()


class SimpleSpider(Spider):  # type: ignore[misc]
    name: Optional[str] = "quote"
    custom_settings: dict[str, str | int | bool | dict[str, int]] = {
        "ITEM_PIPELINES": {
            "scraper.pipelines.ScraperPipeline": 300,
        }
    }

    def start_requests(self) -> Iterator[Request]:
        yield Request(BASE_URL)

    def parse(self, response: Response) -> Iterator[dict[str, str]]:
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


if __name__ == "__main__":
    # This part is not launched in production with scrapyd, used it for make your local development more productive
    dev_settings: dict[str, str | int | bool | dict[str, int]] = {
        "LOG_LEVEL": "DEBUG",
        # "HTTPCACHE_ENABLED": True,
    }
    process = CrawlerProcess(settings=settings)
    SimpleSpider.custom_settings = SimpleSpider.custom_settings or {} | dev_settings
    process.crawl(SimpleSpider)
    process.start()  # the script will block here until the crawling is finished
