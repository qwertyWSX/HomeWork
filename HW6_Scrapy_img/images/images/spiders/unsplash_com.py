import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from scrapy.loader import ItemLoader
from ..items import ImagesItem
from itemloaders.processors import MapCompose
from scrapy.http import HtmlResponse


class UnsplashComSpider(CrawlSpider):
    name = "unsplash_com"
    allowed_domains = ["unsplash.com"]
    start_urls = ["https://unsplash.com/s/photos/space"]

    # rules = (Rule(LinkExtractor(allow=r"Items/"), callback="parse_item", follow=True),)
    rules = (
        Rule(
            LinkExtractor(restrict_xpaths="//div[@class='jWMSo']"),
            callback="parse_item",
            follow=True,
        ),
    )

    def parse_item(self, response: HtmlResponse):
        print("Парсинг", response.url)

        loader = ItemLoader(item=ImagesItem(), response=response)
        loader.default_input_processor = MapCompose(str.strip)

        title = response.xpath("//title/text()").get()
        loader.add_value("name", title)

        url = response.xpath(
            "//div[@class='wdUrX']/img[@class='I7OuT DVW3V L1BOa']/@srcset"
        ).get()
        if url:
            url = url.split(", ")[0]
        loader.add_value("url", url)

        category = response.xpath("//div[@class='zb0Hu atI7H']/a/text()").get()
        loader.add_value("category", category)

        yield loader.load_item()
