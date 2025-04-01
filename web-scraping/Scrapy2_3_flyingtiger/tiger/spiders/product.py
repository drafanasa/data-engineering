import scrapy
from ..items import TigerItem


class ProductSpider(scrapy.Spider):
    name = "product"
    allowed_domains = ["flyingtiger.com"]
    start_urls = ["https://flyingtiger.com/collections/shop-all"] # URL chứa all sản phẩm, phù hợp nhất để scrap

    def parse(self, response):
        container = response.css('ul#product-grid')
        item_in_a_tags = container.css('a.card__information--title')

        # Vòng lặp tìm link dẫn đến page riêng của từng sản phẩm (product_url)
        for a_tag in item_in_a_tags:
            product_url = a_tag.xpath('./@href').get()
            full_url = response.urljoin(product_url)  # Ghép URL tuyệt đối
            yield scrapy.Request(full_url, callback=self.parse_items) # Trả về product_url + chạy function parse item để cào data của sản phẩm này

        # Xử lý paginaction với next button:
        next_page_link = response.xpath('//a[@aria-label="Next"]/@href').get()
        if next_page_link:
            yield response.follow(next_page_link, callback=self.parse) # Follow nút next + chạy lại function parse để tiếp tục lấy product_url

    def parse_items(self, response):

        # Khởi tạo danh sách 'tiger_item' dựa trên thông tin được định nghĩa trong khuôn mẫu class TigerItem() ở items.py
        tiger_item = TigerItem()

        # Scrap các trường thông tin cần thiết
        tiger_item['name'] = response.xpath('//h1[@class="title"]/text()').get().strip()

        tiger_item['price'] = response.xpath('//span[@class="subtitle--s price-item price-item--regular"]/text()').get().strip()

        tiger_item['product_code'] = response.xpath('//div[@class="product__sku"]/text()').get().split(':')[-1].strip()

        # Dùng selector là css vì xpath bị lỗi!
        img_src = response.css('div.product__media img::attr(src)').get()
        if img_src:
            tiger_item['image_urls'] = ['https:' + img_src.split('?')[0]]  # ✔️  Scrapy ImagePipeline mong đợi image_urls phải là một list, do đó lưu ý không được truyền string sẽ làm cho pipeline không hoạt động
        else:
            tiger_item['image_urls'] = []

        tiger_item['product_url'] = response.url  # URL của trang sản phẩm hiện tại

        yield tiger_item # Lưu data vừa scrap được vào danh sách 'tiger_item'