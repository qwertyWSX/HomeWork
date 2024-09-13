# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json


class BookparserPipeline:
    def __init__(self):
        self.file = None
        self.first_item = True

    def open_spider(self, spider):
        self.file = open("books.json", "w", encoding="utf-8")
        self.file.write("[\n")

    def close_spider(self, spider):
        if not self.first_item:
            self.file.write("\n")
        self.file.write("]\n")
        self.file.close()

    def process_item(self, item, spider):

        item["title"] = item.get("title", "").split(": ")[1]
        item["authors"] = item.get("authors", [])
        publisher = item.get("publisher", "")
        item["publisher"] = publisher[1]
        item["year"] = publisher[2].split(" ")[1]
        item["price"] = item.get("price", "")
        item["ISBN"] = item.get("ISBN", "")
        item["pages"] = item.get("pages", "")

        if self.first_item:
            self.first_item = False
        else:
            self.file.write(",\n")
        json.dump(dict(item), self.file, ensure_ascii=False)
        return item
