# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TigerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    product_code = scrapy.Field()
    image_urls = scrapy.Field()  # ✔️ phải là image_urls (plural) -> Dùng để gửi link ảnh sang ImagesPipeline (Pipeline mong đợi image_urls là một list)
    images = scrapy.Field()      # ✔️ nơi Scrapy sẽ lưu metadata ảnh sau khi tải xong ->  ImagesPipeline sẽ ghi dữ liệu ảnh tải về tại đây
    product_url = scrapy.Field()
