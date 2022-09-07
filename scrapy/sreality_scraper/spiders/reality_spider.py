import scrapy
from scrapy_playwright.page import PageCoroutine
from scrapy_playwright.page import PageMethod


class RealitySpider(scrapy.Spider):
    name = "reality_spider"

    def start_requests(self):

        # set up urls for crawling
        url = "https://www.sreality.cz/hledani/prodej/byty?strana="
        urls = ["https://www.sreality.cz/hledani/prodej/byty"]
        for page in range(2, 26):
            urls.append(url + str(page))

        for url in urls:

            # use playwright module to load the whole page including js
            yield scrapy.Request(
                url,
                meta={
                    "playwright": True,
                    "playwright_include_page": True,
                    "playwright_page_coroutines": [
                        PageCoroutine("wait_for_selector", "div.property.ng-scope"),
                        PageMethod(
                            "wait_for_selector", "div.property.ng-scope:nth-child(20)"
                        ),
                    ],
                },
            )

    async def parse(self, response):

        # save the html after all scripts were loaded
        yield {"text": response.text}
