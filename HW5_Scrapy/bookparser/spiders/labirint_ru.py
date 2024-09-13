import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem


class LabirintRuSpider(scrapy.Spider):
    name = "labirint_ru"
    allowed_domains = ["labirint.ru"]
    start_urls = ["https://www.labirint.ru/genres/3079/"]

    def parse(self, response: HtmlResponse):
        links = response.xpath(
            "//div[@class='genres-catalog']//a[@class='product-title-link']/@href"
        ).getall()

        for link in links:
            yield response.follow(link, callback=self.book_parse)

        next_page = response.xpath(
            "//div[@class='pagination-next']//a[@class='pagination-next_text']/@href"
        ).get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def book_parse(self, response: HtmlResponse):
        title = response.xpath("//div[@class='prodtitle']/h1/text()").get()
        authors = response.xpath("//div[@class='authors']//a/text()").getall()
        publisher = response.xpath("//div[@class='publisher']//text()").getall()
        price = response.xpath(
            "//div[@class='buying']//span[@class='buying-pricenew-val-number']//text()"
        ).get()
        ISBN = response.xpath(
            "//span[text()='ISBN: ']/following-sibling::div/text()"
        ).get()
        pages = response.xpath(
            "//div[text()='Страниц']/following-sibling::div/div/text()"
        ).get()
        yield BookparserItem(
            title=title,
            authors=authors,
            publisher=publisher,
            price=price,
            ISBN=ISBN,
            pages=pages,
        )
