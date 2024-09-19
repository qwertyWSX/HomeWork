# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import scrapy


class ImgPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item["url"][0]:
            try:
                yield scrapy.Request(item["url"][0])
            except Exception as e:
                print(e)
